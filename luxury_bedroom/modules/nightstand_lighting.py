"""Floating Cantilever Nightstands & Suspended Designer Pendant Lighting.

Constructs dual floating nightstands with concealed drawer bevels and brushed brass pulls,
paired with suspended minimalist cylindrical brass pendant fixtures with warm emissive diffusers.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    MockBMVert,
    MockBMFace,
    HAS_BMESH,
)
from luxury_bedroom.core.materials import MaterialLibrary

try:
    import bmesh
    from mathutils import Matrix, Vector
except ImportError:
    bmesh = None
    Matrix = None
    Vector = None


class NightstandLightingBuilder:
    """Builder for dual floating nightstands and overhead pendant light fixtures."""

    def __init__(
        self,
        stand_width: float = 0.55,
        stand_depth: float = 0.42,
        stand_height: float = 0.22,
        stand_elevation_z: float = 0.42,
        bed_clearance_gap: float = 0.08,
        pendant_radius: float = 0.04,
        pendant_height: float = 0.32,
        ceiling_z: float = 2.80,
    ) -> None:
        self.stand_width = stand_width
        self.stand_depth = stand_depth
        self.stand_height = stand_height
        self.stand_elevation_z = stand_elevation_z
        self.bed_clearance_gap = bed_clearance_gap
        self.pendant_radius = pendant_radius
        self.pendant_height = pendant_height
        self.ceiling_z = ceiling_z

    def _create_cylinder(
        self,
        bm: Any,
        radius: float,
        height: float,
        center: Tuple[float, float, float],
        segments: int = 16,
        mat_index: int = 0,
    ) -> None:
        """Create a smooth vertical cylinder at center (x, y, z)."""
        cx, cy, cz = center
        hz = height / 2.0

        if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
            top_verts = []
            bot_verts = []
            for i in range(segments):
                angle = (2.0 * math.pi * i) / segments
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                vt = bm.verts.new(Vector((x, y, cz + hz)))
                vb = bm.verts.new(Vector((x, y, cz - hz)))
                top_verts.append(vt)
                bot_verts.append(vb)

            # Stitch side quads
            for i in range(segments):
                nxt = (i + 1) % segments
                try:
                    f = bm.faces.new((bot_verts[i], bot_verts[nxt], top_verts[nxt], top_verts[i]))
                    f.material_index = mat_index
                except ValueError:
                    pass

            # Caps
            try:
                ft = bm.faces.new(reversed(top_verts))
                ft.material_index = mat_index
                fb = bm.faces.new(bot_verts)
                fb.material_index = mat_index
            except ValueError:
                pass
        else:
            # Mock fallback
            corners = [
                (cx - radius, cy - radius, cz - hz),
                (cx + radius, cy - radius, cz - hz),
                (cx + radius, cy + radius, cz - hz),
                (cx - radius, cy + radius, cz - hz),
                (cx - radius, cy - radius, cz + hz),
                (cx + radius, cy - radius, cz + hz),
                (cx + radius, cy + radius, cz + hz),
                (cx - radius, cy + radius, cz + hz),
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

    def build(self, bm: Any, bed_datum: Dict[str, Any], mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct dual nightstands and pendant lights into BMesh."""
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        brass_idx = mat_lib.get_index("BRUSHED_BRASS")
        cove_idx = mat_lib.get_index("LED_WARM_COVE")

        bed_w = bed_datum["bed_width"]
        head_center = bed_datum["headboard_center"]
        stand_y = head_center[1] - (self.stand_depth / 2.0) - 0.05
        side_offset_x = (bed_w / 2.0) + (self.stand_width / 2.0) + self.bed_clearance_gap

        left_x = -side_offset_x
        right_x = +side_offset_x

        positions = [left_x, right_x]

        for sx in positions:
            # 1. Floating Nightstand Carcass
            create_beveled_box(
                bm,
                width=self.stand_width,
                length=self.stand_depth,
                height=self.stand_height,
                bevel_radius=0.015,
                segments=2,
                offset=(sx, stand_y, self.stand_elevation_z),
                mat_index=walnut_idx,
            )

            # 2. Minimalist Brass Pull Handle
            handle_y = stand_y - (self.stand_depth / 2.0) - 0.01
            create_beveled_box(
                bm,
                width=0.14,
                length=0.015,
                height=0.018,
                bevel_radius=0.004,
                segments=2,
                offset=(sx, handle_y, self.stand_elevation_z + (self.stand_height * 0.5)),
                mat_index=brass_idx,
            )

            # 3. Suspended Pendant Fixture
            pendant_center_z = self.stand_elevation_z + self.stand_height + 0.65
            # Brass fixture body
            self._create_cylinder(
                bm,
                radius=self.pendant_radius,
                height=self.pendant_height,
                center=(sx, stand_y, pendant_center_z),
                segments=16,
                mat_index=brass_idx,
            )
            # Emissive diffuser tip
            self._create_cylinder(
                bm,
                radius=self.pendant_radius * 0.92,
                height=0.03,
                center=(sx, stand_y, pendant_center_z - (self.pendant_height / 2.0) - 0.015),
                segments=16,
                mat_index=cove_idx,
            )
            # Thin suspension cord to ceiling
            cord_h = max(0.1, self.ceiling_z - (pendant_center_z + self.pendant_height / 2.0))
            cord_cz = pendant_center_z + (self.pendant_height / 2.0) + (cord_h / 2.0)
            self._create_cylinder(
                bm,
                radius=0.003,
                height=cord_h,
                center=(sx, stand_y, cord_cz),
                segments=6,
                mat_index=brass_idx,
            )

        return {
            "nightstand_left": (left_x, stand_y, self.stand_elevation_z),
            "nightstand_right": (right_x, stand_y, self.stand_elevation_z),
            "pendant_count": 2,
        }
