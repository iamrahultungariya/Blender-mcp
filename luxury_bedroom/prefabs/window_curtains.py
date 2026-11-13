"""Window & Curtains: Architectural Window Reveal & Double-Track Drapery System.

Direct procedural recreation of the left wall window and drapery from the reference turnaround sheet:
- Deep architectural window reveal on the left wall with matte black metal mullions
- Tinted/clear architectural glazing panes
- Concealed ceiling pelmet pocket with warm indirect LED strip lighting
- Dual-track drapery system:
  1. Sheer white inner curtains (fine sinusoidal wave pleats across the center)
  2. Charcoal/taupe heavy blackout side drapes (deep luxury pleated folds gathered on flanks)
  3. Brushed brass drapery trim/details
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_pleated_surface,
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


class WindowCurtainsBuilder:
    """Builder for the architectural window and dual-track drapery system."""

    def __init__(
        self,
        wall_x: float = -2.55,
        center_y: float = 0.30,
        window_width: float = 2.40,
        window_height: float = 2.20,
        window_sill_z: float = 0.40,
        pelmet_z: float = 2.65,
    ) -> None:
        self.wall_x = wall_x
        self.center_y = center_y
        self.window_width = window_width
        self.window_height = window_height
        self.window_sill_z = window_sill_z
        self.pelmet_z = pelmet_z

    def _create_vertical_pleated_curtain(
        self,
        bm: Any,
        center_x: float,
        center_y: float,
        base_z: float,
        width_y: float,
        height_z: float,
        pleat_freq: float,
        pleat_amp: float,
        subdiv_y: int,
        subdiv_z: int,
        mat_index: int,
        taper_factor: float = 1.0,
    ) -> None:
        """Create a vertical hanging curtain mesh with sinusoidal ripple pleating."""
        grid: List[List[Any]] = []

        for i in range(subdiv_y + 1):
            row = []
            u = -1.0 + 2.0 * (i / subdiv_y)
            y = center_y + u * (width_y / 2.0)

            for j in range(subdiv_z + 1):
                t = j / subdiv_z
                z = base_z + t * height_z

                # Taper / flare slightly near bottom for natural fabric weight pooling
                flare = 1.0 + (1.0 - t) * (taper_factor - 1.0)
                wave = pleat_amp * math.sin(pleat_freq * math.pi * u) * flare
                x = center_x + wave

                pt = (x, y, z)

                if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                    vert = bm.verts.new(Vector(pt))
                else:
                    vert = MockBMVert(pt, len(bm.verts))
                    bm.verts.append(vert)
                row.append(vert)
            grid.append(row)

        # Stitch quad faces
        for i in range(subdiv_y):
            for j in range(subdiv_z):
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

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct the window reveal, pelmet cove, and dual curtains into BMesh."""
        black_idx = mat_lib.get_index("MATTE_BLACK_METAL")
        glass_idx = mat_lib.get_index("TINTED_BRONZE_GLASS")
        sheer_idx = mat_lib.get_index("SHEER_WHITE")
        charcoal_idx = mat_lib.get_index("CHARCOAL_PLEAT")
        brass_idx = mat_lib.get_index("BRUSHED_BRASS")
        led_idx = mat_lib.get_index("LED_WARM_2700K")

        # 1. Architectural Window Frame (Matte Black Aluminum)
        frame_th = 0.05
        frame_depth = 0.12
        frame_center_x = self.wall_x + (frame_depth / 2.0)

        # Window sill
        create_beveled_box(
            bm,
            width=frame_depth + 0.04,
            length=self.window_width + 0.08,
            height=0.04,
            bevel_radius=0.005,
            segments=1,
            offset=(frame_center_x - 0.02, self.center_y, self.window_sill_z - 0.04),
            mat_index=black_idx,
        )

        # Outer Frame (Top, Bottom, Left, Right)
        # Top jamb
        create_beveled_box(
            bm,
            width=frame_depth,
            length=self.window_width,
            height=frame_th,
            bevel_radius=0.004,
            segments=1,
            offset=(
                frame_center_x,
                self.center_y,
                self.window_sill_z + self.window_height - frame_th,
            ),
            mat_index=black_idx,
        )
        # Bottom jamb
        create_beveled_box(
            bm,
            width=frame_depth,
            length=self.window_width,
            height=frame_th,
            bevel_radius=0.004,
            segments=1,
            offset=(frame_center_x, self.center_y, self.window_sill_z),
            mat_index=black_idx,
        )
        # Left stile
        create_beveled_box(
            bm,
            width=frame_depth,
            length=frame_th,
            height=self.window_height,
            bevel_radius=0.004,
            segments=1,
            offset=(
                frame_center_x,
                self.center_y - (self.window_width / 2.0) + (frame_th / 2.0),
                self.window_sill_z,
            ),
            mat_index=black_idx,
        )
        # Right stile
        create_beveled_box(
            bm,
            width=frame_depth,
            length=frame_th,
            height=self.window_height,
            bevel_radius=0.004,
            segments=1,
            offset=(
                frame_center_x,
                self.center_y + (self.window_width / 2.0) - (frame_th / 2.0),
                self.window_sill_z,
            ),
            mat_index=black_idx,
        )

        # Central Vertical Mullion
        create_beveled_box(
            bm,
            width=frame_depth * 0.9,
            length=0.035,
            height=self.window_height - (frame_th * 2.0),
            bevel_radius=0.003,
            segments=1,
            offset=(frame_center_x, self.center_y, self.window_sill_z + frame_th),
            mat_index=black_idx,
        )

        # Glass Panes (Left & Right)
        pane_w = (self.window_width - (frame_th * 2.0) - 0.035) / 2.0
        pane_h = self.window_height - (frame_th * 2.0)
        # Left pane
        create_beveled_box(
            bm,
            width=0.01,
            length=pane_w,
            height=pane_h,
            bevel_radius=0.002,
            segments=1,
            offset=(
                frame_center_x,
                self.center_y - (pane_w / 2.0) - 0.018,
                self.window_sill_z + frame_th,
            ),
            mat_index=glass_idx,
        )
        # Right pane
        create_beveled_box(
            bm,
            width=0.01,
            length=pane_w,
            height=pane_h,
            bevel_radius=0.002,
            segments=1,
            offset=(
                frame_center_x,
                self.center_y + (pane_w / 2.0) + 0.018,
                self.window_sill_z + frame_th,
            ),
            mat_index=glass_idx,
        )

        # 2. Ceiling Drapery Pelmet Pocket & Warm LED Strip
        pelmet_depth = 0.28
        pelmet_length = self.window_width + 0.60
        pelmet_x = self.wall_x + (pelmet_depth / 2.0)
        pelmet_z_pos = self.pelmet_z

        # Pelmet fascia board (concealing track mechanism)
        create_beveled_box(
            bm,
            width=0.02,
            length=pelmet_length,
            height=0.14,
            bevel_radius=0.003,
            segments=1,
            offset=(self.wall_x + pelmet_depth, self.center_y, pelmet_z_pos),
            mat_index=black_idx,
        )

        # Concealed Cove LED Light Strip in Pelmet Pocket
        create_beveled_box(
            bm,
            width=0.02,
            length=pelmet_length * 0.95,
            height=0.008,
            bevel_radius=0.002,
            segments=1,
            offset=(self.wall_x + (pelmet_depth * 0.6), self.center_y, pelmet_z_pos + 0.10),
            mat_index=led_idx,
        )

        # 3. Track 1: Sheer White Inner Curtain (Spanning across center)
        sheer_x = self.wall_x + 0.08
        sheer_height = pelmet_z_pos + 0.05
        self._create_vertical_pleated_curtain(
            bm,
            center_x=sheer_x,
            center_y=self.center_y,
            base_z=0.02,
            width_y=self.window_width * 0.90,
            height_z=sheer_height,
            pleat_freq=12.0,
            pleat_amp=0.025,
            subdiv_y=36,
            subdiv_z=20,
            mat_index=sheer_idx,
            taper_factor=1.05,
        )

        # 4. Track 2: Heavy Blackout Pleated Drapes (Gathered at Left & Right Sides)
        drape_x = self.wall_x + 0.18
        drape_height = pelmet_z_pos + 0.06
        drape_panel_w = 0.65

        # Left gathered drape panel
        left_drape_y = self.center_y - (self.window_width / 2.0) + (drape_panel_w / 3.0)
        self._create_vertical_pleated_curtain(
            bm,
            center_x=drape_x,
            center_y=left_drape_y,
            base_z=0.01,
            width_y=drape_panel_w,
            height_z=drape_height,
            pleat_freq=6.0,
            pleat_amp=0.045,
            subdiv_y=24,
            subdiv_z=20,
            mat_index=charcoal_idx,
            taper_factor=1.12,
        )

        # Right gathered drape panel
        right_drape_y = self.center_y + (self.window_width / 2.0) - (drape_panel_w / 3.0)
        self._create_vertical_pleated_curtain(
            bm,
            center_x=drape_x,
            center_y=right_drape_y,
            base_z=0.01,
            width_y=drape_panel_w,
            height_z=drape_height,
            pleat_freq=6.0,
            pleat_amp=0.045,
            subdiv_y=24,
            subdiv_z=20,
            mat_index=charcoal_idx,
            taper_factor=1.12,
        )

        # Brushed Brass Decorative Tie-Back Bands
        for dy in [left_drape_y, right_drape_y]:
            create_beveled_box(
                bm,
                width=0.06,
                length=drape_panel_w * 0.70,
                height=0.03,
                bevel_radius=0.005,
                segments=1,
                offset=(drape_x + 0.01, dy, 0.95),
                mat_index=brass_idx,
            )

        return {
            "curtains_placed": True,
            "double_track_active": True,
            "window_width": self.window_width,
            "window_height": self.window_height,
            "pelmet_height": self.pelmet_z,
            "sheer_curtain_active": True,
            "blackout_curtains_active": True,
        }
