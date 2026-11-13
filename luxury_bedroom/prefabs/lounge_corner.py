"""Lounge Corner: Curved Barrel/Tub Armchair, Pedestal Side Table & Slim Floor Lamp.

Direct procedural recreation of the lounge reading corner from the reference turnaround sheet:
- Ergonomic curved tub armchair with flared backrest contour and angled wooden legs
- Minimalist round pedestal martini side table with lathe-turned base
- Tall slender vertical floor lamp with cylindrical linen lampshade and warm glow
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_cushion_loft,
    create_lathe_mesh,
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


class LoungeCornerBuilder:
    """Builder for the lounge armchair, martini side table, and floor lamp."""

    def __init__(
        self,
        corner_origin: Tuple[float, float, float] = (1.75, -0.65, 0.0),
        chair_width: float = 0.82,
        chair_depth: float = 0.78,
        chair_height: float = 0.76,
    ) -> None:
        self.corner_origin = corner_origin
        self.chair_width = chair_width
        self.chair_depth = chair_depth
        self.chair_height = chair_height

    def _create_armchair(
        self,
        bm: Any,
        center: Tuple[float, float, float],
        boucle_idx: int,
        walnut_idx: int,
    ) -> None:
        """Create the curved tub armchair with ergonomic wrap-around backrest and wooden legs."""
        cx, cy, cz = center

        # 1. 4 Angled / Splayed Tapered Wooden Legs
        leg_h = 0.24
        leg_r_top = 0.022
        leg_r_bot = 0.014
        dx = self.chair_width * 0.32
        dy = self.chair_depth * 0.30

        leg_offsets = [
            (-dx, -dy, -0.04), (+dx, -dy, -0.04),
            (-dx, +dy, +0.02), (+dx, +dy, +0.02)
        ]

        for lx, ly, l_tilt in leg_offsets:
            leg_profile = [(leg_r_bot, 0.0), (leg_r_top, leg_h)]
            create_lathe_mesh(
                bm,
                leg_profile,
                segs=8,
                center=(cx + lx, cy + ly, cz),
                mat_index=walnut_idx,
            )

        # 2. Main Curved Tub Armchair Seat Cushion
        seat_z = cz + leg_h
        seat_thick = 0.16
        create_cushion_loft(
            bm,
            width=self.chair_width * 0.88,
            length=self.chair_depth * 0.85,
            height=seat_thick,
            crown=0.035,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(cx, cy, seat_z),
            mat_index=boucle_idx,
            tilt_deg_x=-4.0,
        )

        # 3. Flared Wrap-Around Curved Tub Backrest
        back_h = self.chair_height - leg_h - seat_thick
        back_z = seat_z + seat_thick
        # Semi-circular enveloping curved segments (7 segments from left to right)
        segs = 7
        arc_radius_x = self.chair_width * 0.44
        arc_radius_y = self.chair_depth * 0.42

        for i in range(segs):
            theta = math.pi * (0.05 + 0.90 * (i / (segs - 1)))  # arc wrapping back & sides
            bx = cx - arc_radius_x * math.cos(theta)
            by = cy + arc_radius_y * math.sin(theta)

            create_beveled_box(
                bm,
                width=0.14,
                length=0.12,
                height=back_h,
                bevel_radius=0.03,
                segments=2,
                offset=(bx, by, back_z),
                mat_index=boucle_idx,
            )

    def _create_side_table(
        self,
        bm: Any,
        center: Tuple[float, float, float],
        black_idx: int,
    ) -> None:
        """Create the round pedestal martini side table with lathe-turned profile."""
        cx, cy, cz = center

        # Profile from heavy flat base up through slender column to beveled top
        table_profile = [
            (0.18, 0.0), (0.18, 0.02), (0.02, 0.04),
            (0.018, 0.46), (0.025, 0.48), (0.22, 0.50),
            (0.22, 0.52), (0.0, 0.52),
        ]
        create_lathe_mesh(bm, table_profile, segs=20, center=(cx, cy, cz), mat_index=black_idx)

    def _create_floor_lamp(
        self,
        bm: Any,
        center: Tuple[float, float, float],
        black_idx: int,
        linen_idx: int,
        led_idx: int,
    ) -> None:
        """Create the slim vertical floor lamp with cylindrical linen lampshade."""
        cx, cy, cz = center

        # 1. Circular flat heavy base plate
        base_profile = [(0.15, 0.0), (0.15, 0.02), (0.015, 0.025)]
        create_lathe_mesh(bm, base_profile, segs=16, center=(cx, cy, cz), mat_index=black_idx)

        # 2. Slender vertical metal pole ($H=1.65m$)
        pole_profile = [(0.012, 0.025), (0.012, 1.55)]
        create_lathe_mesh(bm, pole_profile, segs=10, center=(cx, cy, cz), mat_index=black_idx)

        # 3. Cylindrical linen drum lampshade ($H=0.35m, R=0.16m$)
        shade_z = cz + 1.25
        shade_profile = [
            (0.16, 0.0), (0.16, 0.35), (0.155, 0.35),
            (0.155, 0.0), (0.16, 0.0),
        ]
        create_lathe_mesh(bm, shade_profile, segs=24, center=(cx, cy, shade_z), mat_index=linen_idx)

        # 4. Interior warm emissive light source
        bulb_profile = [(0.04, 0.12), (0.04, 0.22), (0.0, 0.22)]
        create_lathe_mesh(bm, bulb_profile, segs=12, center=(cx, cy, shade_z), mat_index=led_idx)

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct armchair, martini side table, and floor lamp."""
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")
        black_idx = mat_lib.get_index("MATTE_BLACK_METAL")
        white_idx = mat_lib.get_index("LINEN_WHITE")
        led_idx = mat_lib.get_index("LED_WARM_2700K")

        ox, oy, oz = self.corner_origin

        # 1. Curved Tub Armchair
        self._create_armchair(bm, (ox, oy, oz), boucle_idx, walnut_idx)

        # 2. Round Pedestal Martini Side Table (placed slightly forward & inward)
        table_x = ox - 0.55
        table_y = oy + 0.20
        self._create_side_table(bm, (table_x, table_y, oz), black_idx)

        # 3. Modern Slim Floor Lamp (placed behind the armchair in corner)
        lamp_x = ox + 0.35
        lamp_y = oy + 0.40
        self._create_floor_lamp(bm, (lamp_x, lamp_y, oz), black_idx, white_idx, led_idx)

        return {
            "armchair_placed": True,
            "side_table_placed": True,
            "floor_lamp_placed": True,
            "lounge_origin": self.corner_origin,
        }
