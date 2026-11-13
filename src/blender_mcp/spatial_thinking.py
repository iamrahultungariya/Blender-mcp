"""Universal Spatial & Architectural Intelligence Engine.

Provides multi-domain spatial reasoning, architectural datums, ergonomic furniture
curvature formulas, and anti-boxy topological mandates across Architecture, Interior Spaces,
Furniture/Product Design, and Automotive/Vehicle domains.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from blender_mcp.vehicle_thinking import VehicleThinkingEngine


class SpatialThinkingEngine:
    """Universal spatial intelligence reasoning across Architecture, Interiors, Furniture, and Vehicles."""

    # 4 Core Domains
    DOMAIN_ARCHITECTURE = "ARCHITECTURE"
    DOMAIN_INTERIOR = "INTERIOR_SPACES"
    DOMAIN_FURNITURE = "FURNITURE_PRODUCT"
    DOMAIN_VEHICLE = "VEHICLE"

    # Multi-Domain Dimensional Standards & Datums (meters)
    ARCHETYPES: Dict[str, Dict[str, float]] = {
        # --- ARCHITECTURE ---
        "MODERN_VILLA": {
            "length": 14.0,
            "width": 10.0,
            "height": 6.8,
            "exterior_wall_thickness": 0.28,
            "interior_wall_thickness": 0.12,
            "floor_to_floor": 3.20,
            "window_sill": 0.85,
            "window_reveal_depth": 0.18,
            "door_height": 2.10,
            "door_width": 0.90,
            "overhang": 0.60,
            "foundation_depth": 0.45,
        },
        "RESIDENTIAL_HOUSE": {
            "length": 12.0,
            "width": 8.5,
            "height": 7.2,
            "exterior_wall_thickness": 0.25,
            "interior_wall_thickness": 0.10,
            "floor_to_floor": 3.00,
            "window_sill": 0.90,
            "window_reveal_depth": 0.15,
            "door_height": 2.10,
            "door_width": 0.90,
            "overhang": 0.45,
            "foundation_depth": 0.40,
        },
        "CONTEMPORARY_CABIN": {
            "length": 8.0,
            "width": 5.5,
            "height": 4.8,
            "exterior_wall_thickness": 0.22,
            "interior_wall_thickness": 0.10,
            "floor_to_floor": 2.90,
            "window_sill": 0.80,
            "window_reveal_depth": 0.14,
            "door_height": 2.10,
            "door_width": 0.90,
            "overhang": 0.50,
            "foundation_depth": 0.35,
        },

        # --- INTERIOR SPACES ---
        "LIVING_ROOM": {
            "length": 6.0,
            "width": 4.5,
            "height": 2.90,
            "baseboard_height": 0.12,
            "crown_molding_height": 0.08,
            "ceiling_drop": 0.15,
            "wall_thickness": 0.15,
            "door_casing_width": 0.08,
            "cove_recess_depth": 0.05,
        },
        "BEDROOM": {
            "length": 4.5,
            "width": 4.0,
            "height": 2.80,
            "baseboard_height": 0.10,
            "crown_molding_height": 0.07,
            "ceiling_drop": 0.12,
            "wall_thickness": 0.12,
            "door_casing_width": 0.08,
            "cove_recess_depth": 0.04,
        },
        "KITCHEN": {
            "length": 4.2,
            "width": 3.6,
            "height": 2.80,
            "counter_height": 0.90,
            "counter_depth": 0.65,
            "upper_cabinet_depth": 0.35,
            "backsplash_height": 0.60,
            "toe_kick_height": 0.10,
            "toe_kick_depth": 0.08,
            "wall_thickness": 0.15,
        },

        # --- FURNITURE & PRODUCT DESIGN ---
        "SOFA_3_SEATER": {
            "length": 2.20,
            "depth": 0.92,
            "height": 0.82,
            "seat_height": 0.44,
            "seat_depth": 0.60,
            "cushion_crown": 0.04,
            "armrest_width": 0.18,
            "armrest_height": 0.62,
            "back_angle_deg": 104.0,
            "back_cushion_thickness": 0.16,
            "seat_cushion_thickness": 0.18,
            "leg_height": 0.14,
            "fillet_radius": 0.025,
        },
        "ARMCHAIR_LOUNGE": {
            "length": 0.88,
            "depth": 0.85,
            "height": 0.78,
            "seat_height": 0.42,
            "seat_depth": 0.54,
            "cushion_crown": 0.045,
            "armrest_width": 0.12,
            "armrest_height": 0.58,
            "back_angle_deg": 105.0,
            "back_cushion_thickness": 0.14,
            "seat_cushion_thickness": 0.16,
            "leg_height": 0.18,
            "fillet_radius": 0.020,
        },
        "DINING_TABLE": {
            "length": 1.80,
            "width": 0.90,
            "height": 0.76,
            "top_thickness": 0.035,
            "edge_bevel_radius": 0.006,
            "apron_recess": 0.05,
            "leg_taper_top": 0.06,
            "leg_taper_bottom": 0.035,
        },
        "DINING_CHAIR": {
            "length": 0.48,
            "depth": 0.52,
            "height": 0.86,
            "seat_height": 0.46,
            "seat_depth": 0.42,
            "cushion_crown": 0.025,
            "back_angle_deg": 100.0,
            "back_height": 0.40,
            "leg_height": 0.44,
            "fillet_radius": 0.012,
        },
    }

    # Archetype Aliases Map
    ALIASES: Dict[str, str] = {
        "VILLA": "MODERN_VILLA",
        "MODERN_HOUSE": "MODERN_VILLA",
        "HOUSE": "RESIDENTIAL_HOUSE",
        "BUILDING": "RESIDENTIAL_HOUSE",
        "CABIN": "CONTEMPORARY_CABIN",
        "ROOM": "LIVING_ROOM",
        "HALL": "LIVING_ROOM",
        "SOFA": "SOFA_3_SEATER",
        "COUCH": "SOFA_3_SEATER",
        "CHAIR": "DINING_CHAIR",
        "ARMCHAIR": "ARMCHAIR_LOUNGE",
        "TABLE": "DINING_TABLE",
    }

    def __init__(self) -> None:
        self.vehicle_engine = VehicleThinkingEngine()

    def classify_domain(self, query: str) -> str:
        """Infer the spatial domain from user query keywords."""
        q = query.lower()

        # Architecture keywords
        arch_words = [
            "villa", "house", "building", "facade", "cabin", "cottage", "bungalow",
            "mansion", "architecture", "architectural", "roof", "exterior", "porch",
            "pavilion", "patio", "courtyard", "eaves"
        ]
        if any(w in q for w in arch_words):
            return self.DOMAIN_ARCHITECTURE

        # Interior spaces keywords
        interior_words = [
            "room", "living room", "bedroom", "kitchen", "bathroom", "dining room",
            "interior", "hallway", "ceiling", "baseboard", "molding", "casing",
            "foyer", "loft", "closet"
        ]
        if any(w in q for w in interior_words):
            return self.DOMAIN_INTERIOR

        # Furniture & product keywords
        furniture_words = [
            "sofa", "couch", "chair", "armchair", "table", "desk", "bed", "bench",
            "stool", "cushion", "upholstery", "credenza", "cabinet", "shelf",
            "sideboard", "nightstand", "dresser"
        ]
        if any(w in q for w in furniture_words):
            return self.DOMAIN_FURNITURE

        # Vehicle keywords
        vehicle_words = [
            "car", "vehicle", "van", "truck", "sedan", "supercar", "coupe", "suv",
            "ambulance", "automotive", "aerodynamic", "wheel", "chassis", "splitter",
            "spoiler", "hood", "fender"
        ]
        if any(w in q for w in vehicle_words):
            return self.DOMAIN_VEHICLE

        # Default fallback: ARCHITECTURE if environmental, else FURNITURE
        if "space" in q or "structure" in q:
            return self.DOMAIN_ARCHITECTURE
        return self.DOMAIN_FURNITURE

    def get_dimensions(self, archetype: str) -> Dict[str, float]:
        """Lookup dimensional standards for any spatial archetype or alias."""
        key = archetype.upper().strip()
        if key in self.ALIASES:
            key = self.ALIASES[key]

        if key in self.ARCHETYPES:
            return self.ARCHETYPES[key].copy()

        # Check vehicle archetypes
        if key in self.vehicle_engine.ARCHETYPES:
            return self.vehicle_engine.ARCHETYPES[key].copy()

        # Fuzzy match fallback
        for k, v in self.ARCHETYPES.items():
            if k in key or key in k:
                return v.copy()

        # Default architectural dimension set if unknown
        return self.ARCHETYPES["MODERN_VILLA"].copy()

    def calculate_cushion_loft(
        self,
        u: float,
        v: float,
        crown: float,
        z0: float = 0.0
    ) -> float:
        """Calculate double-parabolic organic cushion loft height.

        Formula: Z(u, v) = z0 + crown * (1 - u^2) * (1 - v^2) for u, v in [-1, 1].
        Yields maximum puff at (0, 0) and zero elevation at the cushion seams (|u|=1 or |v|=1).
        """
        u_clamped = max(-1.0, min(1.0, float(u)))
        v_clamped = max(-1.0, min(1.0, float(v)))
        return z0 + crown * (1.0 - u_clamped ** 2) * (1.0 - v_clamped ** 2)

    def get_ergonomic_clearances(self, archetype: str) -> Dict[str, Any]:
        """Return human factor and circulation clearances (meters) for a given archetype."""
        domain = self.classify_domain(archetype)
        if domain == self.DOMAIN_ARCHITECTURE:
            return {
                "min_corridor_width": 1.00,
                "entry_door_clearance": 0.90,
                "stair_tread_depth": 0.28,
                "stair_riser_height": 0.175,
                "exterior_step_run": 0.30,
            }
        elif domain == self.DOMAIN_INTERIOR:
            return {
                "main_circulation_walkway": 0.90,
                "coffee_table_to_sofa_gap": 0.45,
                "dining_chair_pullout_space": 0.75,
                "kitchen_work_triangle_aisle": 1.05,
            }
        elif domain == self.DOMAIN_FURNITURE:
            return {
                "seat_height_range": (0.42, 0.46),
                "seat_depth_comfort": (0.55, 0.65),
                "armrest_above_seat": (0.18, 0.24),
                "table_knee_clearance": 0.68,
            }
        return {
            "driver_eye_height": 1.15,
            "pedal_reach_distance": 0.85,
            "ingress_egress_width": 0.80,
        }

    def generate_spatial_blueprint(self, query: str) -> Dict[str, Any]:
        """Generate a complete spatial blueprint enforcing the Anti-Boxy mandate."""
        domain = self.classify_domain(query)
        
        # Match nearest archetype
        resolved_key = "MODERN_VILLA"
        if domain == self.DOMAIN_ARCHITECTURE:
            resolved_key = "MODERN_VILLA" if "villa" in query.lower() else "RESIDENTIAL_HOUSE"
        elif domain == self.DOMAIN_INTERIOR:
            if "bed" in query.lower():
                resolved_key = "BEDROOM"
            elif "kitchen" in query.lower():
                resolved_key = "KITCHEN"
            else:
                resolved_key = "LIVING_ROOM"
        elif domain == self.DOMAIN_FURNITURE:
            if "chair" in query.lower() or "armchair" in query.lower():
                resolved_key = "ARMCHAIR_LOUNGE" if "armchair" in query.lower() or "lounge" in query.lower() else "DINING_CHAIR"
            elif "table" in query.lower() or "desk" in query.lower():
                resolved_key = "DINING_TABLE"
            else:
                resolved_key = "SOFA_3_SEATER"
        elif domain == self.DOMAIN_VEHICLE:
            resolved_key = "SUPERCAR"

        dims = self.get_dimensions(resolved_key)
        clearances = self.get_ergonomic_clearances(resolved_key)

        return {
            "query": query,
            "domain": domain,
            "archetype": resolved_key,
            "dimensions": dims,
            "clearances": clearances,
            "anti_boxy_mandate": {
                "zero_unfilleted_primitives": True,
                "minimum_wall_thickness": 0.20 if domain == self.DOMAIN_ARCHITECTURE else 0.10,
                "minimum_reveal_depth": 0.14 if domain == self.DOMAIN_ARCHITECTURE else 0.05,
                "cushion_loft_equation": "Z(u,v) = z0 + crown * (1 - u^2) * (1 - v^2)",
                "required_edge_treatment": "FILLET_OR_CHAMFER_MANDATORY",
            }
        }
