"""Autonomous Vehicle Thinking & Topology Heuristics Engine.

Provides procedural knowledge, aerodynamic curvature formulas, dimensional proportions,
and topological form rules so an AI modeling agent creates AAA vehicle silhouettes
even without a user-supplied reference image.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
import numpy as np


class VehicleThinkingEngine:
    """Automotive design intelligence engine calculating form rules and curvature splines."""

    ARCHETYPES: Dict[str, Dict[str, float]] = {
        "AMBULANCE_VAN": {
            "length": 5.92,
            "width": 2.05,
            "height": 2.75,
            "wheelbase": 3.66,
            "front_overhang": 0.96,
            "rear_overhang": 1.30,
            "track_front": 1.72,
            "track_rear": 1.73,
            "ground_clearance": 0.20,
            "tire_radius": 0.375,
            "rim_radius": 0.215,
            "tire_width": 0.235,
        },
        "SEDAN": {
            "length": 4.85,
            "width": 1.85,
            "height": 1.45,
            "wheelbase": 2.85,
            "front_overhang": 0.90,
            "rear_overhang": 1.10,
            "track_front": 1.58,
            "track_rear": 1.58,
            "ground_clearance": 0.14,
            "tire_radius": 0.33,
            "rim_radius": 0.23,
            "tire_width": 0.225,
        },
        "SUPERCAR": {
            "length": 4.55,
            "width": 2.02,
            "height": 1.18,
            "wheelbase": 2.65,
            "front_overhang": 0.95,
            "rear_overhang": 0.95,
            "track_front": 1.68,
            "track_rear": 1.70,
            "ground_clearance": 0.10,
            "tire_radius": 0.34,
            "rim_radius": 0.26,
            "tire_width": 0.305,
        },
        "SUV": {
            "length": 4.95,
            "width": 1.98,
            "height": 1.78,
            "wheelbase": 2.95,
            "front_overhang": 0.92,
            "rear_overhang": 1.08,
            "track_front": 1.66,
            "track_rear": 1.67,
            "ground_clearance": 0.22,
            "tire_radius": 0.38,
            "rim_radius": 0.25,
            "tire_width": 0.265,
        },
        "TRUCK": {
            "length": 6.80,
            "width": 2.45,
            "height": 3.10,
            "wheelbase": 4.20,
            "front_overhang": 1.10,
            "rear_overhang": 1.50,
            "track_front": 2.02,
            "track_rear": 2.02,
            "ground_clearance": 0.28,
            "tire_radius": 0.52,
            "rim_radius": 0.29,
            "tire_width": 0.315,
        },
    }

    CURVATURE_RULES: Dict[str, Dict[str, float]] = {
        "AMBULANCE_VAN": {
            "hood_rake_deg": 32.0,            # Downward slope from cowl to grille
            "hood_sagitta": 0.035,            # Subtle convex crown across hood width
            "windshield_rake_deg": 44.0,      # Rearward incline from cowl to roof
            "windshield_curvature_sagitta": 0.075, # Horizontal bow forward
            "tumblehome_deg": 6.5,            # Inward tilt of side greenhouse pillars
            "roof_blister_height": 0.45,      # High-roof fiberglass aerodynamic bubble
            "roof_blister_rake_deg": 38.0,    # Smooth S-curve transition above windshield
            "wheel_arch_clearance": 0.08,     # Radial gap above tire
            "fender_lip_outset": 0.028,       # Flares outward from side panel
            "corner_fillet_radius": 0.085,    # Soft rounding on all exterior corners
        },
        "SEDAN": {
            "hood_rake_deg": 18.0,
            "hood_sagitta": 0.04,
            "windshield_rake_deg": 58.0,
            "windshield_curvature_sagitta": 0.09,
            "tumblehome_deg": 14.0,
            "roof_blister_height": 0.0,
            "roof_blister_rake_deg": 0.0,
            "wheel_arch_clearance": 0.05,
            "fender_lip_outset": 0.02,
            "corner_fillet_radius": 0.05,
        },
        "SUPERCAR": {
            "hood_rake_deg": 22.0,
            "hood_sagitta": 0.06,
            "windshield_rake_deg": 65.0,
            "windshield_curvature_sagitta": 0.12,
            "tumblehome_deg": 22.0,
            "roof_blister_height": 0.0,
            "roof_blister_rake_deg": 0.0,
            "wheel_arch_clearance": 0.03,
            "fender_lip_outset": 0.05,
            "corner_fillet_radius": 0.03,
        }
    }

    def get_archetype_proportions(self, vehicle_type: str) -> Dict[str, float]:
        """Return standardized dimensional proportions for a vehicle class."""
        key = vehicle_type.upper()
        if key not in self.ARCHETYPES:
            key = "AMBULANCE_VAN"
        return dict(self.ARCHETYPES[key])

    def get_aerodynamic_curvatures(self, vehicle_type: str) -> Dict[str, float]:
        """Return aerodynamic angle and curvature rules for styling."""
        key = vehicle_type.upper()
        if key not in self.CURVATURE_RULES:
            key = "AMBULANCE_VAN"
        return dict(self.CURVATURE_RULES[key])

    def generate_van_chassis_profile(
        self,
        length: float = 5.92,
        width: float = 2.05,
        height: float = 2.75
    ) -> Dict[str, Any]:
        """Calculate complete parametric 3D curve profiles for an aerodynamic high-roof van."""
        prop = self.get_archetype_proportions("AMBULANCE_VAN")
        curv = self.get_aerodynamic_curvatures("AMBULANCE_VAN")

        # Coordinate frame:
        # X: Width (-width/2 to +width/2, Left to Right)
        # Y: Length (Front is +Y, Rear is -Y)
        # Z: Height (0 = Ground, +Z Up)

        # Reference Keypoints along Y (centerline X=0):
        y_front_bumper = length * 0.5
        y_grille = y_front_bumper - 0.22
        y_hood_front = y_grille - 0.08
        y_cowl = y_front_bumper - prop["front_overhang"]  # Base of windshield
        y_windshield_top = y_cowl - 0.85
        y_roof_blister_peak = y_windshield_top - 0.40
        y_rear_bumper = -length * 0.5
        y_rear_doors = y_rear_bumper + 0.15

        # Keypoints along Z:
        z_ground = 0.0
        z_bumper_bottom = prop["ground_clearance"]
        z_grille_top = z_bumper_bottom + 0.58
        z_hood_front = z_grille_top + 0.12
        z_cowl = z_hood_front + 0.32          # Windshield base (~1.22m)
        z_windshield_top = z_cowl + 0.78     # Lower cab roofline (~2.00m)
        z_roof_high = height                 # Full raised roof peak (~2.75m)
        z_beltline = height * 0.52           # Side rubbing strip height (~1.43m)

        # 1. Hood Centerline Spline (Front to Cowl)
        # Slopes downwards towards the front with subtle parabolic crown
        hood_pts = []
        n_hood = 6
        for i in range(n_hood):
            t = i / (n_hood - 1)
            y = (1.0 - t) * y_hood_front + t * y_cowl
            # Parabolic drop
            z = (1.0 - t) * z_hood_front + t * z_cowl + 0.02 * math.sin(t * math.pi)
            hood_pts.append([0.0, float(y), float(z)])

        # 2. Windshield Centerline Spline (Cowl to Roof Header)
        # Rakes backward ~44 deg
        windshield_pts = []
        n_ws = 6
        for i in range(n_ws):
            t = i / (n_ws - 1)
            y = (1.0 - t) * y_cowl + t * y_windshield_top
            z = (1.0 - t) * z_cowl + t * z_windshield_top
            windshield_pts.append([0.0, float(y), float(z)])

        # 3. Roof Aerodynamic Blister Spline (Windshield Top to High Roof)
        # Smooth S-curve transition blister
        roof_pts = []
        n_roof_trans = 6
        for i in range(n_roof_trans):
            t = i / (n_roof_trans - 1)
            # Smoothstep interpolation
            smooth_t = t * t * (3.0 - 2.0 * t)
            y = (1.0 - t) * y_windshield_top + t * y_roof_blister_peak
            z = (1.0 - smooth_t) * z_windshield_top + smooth_t * z_roof_high
            roof_pts.append([0.0, float(y), float(z)])

        # Extend roof back horizontally to rear doors
        roof_pts.append([0.0, float(y_rear_doors + 0.2), float(z_roof_high)])
        roof_pts.append([0.0, float(y_rear_doors), float(z_roof_high - 0.04)])

        # 4. Wheel Arch Centers
        # Front wheel center
        y_front_wheel = y_cowl - 0.28
        # Rear wheel center (wheelbase distance behind front)
        y_rear_wheel = y_front_wheel - prop["wheelbase"]
        z_wheel_center = prop["tire_radius"]

        wheel_arches = {
            "front_left": [width * 0.5, y_front_wheel, z_wheel_center],
            "front_right": [-width * 0.5, y_front_wheel, z_wheel_center],
            "rear_left": [width * 0.5, y_rear_wheel, z_wheel_center],
            "rear_right": [-width * 0.5, y_rear_wheel, z_wheel_center],
            "arch_radius": prop["tire_radius"] + curv["wheel_arch_clearance"],
            "tire_radius": prop["tire_radius"],
            "rim_radius": prop["rim_radius"],
        }

        return {
            "hood_spline": hood_pts,
            "windshield_spline": windshield_pts,
            "roof_spline": roof_pts,
            "wheel_arches": wheel_arches,
            "beltline_z": z_beltline,
            "tumblehome_deg": curv["tumblehome_deg"],
            "bounds": {
                "min": [-width * 0.5, y_rear_bumper, z_ground],
                "max": [width * 0.5, y_front_bumper, height],
            }
        }

    def get_decal_and_lighting_spec(self, vehicle_type: str) -> Dict[str, Any]:
        """Return placement specifications for emergency lightbars, pods, and decals."""
        prop = self.get_archetype_proportions(vehicle_type)
        return {
            "front_lightbar": {
                "center": [0.0, 0.45, prop["height"] - 0.02],
                "length": 1.40,
                "width": 0.26,
                "height": 0.09,
                "colors": ["RED", "BLUE"],
                "luminous_power_lumens": 4200.0,
            },
            "rear_pods": {
                "left": [prop["width"] * 0.40, -prop["length"] * 0.46, prop["height"] - 0.04],
                "right": [-prop["width"] * 0.40, -prop["length"] * 0.46, prop["height"] - 0.04],
                "radius": 0.09,
                "colors": ["BLUE", "RED"],
            },
            "star_of_life": {
                "color": [0.05, 0.25, 0.85, 1.0],
                "left_side_center": [prop["width"] * 0.505, -0.65, prop["height"] * 0.65],
                "right_side_center": [-prop["width"] * 0.505, -0.65, prop["height"] * 0.65],
                "scale": 0.48,
            },
            "chevron_stripes": {
                "rear_bumper_center": [0.0, -prop["length"] * 0.49, 0.55],
                "colors": ["RED", "YELLOW"],
                "angle_deg": 45.0,
            }
        }
