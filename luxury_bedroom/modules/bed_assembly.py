"""Modular Hero Bed Frame, Fluted Headboard & Mattress Assembly.

Constructs an Italian-inspired low-profile floating platform king bed with
a vertical fluted velvet headboard and multi-layer contoured mattress.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_cushion_loft,
    create_fluted_panel,
)
from luxury_bedroom.core.materials import MaterialLibrary


class BedAssemblyBuilder:
    """Builder for floating platform bed frame, fluted headboard, and mattress."""

    def __init__(
        self,
        width: float = 2.04,
        length: float = 2.14,
        frame_height: float = 0.32,
        plinth_recess: float = 0.12,
        plinth_height: float = 0.10,
        headboard_width: float = 2.40,
        headboard_height: float = 1.30,
        headboard_depth: float = 0.08,
        num_flutes: int = 12,
        mattress_thickness: float = 0.28,
        origin: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> None:
        self.width = width
        self.length = length
        self.frame_height = frame_height
        self.plinth_recess = plinth_recess
        self.plinth_height = plinth_height
        self.headboard_width = headboard_width
        self.headboard_height = headboard_height
        self.headboard_depth = headboard_depth
        self.num_flutes = num_flutes
        self.mattress_thickness = mattress_thickness
        self.origin = origin

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct bed assemblies in memory inside the provided BMesh buffer."""
        ox, oy, oz = self.origin
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        velvet_idx = mat_lib.get_index("UPHOLSTERY_VELVET")
        linen_idx = mat_lib.get_index("LINEN_WHITE")

        # 1. Floating Recessed Plinth (creates floating shadow-gap look)
        plinth_w = max(0.2, self.width - 2.0 * self.plinth_recess)
        plinth_l = max(0.2, self.length - 2.0 * self.plinth_recess)
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

        # 2. Main Hardwood Platform Frame
        platform_h = self.frame_height - self.plinth_height
        create_beveled_box(
            bm,
            width=self.width,
            length=self.length,
            height=platform_h,
            bevel_radius=0.02,
            segments=3,
            offset=(ox, oy, oz + self.plinth_height),
            mat_index=walnut_idx,
        )

        # 3. Fluted Velvet Upholstered Headboard
        head_y = oy + (self.length / 2.0) + (self.headboard_depth / 2.0)
        headboard_center = (ox, head_y, oz + (self.headboard_height / 2.0))
        create_fluted_panel(
            bm,
            width=self.headboard_width,
            height=self.headboard_height,
            depth=self.headboard_depth,
            num_flutes=self.num_flutes,
            flute_radius=0.018,
            offset=(ox, head_y, oz),
            mat_index=velvet_idx,
        )

        # 4. Ergonomic Mattress with Beveled Edges & Subtle Crown
        mattress_inset = 0.04
        mattress_w = self.width - (2.0 * mattress_inset)
        mattress_l = self.length - (2.0 * mattress_inset)
        mattress_base_z = oz + self.frame_height

        create_cushion_loft(
            bm,
            width=mattress_w,
            length=mattress_l,
            height=self.mattress_thickness,
            crown=0.025,
            subdivisions_u=10,
            subdivisions_v=10,
            offset=(ox, oy, mattress_base_z),
            mat_index=linen_idx,
            tilt_deg_x=0.0,
        )

        mattress_top_z = mattress_base_z + self.mattress_thickness + 0.025

        return {
            "bed_width": self.width,
            "bed_length": self.length,
            "frame_height": self.frame_height,
            "mattress_top_z": mattress_top_z,
            "headboard_center": headboard_center,
            "headboard_width": self.headboard_width,
            "headboard_height": self.headboard_height,
            "mattress_origin": (ox, oy, mattress_base_z),
            "mattress_dimensions": (mattress_w, mattress_l, self.mattress_thickness),
        }
