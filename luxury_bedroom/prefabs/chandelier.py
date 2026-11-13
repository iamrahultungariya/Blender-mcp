"""Chandelier: Suspended Circular Halo Ring LED Chandelier.

Direct procedural recreation of the hero pendant light from the reference turnaround sheet:
- Suspended circular halo ring fixture centered over the bed and seating area
- Brushed brass and dark bronze ring casing
- Inner continuous warm 2700K LED emissive light band
- 3 ultra-slim suspension aircraft wires connecting to ceiling canopy
- Ceiling brass canopy mounting plate
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


class ChandelierBuilder:
    """Builder for the suspended circular halo ring LED chandelier."""

    def __init__(
        self,
        center_x: float = 0.0,
        center_y: float = 0.40,
        ring_radius: float = 0.60,
        ring_thickness: float = 0.045,
        ring_height: float = 0.055,
        suspension_z: float = 2.18,
        ceiling_z: float = 2.80,
        num_segments: int = 48,
    ) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.ring_radius = ring_radius
        self.ring_thickness = ring_thickness
        self.ring_height = ring_height
        self.suspension_z = suspension_z
        self.ceiling_z = ceiling_z
        self.num_segments = num_segments

    def _build_halo_ring(
        self,
        bm: Any,
        casing_mat: int,
        led_mat: int,
    ) -> None:
        """Construct the concentric halo ring with outer brass casing and inner glowing LED surface."""
        r_outer = self.ring_radius
        r_inner = self.ring_radius - self.ring_thickness
        r_led = self.ring_radius - (self.ring_thickness * 0.70)
        h = self.ring_height
        z_base = self.suspension_z

        # Create polygonal ring segments
        for seg in range(self.num_segments):
            theta0 = 2.0 * math.pi * (seg / self.num_segments)
            theta1 = 2.0 * math.pi * ((seg + 1) / self.num_segments)

            cos0, sin0 = math.cos(theta0), math.sin(theta0)
            cos1, sin1 = math.cos(theta1), math.sin(theta1)

            # Outer casing segment (quad box approximation)
            p_out0 = (self.center_x + r_outer * cos0, self.center_y + r_outer * sin0)
            p_out1 = (self.center_x + r_outer * cos1, self.center_y + r_outer * sin1)
            p_in0 = (self.center_x + r_inner * cos0, self.center_y + r_inner * sin0)
            p_in1 = (self.center_x + r_inner * cos1, self.center_y + r_inner * sin1)

            # Outer casing faces
            v_bot_out0 = (p_out0[0], p_out0[1], z_base)
            v_bot_out1 = (p_out1[0], p_out1[1], z_base)
            v_top_out0 = (p_out0[0], p_out0[1], z_base + h)
            v_top_out1 = (p_out1[0], p_out1[1], z_base + h)

            v_bot_in0 = (p_in0[0], p_in0[1], z_base)
            v_bot_in1 = (p_in1[0], p_in1[1], z_base)
            v_top_in0 = (p_in0[0], p_in0[1], z_base + h)
            v_top_in1 = (p_in1[0], p_in1[1], z_base + h)

            def add_quad(pts: Tuple[Tuple[float, float, float], ...], mat_idx: int) -> None:
                if HAS_BMESH and isinstance(bm, bmesh.types.BMesh):
                    v_objs = [bm.verts.new(Vector(p)) for p in pts]
                    try:
                        f = bm.faces.new(v_objs)
                        f.material_index = mat_idx
                    except ValueError:
                        pass
                else:
                    v_objs = [MockBMVert(p, len(bm.verts) + idx) for idx, p in enumerate(pts)]
                    bm.verts.extend(v_objs)
                    bm.faces.append(MockBMFace(tuple(v_objs), material_index=mat_idx))

            # Outer perimeter face (Brushed Brass)
            add_quad((v_bot_out0, v_bot_out1, v_top_out1, v_top_out0), casing_mat)

            # Top rim face (Brushed Brass)
            add_quad((v_top_out0, v_top_out1, v_top_in1, v_top_in0), casing_mat)

            # Bottom rim face (Brushed Brass)
            add_quad((v_bot_in0, v_bot_in1, v_bot_out1, v_bot_out0), casing_mat)

            # Inner perimeter face: Warm Emissive LED Light Band!
            add_quad((v_bot_in1, v_bot_in0, v_top_in0, v_top_in1), led_mat)

    def _build_suspension_and_canopy(
        self,
        bm: Any,
        wire_mat: int,
        canopy_mat: int,
    ) -> None:
        """Create 3 suspension wires converging up to a ceiling canopy."""
        canopy_r = 0.12
        canopy_h = 0.025
        canopy_z = self.ceiling_z - canopy_h

        # Ceiling Canopy Rosette (Brushed Brass)
        canopy_profile = [(0.0, 0.0), (canopy_r, 0.0), (canopy_r, canopy_h), (0.0, canopy_h)]
        create_lathe_mesh(
            bm,
            canopy_profile,
            segs=24,
            center=(self.center_x, self.center_y, canopy_z),
            mat_index=canopy_mat,
        )

        # 3 Suspension Aircraft Cables
        num_wires = 3
        wire_r = 0.003
        for w_idx in range(num_wires):
            angle = (2.0 * math.pi * w_idx) / num_wires
            ring_attach_x = self.center_x + (self.ring_radius - (self.ring_thickness / 2.0)) * math.cos(angle)
            ring_attach_y = self.center_y + (self.ring_radius - (self.ring_thickness / 2.0)) * math.sin(angle)
            ring_attach_z = self.suspension_z + self.ring_height

            canopy_attach_x = self.center_x + (canopy_r * 0.6) * math.cos(angle)
            canopy_attach_y = self.center_y + (canopy_r * 0.6) * math.sin(angle)
            canopy_attach_z = canopy_z

            # Cable thin box approximation
            dx = canopy_attach_x - ring_attach_x
            dy = canopy_attach_y - ring_attach_y
            dz = canopy_attach_z - ring_attach_z
            length = math.sqrt(dx**2 + dy**2 + dz**2)
            mid_x = (ring_attach_x + canopy_attach_x) / 2.0
            mid_y = (ring_attach_y + canopy_attach_y) / 2.0
            mid_z = (ring_attach_z + canopy_attach_z) / 2.0

            create_beveled_box(
                bm,
                width=wire_r * 2.0,
                length=wire_r * 2.0,
                height=length,
                bevel_radius=0.001,
                segments=1,
                offset=(mid_x, mid_y, ring_attach_z),
                mat_index=wire_mat,
            )

    def build(self, bm: Any, mat_lib: MaterialLibrary) -> Dict[str, Any]:
        """Construct the halo chandelier assembly into the BMesh buffer."""
        brass_idx = mat_lib.get_index("BRUSHED_BRASS")
        led_idx = mat_lib.get_index("LED_WARM_2700K")
        wire_idx = mat_lib.get_index("MATTE_BLACK_METAL")

        # 1. Circular Halo Ring Body & Inner LED Band
        self._build_halo_ring(bm, brass_idx, led_idx)

        # 2. Suspension Cables and Ceiling Rosette Canopy
        self._build_suspension_and_canopy(bm, wire_idx, brass_idx)

        return {
            "chandelier_placed": True,
            "halo_radius": self.ring_radius,
            "halo_diameter": self.ring_radius * 2.0,
            "suspension_z": self.suspension_z,
            "emissive_led_active": True,
        }
