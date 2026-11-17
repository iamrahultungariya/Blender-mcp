"""Architectural Room Envelope, Acoustic Slat Feature Wall & Cove Ceiling.

Constructs the luxury bedroom spatial shell: oak parquet flooring, plush area rug,
vertical acoustic wood slat accent feature wall, and recessed ceiling cove LED tray.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
)
from luxury_bedroom.core.materials import MaterialLibrary


class RoomEnvelopeBuilder:
    """Builder for the room envelope, acoustic slat wall, cove ceiling, and rug."""

    def __init__(
        self,
        length: float = 4.80,
        width: float = 4.20,
        height: float = 2.85,
        slat_wall_width: float = 3.40,
        num_slats: int = 28,
        rug_width: float = 3.20,
        rug_length: float = 2.80,
    ) -> None:
        self.length = length
        self.width = width
        self.height = height
        self.slat_wall_width = slat_wall_width
        self.num_slats = num_slats
        self.rug_width = rug_width
        self.rug_length = rug_length

    def build(self, bm: Any, bed_datum: Dict[str, Any], mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct architectural room shell and accents into BMesh."""
        parquet_idx = mat_lib.get_index("PARQUET_OAK")
        rug_idx = mat_lib.get_index("LINEN_ACCENT")
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        plaster_idx = mat_lib.get_index("WARM_PLASTER")
        cove_idx = mat_lib.get_index("LED_WARM_COVE")

        head_center = bed_datum["headboard_center"]
        back_wall_y = head_center[1] + 0.12

        # 1. Finished Oak Parquet Flooring Slab
        create_beveled_box(
            bm,
            width=self.width,
            length=self.length,
            height=0.04,
            bevel_radius=0.005,
            segments=2,
            offset=(0.0, 0.0, -0.04),
            mat_index=parquet_idx,
        )

        # 2. Plush Area Rug Beneath Bed
        rug_y = head_center[1] - (self.rug_length / 2.0) - 0.20
        create_beveled_box(
            bm,
            width=self.rug_width,
            length=self.rug_length,
            height=0.015,
            bevel_radius=0.006,
            segments=2,
            offset=(0.0, rug_y, 0.001),
            mat_index=rug_idx,
        )

        # 3. Acoustic Wood Slat Feature Wall Behind Bed
        # Backing felt panel (Charcoal/Plaster)
        create_beveled_box(
            bm,
            width=self.slat_wall_width,
            length=0.02,
            height=self.height,
            bevel_radius=0.005,
            segments=2,
            offset=(0.0, back_wall_y, 0.0),
            mat_index=walnut_idx,
        )

        # Vertical walnut slats
        slat_spacing = self.slat_wall_width / max(1, self.num_slats)
        slat_w = slat_spacing * 0.65
        slat_d = 0.025
        slat_front_y = back_wall_y - (slat_d / 2.0)

        for i in range(self.num_slats):
            slat_x = -(self.slat_wall_width / 2.0) + (i + 0.5) * slat_spacing
            create_beveled_box(
                bm,
                width=slat_w,
                length=slat_d,
                height=self.height,
                bevel_radius=0.004,
                segments=2,
                offset=(slat_x, slat_front_y, 0.0),
                mat_index=walnut_idx,
            )

        # 4. Hidden Warm LED Uplight Strip along Slat Wall Base
        create_beveled_box(
            bm,
            width=self.slat_wall_width * 0.98,
            length=0.02,
            height=0.02,
            bevel_radius=0.002,
            segments=1,
            offset=(0.0, slat_front_y - 0.01, 0.005),
            mat_index=cove_idx,
        )

        # 5. Architectural Back Perimeter Drywall
        wall_thickness = 0.12
        create_beveled_box(
            bm,
            width=self.width,
            length=wall_thickness,
            height=self.height,
            bevel_radius=0.01,
            segments=2,
            offset=(0.0, back_wall_y + (wall_thickness / 2.0) + 0.01, 0.0),
            mat_index=plaster_idx,
        )

        # 6. Recessed Ceiling Tray with Warm LED Cove Lip
        # Ceiling main drop slab
        ceiling_drop_z = self.height - 0.12
        cove_tray_w = self.width * 0.75
        cove_tray_l = self.length * 0.75

        # Perimeter LED light trough
        create_beveled_box(
            bm,
            width=cove_tray_w,
            length=0.04,
            height=0.02,
            bevel_radius=0.003,
            segments=1,
            offset=(0.0, (cove_tray_l / 2.0), ceiling_drop_z),
            mat_index=cove_idx,
        )
        create_beveled_box(
            bm,
            width=cove_tray_w,
            length=0.04,
            height=0.02,
            bevel_radius=0.003,
            segments=1,
            offset=(0.0, -(cove_tray_l / 2.0), ceiling_drop_z),
            mat_index=cove_idx,
        )

        return {
            "room_dimensions": (self.width, self.length, self.height),
            "slat_wall_slats": self.num_slats,
            "rug_dimensions": (self.rug_width, self.rug_length),
            "ceiling_cove_active": True,
        }
