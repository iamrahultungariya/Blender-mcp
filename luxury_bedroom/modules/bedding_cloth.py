"""High-Realism Bedding System: Layered Pillows & Draped Chadar (Duvet).

Constructs multi-layered organic pillows with parabolic lofting, seams, and tilt,
paired with a physically convincing draped blanket (chadar) featuring sinusoidal
wrinkle ripples, side overhang drape, and turned-down cuff fold.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_cushion_loft,
    create_draped_cloth_surface,
)
from luxury_bedroom.core.materials import MaterialLibrary


class BeddingClothBuilder:
    """Builder for realistic multi-layered pillows and draped bedsheet/chadar."""

    def __init__(
        self,
        sleeping_pillow_size: Tuple[float, float, float] = (0.78, 0.48, 0.16),
        decorative_pillow_size: Tuple[float, float, float] = (0.62, 0.40, 0.14),
        lumbar_cushion_size: Tuple[float, float, float] = (0.50, 0.28, 0.11),
        chadar_coverage_ratio: float = 0.72,
        chadar_overhang: float = 0.14,
        cuff_length: float = 0.25,
    ) -> None:
        self.sleeping_pillow_size = sleeping_pillow_size
        self.decorative_pillow_size = decorative_pillow_size
        self.lumbar_cushion_size = lumbar_cushion_size
        self.chadar_coverage_ratio = chadar_coverage_ratio
        self.chadar_overhang = chadar_overhang
        self.cuff_length = cuff_length

    def build(self, bm: Any, bed_datum: Dict[str, Any], mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct realistic layered pillows and draped chadar in memory."""
        white_idx = mat_lib.get_index("LINEN_WHITE")
        accent_idx = mat_lib.get_index("LINEN_ACCENT")
        velvet_idx = mat_lib.get_index("UPHOLSTERY_VELVET")

        mattress_top_z = bed_datum["mattress_top_z"]
        head_center = bed_datum["headboard_center"]
        mattress_w, mattress_l, mattress_h = bed_datum["mattress_dimensions"]
        ox, oy, _ = bed_datum["mattress_origin"]

        # ----------------------------------------------------------------------
        # 1. Layer 1: Two Large Structural Sleeping Pillows (White Linen)
        # ----------------------------------------------------------------------
        sp_w, sp_l, sp_h = self.sleeping_pillow_size
        sp_y = head_center[1] - 0.42
        sp_x_offset = mattress_w * 0.24
        pillow_base_z = mattress_top_z - 0.02  # slight physical compression into mattress

        # Left sleeping pillow
        create_cushion_loft(
            bm,
            width=sp_w,
            length=sp_l,
            height=sp_h,
            crown=0.05,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox - sp_x_offset, sp_y, pillow_base_z),
            mat_index=white_idx,
            tilt_deg_x=16.0,
        )

        # Right sleeping pillow
        create_cushion_loft(
            bm,
            width=sp_w,
            length=sp_l,
            height=sp_h,
            crown=0.05,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox + sp_x_offset, sp_y, pillow_base_z),
            mat_index=white_idx,
            tilt_deg_x=16.0,
        )

        # ----------------------------------------------------------------------
        # 2. Layer 2: Two Decorative Front Accent Pillows (Warm Accent Linen)
        # ----------------------------------------------------------------------
        dp_w, dp_l, dp_h = self.decorative_pillow_size
        dp_y = sp_y - 0.30
        dp_x_offset = mattress_w * 0.22

        create_cushion_loft(
            bm,
            width=dp_w,
            length=dp_l,
            height=dp_h,
            crown=0.04,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox - dp_x_offset, dp_y, pillow_base_z),
            mat_index=accent_idx,
            tilt_deg_x=10.0,
        )

        create_cushion_loft(
            bm,
            width=dp_w,
            length=dp_l,
            height=dp_h,
            crown=0.04,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(ox + dp_x_offset, dp_y, pillow_base_z),
            mat_index=accent_idx,
            tilt_deg_x=10.0,
        )

        # ----------------------------------------------------------------------
        # 3. Layer 3: Center Lumbar Velvet Cushion (Matching Headboard Velvet)
        # ----------------------------------------------------------------------
        lp_w, lp_l, lp_h = self.lumbar_cushion_size
        lp_y = dp_y - 0.16

        create_cushion_loft(
            bm,
            width=lp_w,
            length=lp_l,
            height=lp_h,
            crown=0.035,
            subdivisions_u=6,
            subdivisions_v=6,
            offset=(ox, lp_y, pillow_base_z),
            mat_index=velvet_idx,
            tilt_deg_x=5.0,
        )

        # ----------------------------------------------------------------------
        # 4. Chadar / Duvet (Naturally Draped Blanket with Folds & Turned Cuff)
        # ----------------------------------------------------------------------
        chadar_w = mattress_w + (2.0 * self.chadar_overhang)
        chadar_l = mattress_l * self.chadar_coverage_ratio
        # Position chadar covering foot up to the decorative pillows
        foot_y = oy - (mattress_l / 2.0)
        chadar_center_y = foot_y + (chadar_l / 2.0) - 0.02
        chadar_z = mattress_top_z + 0.008  # draped directly on top of mattress

        create_draped_cloth_surface(
            bm,
            width=chadar_w,
            length=chadar_l,
            drape_drop=0.16,
            folds_freq=4.0,
            folds_amp=0.014,
            subdivisions_x=16,
            subdivisions_y=16,
            offset=(ox, chadar_center_y, chadar_z),
            mat_index=accent_idx,
            cuff_length=self.cuff_length,
            cuff_mat_index=white_idx,
        )

        return {
            "pillows_count": 5,
            "pillow_base_z": pillow_base_z,
            "chadar_draped": True,
            "chadar_bounds": {
                "width": chadar_w,
                "length": chadar_l,
                "center": (ox, chadar_center_y, chadar_z),
                "cuff_length": self.cuff_length,
            },
        }
