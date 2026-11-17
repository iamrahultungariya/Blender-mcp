"""Lighting Kit (Ceiling Pendant Lights, Morning Sunlight, Window Daylight Fill).

Tier 3 Modular Prefab: Constructs physical cinematic lighting fixtures and lamps.
"""
from __future__ import annotations

import math
import bpy
from luxury_bedroom.core.mesh_utils import (
    bmesh_to_object,
    create_cylinder,
)


def build_lighting(
    col: bpy.types.Collection, mats: dict[str, bpy.types.Material]
) -> dict[str, bpy.types.Object]:
    """Construct ceiling-hung minimalist pendant lights and morning sunlight."""
    objs = {}

    for side, pos_x in [("Left", -1.48), ("Right", 1.48)]:
        # 1. Ceiling Canopy Disc
        canopy_bm = create_cylinder(radius=0.045, height=0.012, segments=24, offset=(pos_x, 1.88, 2.838))
        objs[f"Canopy_{side}"] = bmesh_to_object(
            canopy_bm, f"Pendant_{side}_Canopy", col, mats["BRUSHED_BRASS"]
        )

        # 2. Slender Straight Suspension Cable (3mm radius)
        cable_h = 2.85 - 1.48
        cable_bm = create_cylinder(radius=0.003, height=cable_h, segments=12, offset=(pos_x, 1.88, 1.48))
        objs[f"Cable_{side}"] = bmesh_to_object(
            cable_bm, f"Pendant_{side}_Cable", col, mats["MATTE_BLACK"]
        )

        # 3. Minimalist Brushed Brass Cylindrical Pendant Shade
        shade_bm = create_cylinder(radius=0.040, height=0.26, segments=24, offset=(pos_x, 1.88, 1.22))
        objs[f"Pendant_Shade_{side}"] = bmesh_to_object(
            shade_bm, f"Pendant_{side}_Brass_Shade", col, mats["BRUSHED_BRASS"]
        )

        # 4. Emissive Bottom Diffuser
        diffuser_bm = create_cylinder(radius=0.036, height=0.01, segments=24, offset=(pos_x, 1.88, 1.22))
        objs[f"Diffuser_{side}"] = bmesh_to_object(
            diffuser_bm, f"Pendant_{side}_Diffuser", col, mats["WARM_LED"]
        )

        # 5. Downward Warm Accent Spot / Point Light
        pl_name = f"Light_Pendant_{side}_Warm"
        pl_data = bpy.data.lights.new(pl_name, type="POINT")
        pl_data.energy = 42.0
        pl_data.color = (1.0, 0.86, 0.68)
        pl_data.shadow_soft_size = 0.08
        pl_obj = bpy.data.objects.new(pl_name, pl_data)
        col.objects.link(pl_obj)
        pl_obj.location = (pos_x, 1.88, 1.18)
        objs[f"Pendant_Light_{side}"] = pl_obj

    # 6. Morning Sunlight (Sun Lamp through Window)
    sun_name = "Sun_Morning_Gold"
    sun_data = bpy.data.lights.new(sun_name, type="SUN")
    sun_data.energy = 7.5
    sun_data.color = (1.0, 0.93, 0.82)
    sun_data.angle = math.radians(3.2)
    sun_obj = bpy.data.objects.new(sun_name, sun_data)
    col.objects.link(sun_obj)
    sun_obj.location = (-6.0, -2.5, 5.0)
    sun_obj.rotation_euler = (math.radians(48.0), math.radians(24.0), math.radians(-52.0))
    objs["Sun_Light"] = sun_obj

    # 7. Window Soft Sky Daylight (Area Light)
    sky_name = "Light_Window_Sky_Daylight"
    sky_data = bpy.data.lights.new(sky_name, type="AREA")
    sky_data.energy = 160.0
    sky_data.color = (0.88, 0.94, 1.0)
    sky_data.size = 2.40
    sky_data.size_y = 2.05
    sky_obj = bpy.data.objects.new(sky_name, sky_data)
    col.objects.link(sky_obj)
    sky_obj.location = (-2.56, 0.40, 1.45)
    sky_obj.rotation_euler = (0.0, math.radians(90.0), 0.0)
    objs["Sky_Area_Light"] = sky_obj

    return objs
