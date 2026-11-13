"""Floating Cantilever Nightstands with Black Mushroom Dome Lamps & Tabletop Plant.

Direct procedural recreation of the floating consoles from the reference turnaround sheet:
- Dual long 2-drawer floating walnut consoles with horizontal brass reveals
- Dual designer black mushroom dome table lamps with warm 2700K ambient glow
- Tabletop ceramic potted indoor plant with organic layered foliage
- Under-nightstand ambient warm LED strip
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
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


class NightstandsBuilder:
    """Builder for dual floating nightstands with dome lamps and decor."""

    def __init__(
        self,
        stand_width: float = 0.75,
        stand_depth: float = 0.45,
        stand_height: float = 0.36,
        stand_elevation_z: float = 0.20,
        bed_clearance_gap: float = 0.10,
        lamp_dome_radius: float = 0.14,
        lamp_height: float = 0.42,
    ) -> None:
        self.stand_width = stand_width
        self.stand_depth = stand_depth
        self.stand_height = stand_height
        self.stand_elevation_z = stand_elevation_z
        self.bed_clearance_gap = bed_clearance_gap
        self.lamp_dome_radius = lamp_dome_radius
        self.lamp_height = lamp_height

    def _create_dome_lamp(
        self,
        bm: Any,
        center: Tuple[float, float, float],
        black_idx: int,
        led_idx: int,
    ) -> None:
        """Create a designer black mushroom/dome table lamp."""
        cx, cy, cz = center

        # 1. Circular base plate
        base_profile = [(0.09, 0.0), (0.09, 0.015), (0.015, 0.02)]
        create_lathe_mesh(bm, base_profile, segs=16, center=(cx, cy, cz), mat_index=black_idx)

        # 2. Slender central stem
        stem_profile = [(0.012, 0.02), (0.012, self.lamp_height - 0.04)]
        create_lathe_mesh(bm, stem_profile, segs=12, center=(cx, cy, cz), mat_index=black_idx)

        # 3. Half-sphere mushroom dome shade
        dome_z = cz + self.lamp_height - 0.08
        dome_profile: List[Tuple[float, float]] = []
        steps = 8
        for s in range(steps + 1):
            theta = (math.pi / 2.0) * (s / steps)
            r = self.lamp_dome_radius * math.cos(theta)
            pz = (self.lamp_dome_radius * 0.7) * math.sin(theta)
            dome_profile.append((r, pz))

        create_lathe_mesh(bm, dome_profile, segs=20, center=(cx, cy, dome_z), mat_index=black_idx)

        # 4. Warm emissive bulb diffuser under dome
        bulb_profile = [(0.04, -0.01), (0.04, 0.02), (0.0, 0.02)]
        create_lathe_mesh(bm, bulb_profile, segs=12, center=(cx, cy, dome_z), mat_index=led_idx)

    def _create_potted_plant(
        self,
        bm: Any,
        center: Tuple[float, float, float],
        pot_mat: int,
        leaf_mat: int,
    ) -> None:
        """Create a ceramic pot with layered organic plant leaves."""
        cx, cy, cz = center

        # Ceramic planter pot
        pot_profile = [
            (0.065, 0.0), (0.075, 0.04), (0.08, 0.12),
            (0.085, 0.14), (0.075, 0.14), (0.06, 0.13),
        ]
        create_lathe_mesh(bm, pot_profile, segs=16, center=(cx, cy, cz), mat_index=pot_mat)

        # 6 radial arching leaves
        num_leaves = 6
        for l_idx in range(num_leaves):
            angle = (2.0 * math.pi * l_idx) / num_leaves
            cos_a, sin_a = math.cos(angle), math.sin(angle)

            # Curved leaf petal
            leaf_length = 0.18
            leaf_width = 0.045
            for seg in range(4):
                t = seg / 4.0
                rad_dist = 0.04 + (t * leaf_length * 0.8)
                lz = cz + 0.12 + (math.sin(t * math.pi * 0.75) * 0.14) - (t * 0.04)

                lx = cx + rad_dist * cos_a
                ly = cy + rad_dist * sin_a

                create_beveled_box(
                    bm,
                    width=leaf_width * (1.0 - t * 0.5),
                    length=leaf_width * (1.0 - t * 0.5),
                    height=0.008,
                    bevel_radius=0.002,
                    segments=1,
                    offset=(lx, ly, lz),
                    mat_index=leaf_mat,
                )

    def build(self, bm: Any, bed_datum: Dict[str, Any], mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct dual floating nightstands, lamps, and tabletop plant."""
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        brass_idx = mat_lib.get_index("BRUSHED_BRASS")
        black_idx = mat_lib.get_index("MATTE_BLACK_METAL")
        led_idx = mat_lib.get_index("LED_WARM_2700K")
        pot_mat = mat_lib.get_index("TAUPE_BOUCLE")

        bed_w = bed_datum["bed_width"]
        head_center = bed_datum["headboard_center"]
        stand_y = head_center[1] - (self.stand_depth / 2.0) - 0.08
        side_dist = (bed_w / 2.0) + (self.stand_width / 2.0) + self.bed_clearance_gap

        left_x = -side_dist
        right_x = +side_dist

        for sx in [left_x, right_x]:
            # 1. Main Floating Walnut Console Carcass
            create_beveled_box(
                bm,
                width=self.stand_width,
                length=self.stand_depth,
                height=self.stand_height,
                bevel_radius=0.02,
                segments=2,
                offset=(sx, stand_y, self.stand_elevation_z),
                mat_index=walnut_idx,
            )

            # 2. Horizontal Brushed Brass Channel Reveal between Drawers
            channel_z = self.stand_elevation_z + (self.stand_height * 0.5) - 0.008
            create_beveled_box(
                bm,
                width=self.stand_width * 0.98,
                length=0.015,
                height=0.016,
                bevel_radius=0.003,
                segments=1,
                offset=(sx, stand_y - (self.stand_depth / 2.0) - 0.008, channel_z),
                mat_index=brass_idx,
            )

            # 3. Under-Nightstand Warm Ambient LED Glow Strip
            create_beveled_box(
                bm,
                width=self.stand_width * 0.90,
                length=self.stand_depth * 0.75,
                height=0.01,
                bevel_radius=0.002,
                segments=1,
                offset=(sx, stand_y, self.stand_elevation_z - 0.012),
                mat_index=led_idx,
            )

            # 4. Black Mushroom Dome Table Lamp
            lamp_x = sx + (0.12 if sx < 0 else -0.12)
            lamp_y = stand_y
            lamp_z = self.stand_elevation_z + self.stand_height
            self._create_dome_lamp(bm, (lamp_x, lamp_y, lamp_z), black_idx, led_idx)

        # 5. Tabletop Plant on Left Nightstand
        plant_x = left_x - 0.16
        plant_y = stand_y - 0.04
        plant_z = self.stand_elevation_z + self.stand_height
        self._create_potted_plant(bm, (plant_x, plant_y, plant_z), pot_mat, walnut_idx)

        return {
            "dome_lamps_count": 2,
            "has_tabletop_plant": True,
            "left_stand_origin": (left_x, stand_y, self.stand_elevation_z),
            "right_stand_origin": (right_x, stand_y, self.stand_elevation_z),
            "stand_top_z": self.stand_elevation_z + self.stand_height,
        }
