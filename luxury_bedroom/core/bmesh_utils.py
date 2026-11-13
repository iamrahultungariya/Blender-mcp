"""Procedural BMesh Geometric Operators & High-Density Surface Math.

High-performance in-memory procedural modeling in C-RAM for Blender MCP.
Implements the 90/10 Hybrid Pipeline Standard: Zero UI context, sub-second execution,
pure bmesh math operators, multi-material face slot tagging.
"""
from __future__ import annotations

import math
from typing import Any, List, Optional, Sequence, Tuple, Union

try:
    import bpy
    import bmesh
    from mathutils import Matrix, Vector
    HAS_BMESH = True
except ImportError:
    bpy = None
    bmesh = None
    Matrix = None
    Vector = None
    HAS_BMESH = False


# ==============================================================================
# Lightweight Mock BMesh for Standalone Unit Tests Outside Blender
# ==============================================================================

class MockBMVert:
    def __init__(self, co: Tuple[float, float, float], index: int = 0) -> None:
        self.co = _VectorMock(co)
        self.index = index


class _VectorMock:
    def __init__(self, coords: Tuple[float, float, float]) -> None:
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.z = float(coords[2])

    def __getitem__(self, item: int) -> float:
        return (self.x, self.y, self.z)[item]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def copy(self) -> "_VectorMock":
        return _VectorMock((self.x, self.y, self.z))


class MockBMFace:
    def __init__(self, verts: Sequence[MockBMVert], material_index: int = 0) -> None:
        self.verts = list(verts)
        self.material_index = material_index
        self.normal = _VectorMock((0.0, 0.0, 1.0))


class MockBMesh:
    """Mock bmesh.BMesh for executing unit tests in headless Python without Blender binaries."""

    def __init__(self) -> None:
        self.verts: List[MockBMVert] = []
        self.faces: List[MockBMFace] = []
        self.edges: List[Any] = []

    @classmethod
    def new(cls) -> "MockBMesh":
        return cls()

    def free(self) -> None:
        self.verts.clear()
        self.faces.clear()
        self.edges.clear()


# ==============================================================================
# Procedural BMesh Primitives & Anti-Boxy Operators
# ==============================================================================

def create_beveled_box(
    bm: Any,
    width: float,
    length: float,
    height: float,
    bevel_radius: float = 0.02,
    segments: int = 2,
    offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    mat_index: int = 0,
) -> Any:
    """Create an axis-aligned box with beveled chamfers and material index tagging."""
    ox, oy, oz = offset
    hx, hy, hz = width / 2.0, length / 2.0, height / 2.0
    cx, cy, cz = ox, oy, oz + hz

    if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
        res = bmesh.ops.create_cube(bm, size=1.0)
        cube_verts = res["verts"]
        mat_trans = Matrix.Translation(Vector((cx, cy, cz))) @ Matrix.Diagonal(
            Vector((width, length, height, 1.0))
        )
        bmesh.ops.transform(bm, verts=cube_verts, matrix=mat_trans)

        safe_bevel = min(bevel_radius, min(width, length, height) * 0.4)
        if safe_bevel > 0.002:
            edges = [e for e in bm.edges if all(v in cube_verts for v in e.verts)]
            if edges:
                bmesh.ops.bevel(
                    bm,
                    geom=edges,
                    offset=safe_bevel,
                    segments=segments,
                    profile=0.5,
                    affect="EDGES",
                )

        for f in bm.faces:
            if any(v in cube_verts for v in f.verts):
                f.material_index = mat_index
        return bm
    else:
        # Mock / Fallback pure python generator
        corners = [
            (cx - hx, cy - hy, cz - hz),
            (cx + hx, cy - hy, cz - hz),
            (cx + hx, cy + hy, cz - hz),
            (cx - hx, cy + hy, cz - hz),
            (cx - hx, cy - hy, cz + hz),
            (cx + hx, cy - hy, cz + hz),
            (cx + hx, cy + hy, cz + hz),
            (cx - hx, cy + hy, cz + hz),
        ]
        verts = [MockBMVert(c, len(bm.verts) + idx) for idx, c in enumerate(corners)]
        bm.verts.extend(verts)
        face_idx = [
            (0, 1, 2, 3), (4, 5, 6, 7),
            (0, 1, 5, 4), (2, 3, 7, 6),
            (0, 3, 7, 4), (1, 2, 6, 5),
        ]
        for f in face_idx:
            bm.faces.append(MockBMFace([verts[i] for i in f], material_index=mat_index))
        return bm


def create_cushion_loft(
    bm: Any,
    width: float,
    length: float,
    height: float,
    crown: float = 0.04,
    subdivisions_u: int = 8,
    subdivisions_v: int = 8,
    offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    mat_index: int = 0,
    tilt_deg_x: float = 0.0,
) -> Any:
    """Create an organic upholstered pillow or cushion with parabolic loft and corner welt.

    Equation: Z(u,v) = z0 + height + crown * (1 - u^2) * (1 - v^2)
    """
    ox, oy, oz = offset
    rad_tilt = math.radians(tilt_deg_x)
    cos_t, sin_t = math.cos(rad_tilt), math.sin(rad_tilt)

    top_grid: List[List[Any]] = []
    bot_grid: List[List[Any]] = []

    # Generate Top and Bottom grids
    for i in range(subdivisions_u + 1):
        top_row = []
        bot_row = []
        u = -1.0 + 2.0 * (i / subdivisions_u)  # [-1, 1]
        x = u * (width / 2.0)

        for j in range(subdivisions_v + 1):
            v = -1.0 + 2.0 * (j / subdivisions_v)  # [-1, 1]
            y = v * (length / 2.0)

            # Parabolic crown deformation
            crown_factor = max(0.0, (1.0 - u * u) * (1.0 - v * v))
            zt = height + crown * crown_factor
            zb = 0.0 - (crown * 0.3) * crown_factor  # Slight bottom bulge

            # Apply tilt around back edge (y = length/2)
            y_rel = y - (length / 2.0)
            yt_rot = y_rel * cos_t - zt * sin_t + (length / 2.0)
            zt_rot = y_rel * sin_t + zt * cos_t

            yb_rot = y_rel * cos_t - zb * sin_t + (length / 2.0)
            zb_rot = y_rel * sin_t + zb * cos_t

            # Translate by offset
            pt_top = (ox + x, oy + yt_rot, oz + zt_rot)
            pt_bot = (ox + x, oy + yb_rot, oz + zb_rot)

            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                vt = bm.verts.new(Vector(pt_top))
                vb = bm.verts.new(Vector(pt_bot))
            else:
                vt = MockBMVert(pt_top, len(bm.verts))
                bm.verts.append(vt)
                vb = MockBMVert(pt_bot, len(bm.verts))
                bm.verts.append(vb)

            top_row.append(vt)
            bot_row.append(vb)
        top_grid.append(top_row)
        bot_grid.append(bot_row)

    # Stitch top faces
    for i in range(subdivisions_u):
        for j in range(subdivisions_v):
            v0 = top_grid[i][j]
            v1 = top_grid[i + 1][j]
            v2 = top_grid[i + 1][j + 1]
            v3 = top_grid[i][j + 1]
            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                try:
                    f = bm.faces.new((v0, v1, v2, v3))
                    f.material_index = mat_index
                except ValueError:
                    pass
            else:
                bm.faces.append(MockBMFace((v0, v1, v2, v3), material_index=mat_index))

    # Stitch bottom faces (reversed winding)
    for i in range(subdivisions_u):
        for j in range(subdivisions_v):
            v0 = bot_grid[i][j]
            v1 = bot_grid[i][j + 1]
            v2 = bot_grid[i + 1][j + 1]
            v3 = bot_grid[i + 1][j]
            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                try:
                    f = bm.faces.new((v0, v1, v2, v3))
                    f.material_index = mat_index
                except ValueError:
                    pass
            else:
                bm.faces.append(MockBMFace((v0, v1, v2, v3), material_index=mat_index))

    # Stitch side seam perimeter
    perimeter_indices = []
    for i in range(subdivisions_u):
        perimeter_indices.append((top_grid[i][0], top_grid[i + 1][0], bot_grid[i + 1][0], bot_grid[i][0]))
    for j in range(subdivisions_v):
        perimeter_indices.append((top_grid[subdivisions_u][j], top_grid[subdivisions_u][j + 1], bot_grid[subdivisions_u][j + 1], bot_grid[subdivisions_u][j]))
    for i in range(subdivisions_u - 1, -1, -1):
        perimeter_indices.append((top_grid[i + 1][subdivisions_v], top_grid[i][subdivisions_v], bot_grid[i][subdivisions_v], bot_grid[i + 1][subdivisions_v]))
    for j in range(subdivisions_v - 1, -1, -1):
        perimeter_indices.append((top_grid[0][j + 1], top_grid[0][j], bot_grid[0][j], bot_grid[0][j + 1]))

    for quad in perimeter_indices:
        if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
            try:
                f = bm.faces.new(quad)
                f.material_index = mat_index
            except ValueError:
                pass
        else:
            bm.faces.append(MockBMFace(quad, material_index=mat_index))

    return bm


def create_draped_cloth_surface(
    bm: Any,
    width: float,
    length: float,
    drape_drop: float = 0.18,
    folds_freq: float = 4.0,
    folds_amp: float = 0.015,
    subdivisions_x: int = 16,
    subdivisions_y: int = 16,
    offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    mat_index: int = 0,
    cuff_length: float = 0.25,
    cuff_mat_index: Optional[int] = None,
) -> Any:
    """Create a physically convincing bedsheet / blanket (chadar) with realistic drape & turned-down cuff."""
    ox, oy, oz = offset
    cuff_mat = mat_index if cuff_mat_index is None else cuff_mat_index

    grid: List[List[Any]] = []
    cuff_y_threshold = (length / 2.0) - cuff_length

    for i in range(subdivisions_x + 1):
        row = []
        u = -1.0 + 2.0 * (i / subdivisions_x)
        x = u * (width / 2.0)

        # Drape drop towards left/right flanks
        flank_dist = max(0.0, abs(u) - 0.75) / 0.25
        flank_drop = (flank_dist ** 2) * drape_drop

        for j in range(subdivisions_y + 1):
            v = -1.0 + 2.0 * (j / subdivisions_y)
            y = v * (length / 2.0)

            # Foot drop (bottom edge v -> -1)
            foot_dist = max(0.0, (-v) - 0.75) / 0.25
            foot_drop = (foot_dist ** 2) * drape_drop

            # Sinusoidal cloth fold deformation
            cloth_ripple = folds_amp * math.sin(folds_freq * math.pi * u) * math.cos(3.0 * math.pi * v)

            # Turned-down cuff behavior at the head edge (v -> 1)
            z_cuff_offset = 0.0
            if y > cuff_y_threshold:
                cuff_progress = (y - cuff_y_threshold) / max(0.01, cuff_length)
                z_cuff_offset = math.sin(cuff_progress * math.pi) * 0.04 - (cuff_progress * 0.02)

            z = oz + cloth_ripple - flank_drop - foot_drop + z_cuff_offset
            pt = (ox + x, oy + y, z)

            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                vert = bm.verts.new(Vector(pt))
            else:
                vert = MockBMVert(pt, len(bm.verts))
                bm.verts.append(vert)
            row.append(vert)
        grid.append(row)

    # Stitch cloth faces
    for i in range(subdivisions_x):
        for j in range(subdivisions_y):
            v0 = grid[i][j]
            v1 = grid[i + 1][j]
            v2 = grid[i + 1][j + 1]
            v3 = grid[i][j + 1]

            mid_y = (v0.co[1] + v2.co[1]) / 2.0 - oy
            active_mat = cuff_mat if mid_y > cuff_y_threshold else mat_index

            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                try:
                    f = bm.faces.new((v0, v1, v2, v3))
                    f.material_index = active_mat
                except ValueError:
                    pass
            else:
                bm.faces.append(MockBMFace((v0, v1, v2, v3), material_index=active_mat))

    return bm


def create_fluted_panel(
    bm: Any,
    width: float,
    height: float,
    depth: float = 0.06,
    num_flutes: int = 12,
    flute_radius: float = 0.015,
    offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    mat_index: int = 0,
) -> Any:
    """Create a vertical fluted acoustic or decorative headboard panel."""
    ox, oy, oz = offset

    # Base backboard
    create_beveled_box(
        bm,
        width=width,
        length=depth,
        height=height,
        bevel_radius=0.01,
        segments=2,
        offset=(ox, oy, oz),
        mat_index=mat_index,
    )

    # Vertical half-round or beveled fluted slats
    flute_spacing = width / max(1, num_flutes)
    flute_width = flute_spacing * 0.85
    flute_depth = flute_radius * 1.5

    for i in range(num_flutes):
        flute_x = ox - (width / 2.0) + (i + 0.5) * flute_spacing
        flute_y = oy + (depth / 2.0) + (flute_depth / 2.0)

        create_beveled_box(
            bm,
            width=flute_width,
            length=flute_depth,
            height=height * 0.98,
            bevel_radius=flute_radius * 0.45,
            segments=2,
            offset=(flute_x, flute_y, oz + (height * 0.01)),
            mat_index=mat_index,
        )

    return bm


def create_pleated_surface(
    bm: Any,
    width: float,
    length: float,
    pleat_freq: float = 8.0,
    pleat_amp: float = 0.03,
    subdivisions_x: int = 24,
    subdivisions_y: int = 16,
    offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    mat_index: int = 0,
    along_axis: str = "X",
) -> Any:
    """Create a high-density sinusoidal pleated surface for curtains, runners, and accordion fabrics."""
    ox, oy, oz = offset
    grid: List[List[Any]] = []

    for i in range(subdivisions_x + 1):
        row = []
        u = -1.0 + 2.0 * (i / subdivisions_x)
        x = u * (width / 2.0)

        for j in range(subdivisions_y + 1):
            v = -1.0 + 2.0 * (j / subdivisions_y)
            y = v * (length / 2.0)

            if along_axis == "X":
                wave = pleat_amp * math.sin(pleat_freq * math.pi * u)
            else:
                wave = pleat_amp * math.sin(pleat_freq * math.pi * v)

            pt = (ox + x, oy + y, oz + wave)

            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                vert = bm.verts.new(Vector(pt))
            else:
                vert = MockBMVert(pt, len(bm.verts))
                bm.verts.append(vert)
            row.append(vert)
        grid.append(row)

    # Stitch quad faces
    for i in range(subdivisions_x):
        for j in range(subdivisions_y):
            v0 = grid[i][j]
            v1 = grid[i + 1][j]
            v2 = grid[i + 1][j + 1]
            v3 = grid[i][j + 1]
            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                try:
                    f = bm.faces.new((v0, v1, v2, v3))
                    f.material_index = mat_index
                except ValueError:
                    pass
            else:
                bm.faces.append(MockBMFace((v0, v1, v2, v3), material_index=mat_index))

    return bm


def create_lathe_mesh(
    bm: Any,
    profile: List[Tuple[float, float]],
    segs: int = 24,
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    mat_index: int = 0,
) -> Any:
    """Revolve a 2D profile [(radius, z_offset), ...] around the Z-axis with high radial density."""
    cx, cy, cz = center
    rings: List[List[Any]] = []

    for r, pz in profile:
        ring = []
        if r <= 0.001:
            pt = (cx, cy, cz + pz)
            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                v = bm.verts.new(Vector(pt))
            else:
                v = MockBMVert(pt, len(bm.verts))
                bm.verts.append(v)
            ring = [v] * segs
        else:
            for s in range(segs):
                angle = (2.0 * math.pi * s) / segs
                px = cx + r * math.cos(angle)
                py = cy + r * math.sin(angle)
                pt = (px, py, cz + pz)
                if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                    v = bm.verts.new(Vector(pt))
                else:
                    v = MockBMVert(pt, len(bm.verts))
                    bm.verts.append(v)
                ring.append(v)
        rings.append(ring)

    # Stitch quads between consecutive profile rings
    for r_idx in range(len(profile) - 1):
        r0 = rings[r_idx]
        r1 = rings[r_idx + 1]
        for s in range(segs):
            nxt = (s + 1) % segs
            v0 = r0[s]
            v1 = r0[nxt]
            v2 = r1[nxt]
            v3 = r1[s]

            if v0 == v1 and v2 != v3:
                quad = (v0, v2, v3)
            elif v2 == v3 and v0 != v1:
                quad = (v0, v1, v2)
            elif v0 != v1 and v2 != v3:
                quad = (v0, v1, v2, v3)
            else:
                continue

            if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                try:
                    f = bm.faces.new(quad)
                    f.material_index = mat_index
                except ValueError:
                    pass
            else:
                bm.faces.append(MockBMFace(quad, material_index=mat_index))

    return bm
