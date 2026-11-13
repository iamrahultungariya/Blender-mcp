"""Media Wall: Floating Low-Profile Credenza, Wall-Mounted 65" TV & Decor.

Direct procedural recreation of the media wall from the reference turnaround sheet:
- Long floating 3-section media credenza in warm walnut with brass reveals
- Under-cabinet warm ambient LED glow
- Wall-mounted ultra-slim 65" flat screen TV with beveled border
- Tabletop decorative vase and cascading shelf plant
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple
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


class MediaWallBuilder:
    """Builder for the floating media credenza and wall-mounted TV."""

    def __init__(
        self,
        wall_y: float = -2.10,
        credenza_width: float = 2.60,
        credenza_depth: float = 0.40,
        credenza_height: float = 0.38,
        credenza_elevation_z: float = 0.22,
        tv_width: float = 1.45,
        tv_height: float = 0.84,
        tv_depth: float = 0.04,
        tv_center_z: float = 1.38,
    ) -> None:
        self.wall_y = wall_y
        self.credenza_width = credenza_width
        self.credenza_depth = credenza_depth
        self.credenza_height = credenza_height
        self.credenza_elevation_z = credenza_elevation_z
        self.tv_width = tv_width
        self.tv_height = tv_height
        self.tv_depth = tv_depth
        self.tv_center_z = tv_center_z

    def _create_cascading_plant(
        self,
        bm: Any,
        center: Tuple[float, float, float],
        pot_mat: int,
        leaf_mat: int,
    ) -> None:
        """Create a planter pot with trailing cascading vine leaves over the credenza front."""
        cx, cy, cz = center

        # Small ceramic pot
        pot_profile = [(0.06, 0.0), (0.07, 0.03), (0.07, 0.10), (0.065, 0.10)]
        create_lathe_mesh(bm, pot_profile, segs=16, center=(cx, cy, cz), mat_index=pot_mat)

        # 4 cascading vine runners trailing down the front of the credenza
        for v_idx in range(4):
            vx_offset = (v_idx - 1.5) * 0.045
            for step in range(5):
                t = step / 5.0
                leaf_z = cz + 0.08 - (t * 0.28)  # trails downwards
                leaf_y = cy - 0.06 - (t * 0.04)
                leaf_x = cx + vx_offset + math.sin(t * 3.0) * 0.02

                create_beveled_box(
                    bm,
                    width=0.035,
                    length=0.03,
                    height=0.008,
                    bevel_radius=0.002,
                    segments=1,
                    offset=(leaf_x, leaf_y, leaf_z),
                    mat_index=leaf_mat,
                )

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct the media credenza and wall-mounted TV into the BMesh buffer."""
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        brass_idx = mat_lib.get_index("BRUSHED_BRASS")
        black_idx = mat_lib.get_index("MATTE_BLACK_METAL")
        led_idx = mat_lib.get_index("LED_WARM_2700K")
        pot_mat = mat_lib.get_index("TAUPE_BOUCLE")

        credenza_center_y = self.wall_y + (self.credenza_depth / 2.0)

        # 1. Main Floating Credenza Carcass (Walnut Wood)
        create_beveled_box(
            bm,
            width=self.credenza_width,
            length=self.credenza_depth,
            height=self.credenza_height,
            bevel_radius=0.015,
            segments=2,
            offset=(0.0, credenza_center_y, self.credenza_elevation_z),
            mat_index=walnut_idx,
        )

        # 2. 3 Drawer Fronts with Horizontal Brass Trim Channel
        num_sections = 3
        section_w = (self.credenza_width - 0.06) / num_sections
        front_y = credenza_center_y - (self.credenza_depth / 2.0) - 0.006

        for i in range(num_sections):
            sec_x = -(self.credenza_width / 2.0) + 0.03 + (i + 0.5) * section_w
            create_beveled_box(
                bm,
                width=section_w * 0.96,
                length=0.015,
                height=self.credenza_height * 0.88,
                bevel_radius=0.006,
                segments=2,
                offset=(sec_x, front_y, self.credenza_elevation_z + (self.credenza_height * 0.06)),
                mat_index=walnut_idx,
            )

        # Brass edge reveal along top edge
        create_beveled_box(
            bm,
            width=self.credenza_width * 0.99,
            length=0.015,
            height=0.012,
            bevel_radius=0.003,
            segments=1,
            offset=(0.0, front_y, self.credenza_elevation_z + self.credenza_height - 0.015),
            mat_index=brass_idx,
        )

        # 3. Under-Credenza Warm LED Glow Strip
        create_beveled_box(
            bm,
            width=self.credenza_width * 0.92,
            length=self.credenza_depth * 0.70,
            height=0.01,
            bevel_radius=0.002,
            segments=1,
            offset=(0.0, credenza_center_y, self.credenza_elevation_z - 0.012),
            mat_index=led_idx,
        )

        # 4. Wall-Mounted Slim 65" TV Display
        tv_y = self.wall_y + (self.tv_depth / 2.0) + 0.015
        # Outer bezel
        create_beveled_box(
            bm,
            width=self.tv_width,
            length=self.tv_depth,
            height=self.tv_height,
            bevel_radius=0.006,
            segments=2,
            offset=(0.0, tv_y, self.tv_center_z - (self.tv_height / 2.0)),
            mat_index=black_idx,
        )
        # Inner glossy dark display panel
        create_beveled_box(
            bm,
            width=self.tv_width * 0.97,
            length=0.005,
            height=self.tv_height * 0.95,
            bevel_radius=0.002,
            segments=1,
            offset=(0.0, tv_y - (self.tv_depth / 2.0) - 0.003, self.tv_center_z - (self.tv_height / 2.0) + 0.02),
            mat_index=black_idx,
        )

        # 5. Cascading Greenery on Right Edge of Credenza
        plant_x = (self.credenza_width / 2.0) - 0.25
        plant_y = credenza_center_y - 0.05
        plant_z = self.credenza_elevation_z + self.credenza_height
        self._create_cascading_plant(bm, (plant_x, plant_y, plant_z), pot_mat, walnut_idx)

        # Calculate diagonal in inches: sqrt(w^2 + h^2) in meters / 0.0254
        diag_inches = math.sqrt(self.tv_width**2 + self.tv_height**2) / 0.0254

        return {
            "credenza_placed": True,
            "tv_mounted": True,
            "credenza_width": self.credenza_width,
            "tv_screen_diagonal_inches": diag_inches,
            "credenza_top_z": self.credenza_elevation_z + self.credenza_height,
            "tv_center": (0.0, tv_y, self.tv_center_z),
        }
