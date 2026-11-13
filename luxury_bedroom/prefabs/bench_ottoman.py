"""End-of-Bed Upholstered Ottoman Bench with Rounded Double Cushion.

Direct procedural recreation of the ottoman bench from the reference turnaround sheet:
- Long rectangular bench centered at the foot of the bed
- Split into 2 soft crowned cushions in taupe bouclé fabric
- Dark recessed hardwood plinth base with shadow gap
"""
from __future__ import annotations

from typing import Any, Dict, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_cushion_loft,
)
from luxury_bedroom.core.materials import MaterialLibrary


class OttomanBenchBuilder:
    """Builder for the upholstered end-of-bed bench."""

    def __init__(
        self,
        bench_width: float = 1.38,
        bench_depth: float = 0.46,
        total_height: float = 0.44,
        plinth_height: float = 0.12,
        plinth_recess: float = 0.05,
        bed_clearance_gap: float = 0.14,
    ) -> None:
        self.bench_width = bench_width
        self.bench_depth = bench_depth
        self.total_height = total_height
        self.plinth_height = plinth_height
        self.plinth_recess = plinth_recess
        self.bed_clearance_gap = bed_clearance_gap

    def build(self, bm: Any, bed_datum: Dict[str, Any], mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct the end-of-bed bench into the BMesh buffer."""
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")

        bed_l = bed_datum["bed_length"]
        head_center = bed_datum["headboard_center"]
        bed_center_x = head_center[0]

        # Calculate foot-of-bed position
        foot_y = head_center[1] - bed_l - 0.08
        bench_center_y = foot_y - (self.bench_depth / 2.0) - self.bed_clearance_gap

        # 1. Recessed Hardwood Plinth Base
        plinth_w = self.bench_width - (2.0 * self.plinth_recess)
        plinth_d = self.bench_depth - (2.0 * self.plinth_recess)
        create_beveled_box(
            bm,
            width=plinth_w,
            length=plinth_d,
            height=self.plinth_height,
            bevel_radius=0.01,
            segments=2,
            offset=(bed_center_x, bench_center_y, 0.0),
            mat_index=walnut_idx,
        )

        # 2. Lower Upholstered Support Deck
        deck_h = 0.08
        deck_z = self.plinth_height
        create_beveled_box(
            bm,
            width=self.bench_width,
            length=self.bench_depth,
            height=deck_h,
            bevel_radius=0.02,
            segments=2,
            offset=(bed_center_x, bench_center_y, deck_z),
            mat_index=boucle_idx,
        )

        # 3. Two Rounded Padded Cushions (Split Left and Right)
        cushion_h = self.total_height - (deck_z + deck_h)
        cushion_w = (self.bench_width * 0.485)
        cushion_d = self.bench_depth * 0.96
        cushion_z = deck_z + deck_h

        left_cushion_x = bed_center_x - (self.bench_width * 0.25)
        right_cushion_x = bed_center_x + (self.bench_width * 0.25)

        # Left Cushion
        create_cushion_loft(
            bm,
            width=cushion_w,
            length=cushion_d,
            height=cushion_h,
            crown=0.035,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(left_cushion_x, bench_center_y, cushion_z),
            mat_index=boucle_idx,
            tilt_deg_x=0.0,
        )

        # Right Cushion
        create_cushion_loft(
            bm,
            width=cushion_w,
            length=cushion_d,
            height=cushion_h,
            crown=0.035,
            subdivisions_u=8,
            subdivisions_v=8,
            offset=(right_cushion_x, bench_center_y, cushion_z),
            mat_index=boucle_idx,
            tilt_deg_x=0.0,
        )

        return {
            "bench_placed": True,
            "cushions_count": 2,
            "bench_origin": (bed_center_x, bench_center_y, 0.0),
            "bench_dimensions": (self.bench_width, self.bench_depth, self.total_height),
        }
