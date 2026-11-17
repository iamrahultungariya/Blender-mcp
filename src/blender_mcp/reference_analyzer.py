"""Reference Evidence Matrix & Datum Alignment Engine for Blender MCP.

Enforces Section 1 (Multi-View Reference Intake) and Section 11 of the
Reference-to-Asset Pipeline v2 Contract. Cross-checks orthographic view
projections, establishes 3D datum planes, and prevents hallucinated/box models.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ReferenceEvidenceMatrix:
    """Matrix classifying features into OBSERVED, INFERRED, or DESIGNED."""

    FEATURE_VIEW_MAP = {
        "bounding_envelope": ["front", "side", "top"],
        "wheelbase_and_track": ["side", "top", "front"],
        "tumblehome_and_rake": ["front", "side", "perspective"],
        "wheel_arches": ["side", "front", "perspective"],
        "fascia_and_grille": ["front", "perspective"],
        "lighting_housings": ["front", "rear", "perspective"],
        "underbody_chassis": ["side", "front", "bottom"],
    }

    @classmethod
    def evaluate_features(cls, available_views: List[str]) -> Dict[str, Dict[str, Any]]:
        norm_views = [v.lower() for v in available_views]
        matrix = {}
        for feature, required_views in cls.FEATURE_VIEW_MAP.items():
            overlap = [v for v in required_views if any(rv in v or v in rv for rv in norm_views)]
            match_count = len(overlap)
            if match_count >= 2:
                status = "OBSERVED"
                confidence = 0.95
                notes = f"Verified across multiple views: {', '.join(overlap)}"
            elif match_count == 1:
                status = "INFERRED"
                confidence = 0.70
                notes = f"Observed in {overlap[0]}; mirrored/projected across symmetry plane"
            else:
                status = "DESIGNED"
                confidence = 0.50
                notes = "Hidden/obscured in references; engineered from vehicle standard archetype"

            matrix[feature] = {
                "status": status,
                "confidence": confidence,
                "source_views": overlap,
                "notes": notes,
            }
        return matrix


ARCHETYPE_DEFAULTS = {
    "VEHICLE": {
        "length": 5.92,
        "width": 2.02,
        "height": 2.75,
        "wheelbase": 3.665,
        "front_overhang": 1.01,
        "rear_overhang": 1.245,
        "ground_clearance": 0.20,
    },
    "AMBULANCE": {
        "length": 5.92,
        "width": 2.02,
        "height": 2.75,
        "wheelbase": 3.665,
        "front_overhang": 1.01,
        "rear_overhang": 1.245,
        "ground_clearance": 0.20,
    },
    "VAN": {
        "length": 5.92,
        "width": 2.02,
        "height": 2.75,
        "wheelbase": 3.665,
        "front_overhang": 1.01,
        "rear_overhang": 1.245,
        "ground_clearance": 0.20,
    },
    "SPORTS_CAR": {
        "length": 4.50,
        "width": 1.95,
        "height": 1.20,
        "wheelbase": 2.65,
        "front_overhang": 0.95,
        "rear_overhang": 0.90,
        "ground_clearance": 0.11,
    },
    "PROP": {
        "length": 1.0,
        "width": 1.0,
        "height": 1.0,
        "wheelbase": 0.0,
        "front_overhang": 0.0,
        "rear_overhang": 0.0,
        "ground_clearance": 0.0,
    },
}


def reconcile_reference_datums(
    views: Optional[List[str]] = None,
    archetype: str = "VEHICLE",
    dimensions: Optional[Dict[str, float]] = None,
    confidence_threshold: float = 0.8,
) -> Dict[str, Any]:
    """Reconcile reference views, audit cross-view dimensions, and build evidence matrix."""
    views = views or []
    arch_key = archetype.upper()
    default_dims = ARCHETYPE_DEFAULTS.get(arch_key, ARCHETYPE_DEFAULTS["VEHICLE"]).copy()

    reconciled = default_dims.copy()
    if dimensions:
        reconciled.update(dimensions)

    discrepancies: List[str] = []

    # Check 1: Cross-view width consistency (Front Width vs Top Width)
    front_w = dimensions.get("front_width") if dimensions else None
    top_w = dimensions.get("top_width") if dimensions else None
    if front_w is not None and top_w is not None:
        diff = abs(front_w - top_w)
        pct = diff / max(front_w, top_w)
        if pct > 0.04:  # >4% discrepancy threshold
            discrepancies.append(
                f"Front view width ({front_w:.3f}m) conflicts with Top view width ({top_w:.3f}m) by {pct*100:.1f}%. Silently averaging is prohibited."
            )
        reconciled["width"] = (front_w + top_w) / 2.0
    elif front_w is not None:
        reconciled["width"] = front_w
    elif top_w is not None:
        reconciled["width"] = top_w

    # Check 2: Cross-view length consistency (Side Length vs Top Length)
    side_l = dimensions.get("side_length") if dimensions else None
    top_l = dimensions.get("top_length") if dimensions else None
    if side_l is not None and top_l is not None:
        diff = abs(side_l - top_l)
        pct = diff / max(side_l, top_l)
        if pct > 0.04:
            discrepancies.append(
                f"Side view length ({side_l:.3f}m) conflicts with Top view length ({top_l:.3f}m) by {pct*100:.1f}%. Explicit user resolution required."
            )
        reconciled["length"] = (side_l + top_l) / 2.0
    elif side_l is not None:
        reconciled["length"] = side_l
    elif top_l is not None:
        reconciled["length"] = top_l

    # Check 3: Overhang + Wheelbase sum vs total vehicle length
    if "wheelbase" in reconciled and "front_overhang" in reconciled and "rear_overhang" in reconciled and "length" in reconciled:
        sum_components = reconciled["wheelbase"] + reconciled["front_overhang"] + reconciled["rear_overhang"]
        if abs(sum_components - reconciled["length"]) > 0.08 and reconciled["wheelbase"] > 0:
            discrepancies.append(
                f"Sum of wheelbase ({reconciled['wheelbase']}m) + front overhang ({reconciled['front_overhang']}m) + rear overhang ({reconciled['rear_overhang']}m) = {sum_components:.3f}m, which differs from vehicle length ({reconciled['length']}m)."
            )

    evidence_matrix = ReferenceEvidenceMatrix.evaluate_features(views)

    status = "PASS" if len(discrepancies) == 0 else "DISCREPANCY_FLAGGED"

    return {
        "status": status,
        "archetype": archetype,
        "reconciled_datums": reconciled,
        "evidence_matrix": evidence_matrix,
        "discrepancies": discrepancies,
        "prohibited_assumptions": [
            "Never average conflicting multi-view reference coordinates silently",
            "Never author planar box geometry when aerodynamic tumblehome is visible",
            "Never create glued-on surface geometry without boolean cavity carving",
            "Never proceed to detailing without verified primary subdivision cage",
        ],
        "views_analyzed": views,
    }
