"""Hero Winged Bed Assembly with 6 Layered Pillows, Draped Duvet & Pleated Runner.

Direct procedural recreation of the reference hero bed from concept turnaround sheet:
- Segmented winged headboard (3 horizontal cushioned channels + angled wingback sides)
- Floating upholstered platform base with recessed shadow gap
- Contoured ergonomic mattress
- 6 Layered Pillows (2 sleeping white + 2 decorative charcoal + 2 lumbar taupe)
- White draped duvet with turned cuff
- Folded pleated charcoal bed runner draped across lower third
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_cushion_loft,
    create_draped_cloth_surface,
    create_pleated_surface,
)
from luxury_bedroom.core.materials import MaterialLibrary


class HeroBedBuilder:
    """Builder for the reference hero winged bed assembly."""

    def __init__(
        self,
        bed_width: float = 2.12,
        bed_length: float = 2.22,
        frame_height: float = 0.36,
        plinth_height: float = 0.12,
        plinth_recess: float = 0.14,
        headboard_width: float = 2.30,
        headboard_height: float = 1.25,
        headboard_depth: float = 0.12,
        mattress_thickness: float = 0.28,
        origin: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> None:
        self.bed_width = bed_width
        self.bed_length = bed_length
        self.frame_height = frame_height
        self.plinth_height = plinth_height
        self.plinth_recess = plinth_recess
        self.headboard_width = headboard_width
        self.headboard_height = headboard_height
        self.headboard_depth = headboard_depth
        self.mattress_thickness = mattress_thickness
        self.origin = origin

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct the complete hero bed assembly in memory."""
        ox, oy, oz = self.origin

        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")
        white_idx = mat_lib.get_index("LINEN_WHITE")
        charcoal_idx = mat_lib.get_index("CHARCOAL_PLEAT")

        # ----------------------------------------------------------------------
        # 1. Floating Base: Recessed Shadow-Gap Plinth
        # ----------------------------------------------------------------------
        plinth_w = max(0.4, self.bed_width - (2.0 * self.plinth_recess))
        plinth_l = max(0.4, self.bed_length - (2.0 * self.plinth_recess))
        create_beveled_box(
            bm,
            width=plinth_w,
            length=plinth_l,
            height=self.plinth_height,
            bevel_radius=0.01,
            segments=2,
            offset=(ox, oy, oz),
            mat_index=walnut_idx,
        )

        # ----------------------------------------------------------------------
        # 2. Main Upholstered Platform Bed Frame (Taupe Bouclé)
        # ----------------------------------------------------------------------
        platform_h = self.frame_height - self.plinth_height
        platform_z = oz + self.plinth_height
        create_beveled_box(
            bm,
            width=self.bed_width,
            length=self.bed_length,
            height=platform_h,
            bevel_radius=0.035,
            segments=3,
            offset=(ox, oy, platform_z),
            mat_index=boucle_idx,
        )

        # ----------------------------------------------------------------------
        # 3. Winged Segmented Headboard
        # ----------------------------------------------------------------------
        head_y = oy + (self.bed_length / 2.0) + (self.headboard_depth / 2.0)
        head_center = (ox, head_y, oz + (self.headboard_height / 2.0))

        # 3a. Central backboard structure
        create_beveled_box(
            bm,
            width=self.headboard_width,
            length=self.headboard_depth * 0.4,
            height=self.headboard_height,
            bevel_radius=0.015,
            segments=2,
            offset=(ox, head_y + (self.headboard_depth * 0.3), oz),
            mat_index=walnut_idx,
        )

        # 3b. 3 Horizontal Cushioned Channels (Taupe Bouclé)
        channel_count = 3
        channel_h = (self.headboard_height - 0.08) / channel_count
        channel_d = self.headboard_depth * 0.75

        for c_idx in range(channel_count):
            cz = oz + 0.04 + (c_idx * channel_h)
            create_cushion_loft(
                bm,
                width=self.headboard_width * 0.96,
                length=channel_d,
                height=channel_h * 0.95,
                crown=0.03,
                subdivisions_u=10,
                subdivisions_v=6,
                offset=(ox, head_y - (channel_d * 0.2), cz),
                mat_index=boucle_idx,
                tilt_deg_x=0.0,
            )

        # 3c. 2 Angled Wingback Side Panels
        wing_w = 0.14
        wing_d = 0.35
        wing_h = self.headboard_height
        wing_offset_x = (self.headboard_width / 2.0) + (wing_w / 2.0) - 0.02
        wing_y = head_y - (wing_d * 0.35)

        # Left wing panel
        create_beveled_box(
            bm,
            width=wing_w,
            length=wing_d,
            height=wing_h,
            bevel_radius=0.02,
            segments=2,
            offset=(-wing_offset_x, wing_y, oz),
            mat_index=boucle_idx,
        )
        # Right wing panel
        create_beveled_box(
            bm,
            width=wing_w,
            length=wing_d,
            height=wing_h,
            bevel_radius=0.02,
            segments=2,
            offset=(+wing_offset_x, wing_y, oz),
            mat_index=boucle_idx,
        )

        # ----------------------------------------------------------------------
        # 4. Contoured Ergonomic Mattress
        # ----------------------------------------------------------------------
        mattress_inset = 0.05
        mattress_w = self.bed_width - (2.0 * mattress_inset)
        mattress_l = self.bed_length - (2.0 * mattress_inset)
        mattress_base_z = oz + self.frame_height

        create_cushion_loft(
            bm,
            width=mattress_w,
            length=mattress_l,
            height=self.mattress_thickness,
            crown=0.035,
            subdivisions_u=12,
            subdivisions_v=12,
            offset=(ox, oy - mattress_inset * 0.5, mattress_base_z),
            mat_index=white_idx,
            tilt_deg_x=0.0,
        )

        mattress_top_z = mattress_base_z + self.mattress_thickness + 0.035

        # ----------------------------------------------------------------------
        # 5. 6-Pillow Luxury Arrangement (2 Sleeping + 2 Accent + 2 Lumbar)
        # ----------------------------------------------------------------------
        sp_y = head_y - 0.42
        sp_x_offset = mattress_w * 0.25
        pillow_z = mattress_top_z - 0.015

        # 5a. 2 Large Sleeping Pillows (White Linen, tilted 16°)
        create_cushion_loft(
            bm,
            width=0.82,
            length=0.48,
            height=0.17,
            crown=0.055,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox - sp_x_offset, sp_y, pillow_z),
            mat_index=white_idx,
            tilt_deg_x=16.0,
        )
        create_cushion_loft(
            bm,
            width=0.82,
            length=0.48,
            height=0.17,
            crown=0.055,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox + sp_x_offset, sp_y, pillow_z),
            mat_index=white_idx,
            tilt_deg_x=16.0,
        )

        # 5b. 2 Square Decorative Accent Pillows (Charcoal Pleated Fabric, tilted 11°)
        dp_y = sp_y - 0.32
        dp_x_offset = mattress_w * 0.23
        create_cushion_loft(
            bm,
            width=0.64,
            length=0.42,
            height=0.15,
            crown=0.045,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox - dp_x_offset, dp_y, pillow_z),
            mat_index=charcoal_idx,
            tilt_deg_x=11.0,
        )
        create_cushion_loft(
            bm,
            width=0.64,
            length=0.42,
            height=0.15,
            crown=0.045,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox + dp_x_offset, dp_y, pillow_z),
            mat_index=charcoal_idx,
            tilt_deg_x=11.0,
        )

        # 5c. 2 Front Lumbar Pillows (Taupe Bouclé, tilted 6°)
        lp_y = dp_y - 0.22
        lp_x_offset = mattress_w * 0.18
        create_cushion_loft(
            bm,
            width=0.46,
            length=0.28,
            height=0.11,
            crown=0.035,
            subdivisions_u=6,
            subdivisions_v=6,
            offset=(ox - lp_x_offset, lp_y, pillow_z),
            mat_index=boucle_idx,
            tilt_deg_x=6.0,
        )
        create_cushion_loft(
            bm,
            width=0.46,
            length=0.28,
            height=0.11,
            crown=0.035,
            subdivisions_u=6,
            subdivisions_v=6,
            offset=(ox + lp_x_offset, lp_y, pillow_z),
            mat_index=boucle_idx,
            tilt_deg_x=6.0,
        )

        # ----------------------------------------------------------------------
        # 6. Draped White Duvet with Turned Cuff
        # ----------------------------------------------------------------------
        chadar_w = mattress_w + 0.28
        chadar_l = mattress_l * 0.72
        foot_y = oy - (mattress_l / 2.0)
        chadar_center_y = foot_y + (chadar_l / 2.0) - 0.02
        chadar_z = mattress_top_z + 0.008

        create_draped_cloth_surface(
            bm,
            width=chadar_w,
            length=chadar_l,
            drape_drop=0.18,
            folds_freq=4.0,
            folds_amp=0.015,
            subdivisions_x=16,
            subdivisions_y=16,
            offset=(ox, chadar_center_y, chadar_z),
            mat_index=white_idx,
            cuff_length=0.26,
            cuff_mat_index=white_idx,
        )

        # ----------------------------------------------------------------------
        # 7. Pleated Charcoal Bed Runner Draped Across Lower Third
        # ----------------------------------------------------------------------
        runner_w = mattress_w + 0.32
        runner_l = 0.58
        runner_y = foot_y + (runner_l / 2.0) + 0.20
        runner_z = chadar_z + 0.015

        create_pleated_surface(
            bm,
            width=runner_w,
            length=runner_l,
            pleat_freq=10.0,
            pleat_amp=0.012,
            subdivisions_x=24,
            subdivisions_y=12,
            offset=(ox, runner_y, runner_z),
            mat_index=charcoal_idx,
            along_axis="X",
        )

        return {
            "bed_width": self.bed_width,
            "bed_length": self.bed_length,
            "headboard_center": head_center,
            "mattress_top_z": mattress_top_z,
            "pillows_count": 6,
            "pillows_breakdown": {
                "sleeping": 2,
                "accent": 2,
                "lumbar": 2,
            },
            "has_winged_headboard": True,
            "has_bed_runner": True,
            "bed_datum": {
                "mattress_top_z": mattress_top_z,
                "headboard_center": head_center,
                "bed_width": self.bed_width,
                "bed_length": self.bed_length,
                "mattress_origin": (ox, oy, mattress_base_z),
                "mattress_dimensions": (mattress_w, mattress_l, self.mattress_thickness),
            }
        }
