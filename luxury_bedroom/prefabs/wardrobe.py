"""Wardrobe: Full-Height 4-Door Bronze Glass & Walnut Wardrobe.

Direct procedural recreation of the luxury wardrobe from the reference turnaround sheet:
- Full-height casework situated along the right wall
- Dark walnut outer carcass, bottom plinth, and top soffit/header
- 4 full-length doors with tinted bronze glass panels and slim walnut/brass stiles
- Brushed brass vertical recessed pull handles
- Internal lit shelving sections, vertical dividers, and horizontal clothes hanger rod
- Warm interior LED illumination (2700K)
"""
from __future__ import annotations

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


class WardrobeBuilder:
    """Builder for the luxury full-height wardrobe."""

    def __init__(
        self,
        wall_x: float = 2.50,
        center_y: float = 0.20,
        wardrobe_width_y: float = 2.40,
        wardrobe_depth_x: float = 0.65,
        wardrobe_height: float = 2.65,
        plinth_height: float = 0.08,
        header_height: float = 0.08,
        num_doors: int = 4,
    ) -> None:
        self.wall_x = wall_x
        self.center_y = center_y
        self.wardrobe_width_y = wardrobe_width_y
        self.wardrobe_depth_x = wardrobe_depth_x
        self.wardrobe_height = wardrobe_height
        self.plinth_height = plinth_height
        self.header_height = header_height
        self.num_doors = num_doors

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct the wardrobe assembly into the BMesh buffer."""
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        brass_idx = mat_lib.get_index("BRUSHED_BRASS")
        glass_idx = mat_lib.get_index("TINTED_BRONZE_GLASS")
        led_idx = mat_lib.get_index("LED_WARM_2700K")
        black_idx = mat_lib.get_index("MATTE_BLACK_METAL")

        # Center X of the wardrobe body (facing into the room in -X direction)
        carcass_center_x = self.wall_x - (self.wardrobe_depth_x / 2.0)
        front_x = self.wall_x - self.wardrobe_depth_x

        # 1. Main Carcass Shell (Outer top, bottom, back, sides)
        # Back panel (flush with wall)
        create_beveled_box(
            bm,
            width=0.02,
            length=self.wardrobe_width_y,
            height=self.wardrobe_height,
            bevel_radius=0.003,
            segments=1,
            offset=(self.wall_x - 0.01, self.center_y, 0.0),
            mat_index=walnut_idx,
        )

        # Bottom Plinth / Baseboard
        create_beveled_box(
            bm,
            width=self.wardrobe_depth_x,
            length=self.wardrobe_width_y,
            height=self.plinth_height,
            bevel_radius=0.004,
            segments=1,
            offset=(carcass_center_x, self.center_y, 0.0),
            mat_index=walnut_idx,
        )

        # Top Header / Soffit
        create_beveled_box(
            bm,
            width=self.wardrobe_depth_x,
            length=self.wardrobe_width_y,
            height=self.header_height,
            bevel_radius=0.004,
            segments=1,
            offset=(carcass_center_x, self.center_y, self.wardrobe_height - self.header_height),
            mat_index=walnut_idx,
        )

        # Left Outer Gable End (Side Panel)
        create_beveled_box(
            bm,
            width=self.wardrobe_depth_x,
            length=0.03,
            height=self.wardrobe_height - self.plinth_height - self.header_height,
            bevel_radius=0.004,
            segments=1,
            offset=(
                carcass_center_x,
                self.center_y - (self.wardrobe_width_y / 2.0) + 0.015,
                self.plinth_height,
            ),
            mat_index=walnut_idx,
        )

        # Right Outer Gable End (Side Panel)
        create_beveled_box(
            bm,
            width=self.wardrobe_depth_x,
            length=0.03,
            height=self.wardrobe_height - self.plinth_height - self.header_height,
            bevel_radius=0.004,
            segments=1,
            offset=(
                carcass_center_x,
                self.center_y + (self.wardrobe_width_y / 2.0) - 0.015,
                self.plinth_height,
            ),
            mat_index=walnut_idx,
        )

        # 2. Internal Partition Walls & Shelving
        # 3 internal vertical partition dividers separating into 4 bays
        internal_height = self.wardrobe_height - self.plinth_height - self.header_height
        bay_width = (self.wardrobe_width_y - 0.06) / self.num_doors
        start_y = self.center_y - (self.wardrobe_width_y / 2.0) + 0.03

        for i in range(1, self.num_doors):
            divider_y = start_y + (i * bay_width)
            create_beveled_box(
                bm,
                width=self.wardrobe_depth_x - 0.05,
                length=0.02,
                height=internal_height,
                bevel_radius=0.003,
                segments=1,
                offset=(carcass_center_x + 0.02, divider_y, self.plinth_height),
                mat_index=walnut_idx,
            )

        # Internal Horizontal Shelves and LED strip for each bay
        for b in range(self.num_doors):
            bay_center_y = start_y + (b + 0.5) * bay_width

            # Top Hat Shelf
            shelf_z1 = self.plinth_height + internal_height * 0.75
            create_beveled_box(
                bm,
                width=self.wardrobe_depth_x - 0.06,
                length=bay_width - 0.01,
                height=0.02,
                bevel_radius=0.003,
                segments=1,
                offset=(carcass_center_x + 0.02, bay_center_y, shelf_z1),
                mat_index=walnut_idx,
            )

            # Warm LED strip under top shelf
            create_beveled_box(
                bm,
                width=0.02,
                length=bay_width - 0.04,
                height=0.008,
                bevel_radius=0.002,
                segments=1,
                offset=(carcass_center_x + 0.02, bay_center_y, shelf_z1 - 0.01),
                mat_index=led_idx,
            )

            # Lower shelf
            shelf_z2 = self.plinth_height + internal_height * 0.25
            create_beveled_box(
                bm,
                width=self.wardrobe_depth_x - 0.06,
                length=bay_width - 0.01,
                height=0.02,
                bevel_radius=0.003,
                segments=1,
                offset=(carcass_center_x + 0.02, bay_center_y, shelf_z2),
                mat_index=walnut_idx,
            )

            # Hanging Rod (Metal Tube)
            rod_z = shelf_z1 - 0.06
            create_beveled_box(
                bm,
                width=0.018,
                length=bay_width - 0.02,
                height=0.018,
                bevel_radius=0.006,
                segments=2,
                offset=(carcass_center_x + 0.04, bay_center_y, rod_z),
                mat_index=black_idx,
            )

        # 3. 4 Full-Height Bronze Glass Doors with Walnut Perimeter and Brass Handles
        door_clearance = 0.004
        door_height = internal_height - (door_clearance * 2.0)
        door_y_size = bay_width - door_clearance

        for d in range(self.num_doors):
            door_center_y = start_y + (d + 0.5) * bay_width
            door_front_x = front_x + 0.01

            # Door Frame Perimeter (Slim Walnut Stiles & Rails)
            frame_th = 0.04
            # Top rail
            create_beveled_box(
                bm,
                width=0.02,
                length=door_y_size,
                height=frame_th,
                bevel_radius=0.003,
                segments=1,
                offset=(
                    door_front_x,
                    door_center_y,
                    self.plinth_height + door_clearance + door_height - frame_th,
                ),
                mat_index=walnut_idx,
            )
            # Bottom rail
            create_beveled_box(
                bm,
                width=0.02,
                length=door_y_size,
                height=frame_th,
                bevel_radius=0.003,
                segments=1,
                offset=(
                    door_front_x,
                    door_center_y,
                    self.plinth_height + door_clearance,
                ),
                mat_index=walnut_idx,
            )
            # Left stile
            create_beveled_box(
                bm,
                width=0.02,
                length=frame_th,
                height=door_height,
                bevel_radius=0.003,
                segments=1,
                offset=(
                    door_front_x,
                    door_center_y - (door_y_size / 2.0) + (frame_th / 2.0),
                    self.plinth_height + door_clearance,
                ),
                mat_index=walnut_idx,
            )
            # Right stile
            create_beveled_box(
                bm,
                width=0.02,
                length=frame_th,
                height=door_height,
                bevel_radius=0.003,
                segments=1,
                offset=(
                    door_front_x,
                    door_center_y + (door_y_size / 2.0) - (frame_th / 2.0),
                    self.plinth_height + door_clearance,
                ),
                mat_index=walnut_idx,
            )

            # Central Tinted Bronze Glass Panel
            create_beveled_box(
                bm,
                width=0.008,
                length=door_y_size - (frame_th * 1.8),
                height=door_height - (frame_th * 1.8),
                bevel_radius=0.002,
                segments=1,
                offset=(
                    door_front_x,
                    door_center_y,
                    self.plinth_height + door_clearance + (frame_th * 0.9),
                ),
                mat_index=glass_idx,
            )

            # Elegant Vertical Brushed Brass Slim Handle
            # Position handle along the inner edge of each pair of doors
            handle_offset_y = (
                (door_y_size / 2.0) - 0.05 if (d % 2 == 0) else -(door_y_size / 2.0) + 0.05
            )
            handle_z = self.plinth_height + (door_height / 2.0) - 0.25
            create_beveled_box(
                bm,
                width=0.015,
                length=0.012,
                height=0.50,
                bevel_radius=0.003,
                segments=1,
                offset=(door_front_x - 0.015, door_center_y + handle_offset_y, handle_z),
                mat_index=brass_idx,
            )

        return {
            "wardrobe_placed": True,
            "doors_count": self.num_doors,
            "wardrobe_width": self.wardrobe_width_y,
            "wardrobe_depth": self.wardrobe_depth_x,
            "wardrobe_height": self.wardrobe_height,
            "front_x": front_x,
        }
