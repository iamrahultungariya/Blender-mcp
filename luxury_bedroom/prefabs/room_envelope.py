"""Room Envelope: Architectural Walls, Travertine Floor, Cove Ceiling, Fluted Accent Wall & Artwork.

Direct procedural recreation of the architectural shell from the reference turnaround sheet:
- Travertine floor tiles with physical grout grooves and subtle surface variation
- Large plush woven area rug centered beneath the hero bed and extending past the ottoman bench
- Feature headboard accent wall:
  - Dual fluted vertical walnut acoustic slat panel sections (left and right)
  - Recessed warm-grey center wall panel
  - Twin vertical floor-to-ceiling recessed warm LED glow channels (2700K)
  - Horizontal framed panoramic mountain landscape artwork with beveled frame
- Architectural solid walls with deep window and door reveals
- Dropped false ceiling with recessed tray and continuous indirect warm LED cove lighting trough
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_fluted_panel,
    create_cushion_loft,
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


class RoomEnvelopeBuilder:
    """Builder for the room envelope, floor, ceiling cove, and architectural accent wall."""

    def __init__(
        self,
        room_width_x: float = 5.20,
        room_length_y: float = 5.80,
        room_height_z: float = 2.85,
        wall_thickness: float = 0.20,
        ceiling_drop: float = 0.18,
        cove_inset: float = 0.65,
    ) -> None:
        self.room_width_x = room_width_x
        self.room_length_y = room_length_y
        self.room_height_z = room_height_z
        self.wall_thickness = wall_thickness
        self.ceiling_drop = ceiling_drop
        self.cove_inset = cove_inset

    def _build_tiled_floor(
        self,
        bm: Any,
        mat_index: int,
        tile_size: float = 0.80,
        grout_gap: float = 0.005,
    ) -> None:
        """Create floor composed of individual beveled travertine tiles with physical grout spacing."""
        nx = int(math.ceil(self.room_width_x / tile_size))
        ny = int(math.ceil(self.room_length_y / tile_size))
        actual_tx = self.room_width_x / nx
        actual_ty = self.room_length_y / ny

        for i in range(nx):
            x_c = -(self.room_width_x / 2.0) + (i + 0.5) * actual_tx
            for j in range(ny):
                y_c = -(self.room_length_y / 2.0) + (j + 0.5) * actual_ty
                create_beveled_box(
                    bm,
                    width=actual_tx - grout_gap,
                    length=actual_ty - grout_gap,
                    height=0.03,
                    bevel_radius=0.003,
                    segments=1,
                    offset=(x_c, y_c, -0.03),
                    mat_index=mat_index,
                )

    def _build_accent_headboard_wall(
        self,
        bm: Any,
        mat_lib: MaterialLibrary,
        back_wall_y: float,
    ) -> None:
        """Create the luxury fluted wood accent wall behind the bed with vertical LED channels and mountain artwork."""
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")
        boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")
        brass_idx = mat_lib.get_index("BRUSHED_BRASS")
        led_idx = mat_lib.get_index("LED_WARM_2700K")
        black_idx = mat_lib.get_index("MATTE_BLACK_METAL")

        wall_h = self.room_height_z - self.ceiling_drop
        center_panel_w = 2.40
        flute_section_w = (self.room_width_x - center_panel_w - 0.20) / 2.0

        # 1. Left Fluted Wood Slat Section (28 vertical slats)
        left_center_x = -(center_panel_w / 2.0) - (flute_section_w / 2.0) - 0.05
        create_fluted_panel(
            bm,
            width=flute_section_w,
            height=wall_h,
            depth=0.04,
            num_flutes=28,
            flute_radius=0.012,
            offset=(left_center_x, back_wall_y - 0.02, 0.0),
            mat_index=walnut_idx,
        )

        # 2. Right Fluted Wood Slat Section (28 vertical slats)
        right_center_x = (center_panel_w / 2.0) + (flute_section_w / 2.0) + 0.05
        create_fluted_panel(
            bm,
            width=flute_section_w,
            height=wall_h,
            depth=0.04,
            num_flutes=28,
            flute_radius=0.012,
            offset=(right_center_x, back_wall_y - 0.02, 0.0),
            mat_index=walnut_idx,
        )

        # 3. Recessed Center Warm-Grey Wall Panel
        create_beveled_box(
            bm,
            width=center_panel_w,
            length=0.02,
            height=wall_h,
            bevel_radius=0.005,
            segments=1,
            offset=(0.0, back_wall_y + 0.01, 0.0),
            mat_index=boucle_idx,
        )

        # 4. Twin Vertical Floor-to-Ceiling Warm LED Light Channels
        chan_w = 0.035
        chan_d = 0.025
        # Left vertical LED channel
        create_beveled_box(
            bm,
            width=chan_w,
            length=chan_d,
            height=wall_h,
            bevel_radius=0.002,
            segments=1,
            offset=(-(center_panel_w / 2.0) - (chan_w / 2.0), back_wall_y - 0.01, 0.0),
            mat_index=led_idx,
        )
        # Right vertical LED channel
        create_beveled_box(
            bm,
            width=chan_w,
            length=chan_d,
            height=wall_h,
            bevel_radius=0.002,
            segments=1,
            offset=((center_panel_w / 2.0) + (chan_w / 2.0), back_wall_y - 0.01, 0.0),
            mat_index=led_idx,
        )

        # 5. Framed Mountain Landscape Artwork centered above bed
        art_w = 1.45
        art_h = 0.75
        art_center_z = 1.85
        art_frame_th = 0.035
        art_y = back_wall_y + 0.005

        # Outer Dark Wood Beveled Picture Frame
        create_beveled_box(
            bm,
            width=art_w,
            length=0.025,
            height=art_h,
            bevel_radius=0.006,
            segments=2,
            offset=(0.0, art_y - 0.015, art_center_z - (art_h / 2.0)),
            mat_index=black_idx,
        )

        # Inner Brass Slip / Inset Margin
        create_beveled_box(
            bm,
            width=art_w - (art_frame_th * 1.6),
            length=0.01,
            height=art_h - (art_frame_th * 1.6),
            bevel_radius=0.002,
            segments=1,
            offset=(0.0, art_y - 0.022, art_center_z - (art_h / 2.0) + (art_frame_th * 0.8)),
            mat_index=brass_idx,
        )

        # Canvas Artwork Face (Mountain Monochrome Graphic)
        create_beveled_box(
            bm,
            width=art_w - (art_frame_th * 2.2),
            length=0.005,
            height=art_h - (art_frame_th * 2.2),
            bevel_radius=0.002,
            segments=1,
            offset=(0.0, art_y - 0.025, art_center_z - (art_h / 2.0) + (art_frame_th * 1.1)),
            mat_index=boucle_idx,
        )

    def _build_ceiling_tray_and_cove(
        self,
        bm: Any,
        mat_lib: MaterialLibrary,
    ) -> None:
        """Create architectural false ceiling with recessed tray and continuous indirect warm LED cove lighting."""
        boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")
        led_idx = mat_lib.get_index("LED_WARM_2700K")

        soffit_z = self.room_height_z - self.ceiling_drop
        tray_w = self.room_width_x - (self.cove_inset * 2.0)
        tray_l = self.room_length_y - (self.cove_inset * 2.0)

        # Perimeter Dropped Soffit (North, South, East, West borders)
        # North border (back)
        create_beveled_box(
            bm,
            width=self.room_width_x,
            length=self.cove_inset,
            height=self.ceiling_drop,
            bevel_radius=0.01,
            segments=2,
            offset=(0.0, (self.room_length_y / 2.0) - (self.cove_inset / 2.0), soffit_z),
            mat_index=boucle_idx,
        )
        # South border (front)
        create_beveled_box(
            bm,
            width=self.room_width_x,
            length=self.cove_inset,
            height=self.ceiling_drop,
            bevel_radius=0.01,
            segments=2,
            offset=(0.0, -(self.room_length_y / 2.0) + (self.cove_inset / 2.0), soffit_z),
            mat_index=boucle_idx,
        )
        # West border (left)
        create_beveled_box(
            bm,
            width=self.cove_inset,
            length=tray_l,
            height=self.ceiling_drop,
            bevel_radius=0.01,
            segments=2,
            offset=(-(self.room_width_x / 2.0) + (self.cove_inset / 2.0), 0.0, soffit_z),
            mat_index=boucle_idx,
        )
        # East border (right)
        create_beveled_box(
            bm,
            width=self.cove_inset,
            length=tray_l,
            height=self.ceiling_drop,
            bevel_radius=0.01,
            segments=2,
            offset=((self.room_width_x / 2.0) - (self.cove_inset / 2.0), 0.0, soffit_z),
            mat_index=boucle_idx,
        )

        # Upper Recessed Ceiling Tray Slab
        create_beveled_box(
            bm,
            width=tray_w,
            length=tray_l,
            height=0.04,
            bevel_radius=0.005,
            segments=1,
            offset=(0.0, 0.0, self.room_height_z - 0.04),
            mat_index=boucle_idx,
        )

        # Continuous Perimeter Indirect LED Cove Lighting Strip
        cove_strip_th = 0.015
        # North cove LED
        create_beveled_box(
            bm,
            width=tray_w * 0.98,
            length=cove_strip_th,
            height=cove_strip_th,
            bevel_radius=0.002,
            segments=1,
            offset=(0.0, (tray_l / 2.0) + (cove_strip_th / 2.0), soffit_z + 0.02),
            mat_index=led_idx,
        )
        # South cove LED
        create_beveled_box(
            bm,
            width=tray_w * 0.98,
            length=cove_strip_th,
            height=cove_strip_th,
            bevel_radius=0.002,
            segments=1,
            offset=(0.0, -(tray_l / 2.0) - (cove_strip_th / 2.0), soffit_z + 0.02),
            mat_index=led_idx,
        )
        # West cove LED
        create_beveled_box(
            bm,
            width=cove_strip_th,
            length=tray_l * 0.98,
            height=cove_strip_th,
            bevel_radius=0.002,
            segments=1,
            offset=(-(tray_w / 2.0) - (cove_strip_th / 2.0), 0.0, soffit_z + 0.02),
            mat_index=led_idx,
        )
        # East cove LED
        create_beveled_box(
            bm,
            width=cove_strip_th,
            length=tray_l * 0.98,
            height=cove_strip_th,
            bevel_radius=0.002,
            segments=1,
            offset=((tray_w / 2.0) + (cove_strip_th / 2.0), 0.0, soffit_z + 0.02),
            mat_index=led_idx,
        )

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct the full architectural envelope, floor tiles, rug, accent wall, and ceiling cove."""
        travertine_idx = mat_lib.get_index("TRAVERTINE_TILES")
        boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")
        walnut_idx = mat_lib.get_index("WALNUT_WOOD")

        back_wall_y = (self.room_length_y / 2.0) - 0.05
        front_wall_y = -(self.room_length_y / 2.0) + 0.05
        left_wall_x = -(self.room_width_x / 2.0) + 0.05
        right_wall_x = (self.room_width_x / 2.0) - 0.05

        # 1. Beveled Travertine Tile Floor
        self._build_tiled_floor(bm, travertine_idx, tile_size=0.85, grout_gap=0.006)

        # 2. Large Plush Area Rug Under Bed & Bench
        rug_w = 3.20
        rug_l = 3.80
        rug_h = 0.016
        create_beveled_box(
            bm,
            width=rug_w,
            length=rug_l,
            height=rug_h,
            bevel_radius=0.005,
            segments=2,
            offset=(0.0, 0.40, 0.0),
            mat_index=boucle_idx,
        )

        # 3. Fluted Wood Accent Wall & Mountain Art behind Bed
        self._build_accent_headboard_wall(bm, mat_lib, back_wall_y)

        # 4. Architectural Perimeter Walls (Manifold 0.20m thick)
        # Back Solid Wall
        create_beveled_box(
            bm,
            width=self.room_width_x + (self.wall_thickness * 2.0),
            length=self.wall_thickness,
            height=self.room_height_z,
            bevel_radius=0.01,
            segments=2,
            offset=(0.0, (self.room_length_y / 2.0) + (self.wall_thickness / 2.0), 0.0),
            mat_index=boucle_idx,
        )
        # Front Wall (Media wall boundary)
        create_beveled_box(
            bm,
            width=self.room_width_x + (self.wall_thickness * 2.0),
            length=self.wall_thickness,
            height=self.room_height_z,
            bevel_radius=0.01,
            segments=2,
            offset=(0.0, -(self.room_length_y / 2.0) - (self.wall_thickness / 2.0), 0.0),
            mat_index=boucle_idx,
        )
        # Left Wall (Window wall boundary)
        create_beveled_box(
            bm,
            width=self.wall_thickness,
            length=self.room_length_y,
            height=self.room_height_z,
            bevel_radius=0.01,
            segments=2,
            offset=(-(self.room_width_x / 2.0) - (self.wall_thickness / 2.0), 0.0, 0.0),
            mat_index=boucle_idx,
        )
        # Right Wall (Wardrobe & Entrance Door boundary)
        create_beveled_box(
            bm,
            width=self.wall_thickness,
            length=self.room_length_y,
            height=self.room_height_z,
            bevel_radius=0.01,
            segments=2,
            offset=((self.room_width_x / 2.0) + (self.wall_thickness / 2.0), 0.0, 0.0),
            mat_index=boucle_idx,
        )

        # Entrance Door in Right Wall (at front right corner as shown in floorplan and thumbnails)
        door_w = 0.90
        door_h = 2.15
        door_y = -(self.room_length_y / 2.0) + 0.95
        # Door frame
        create_beveled_box(
            bm,
            width=0.08,
            length=door_w + 0.08,
            height=door_h + 0.04,
            bevel_radius=0.008,
            segments=2,
            offset=(right_wall_x + 0.02, door_y, 0.0),
            mat_index=walnut_idx,
        )
        # Door leaf panel
        create_beveled_box(
            bm,
            width=0.045,
            length=door_w,
            height=door_h,
            bevel_radius=0.006,
            segments=2,
            offset=(right_wall_x + 0.02, door_y, 0.0),
            mat_index=walnut_idx,
        )

        # 5. Dropped False Ceiling with Indirect Cove LED Lighting
        self._build_ceiling_tray_and_cove(bm, mat_lib)

        return {
            "envelope_placed": True,
            "room_dimensions": (self.room_width_x, self.room_length_y, self.room_height_z),
            "floor_tiles_active": True,
            "area_rug_placed": True,
            "fluted_accent_wall_active": True,
            "ceiling_cove_active": True,
            "entrance_door_placed": True,
        }
