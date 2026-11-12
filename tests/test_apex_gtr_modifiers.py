"""Unit tests for Apex GT-R Modifier Stack & Normal Hardening (Task 14)."""
import pytest
from scripts.generate_apex_gtr import (
    MODIFIER_FINISHING_SPECS,
    COLLECTION_HIERARCHY,
)


def test_modifier_specs_completeness():
    """Verify modifier finishing specifications include Bevel and WeightedNormal."""
    assert "bevel" in MODIFIER_FINISHING_SPECS
    assert "weighted_normal" in MODIFIER_FINISHING_SPECS

    bev = MODIFIER_FINISHING_SPECS["bevel"]
    assert bev["segments"] == 2
    assert bev["profile"] == 0.50
    assert bev["harden_normals"] is True

    wn = MODIFIER_FINISHING_SPECS["weighted_normal"]
    assert wn["keep_sharp"] is True


def test_required_component_count():
    """Verify all 12 modular component assemblies are registered."""
    all_components = []
    for cat, comps in COLLECTION_HIERARCHY.items():
        all_components.extend(comps)
    # 3 body + 4 aero + 2 glass/mirrors + 2 lighting + 4 wheels = 15 object instances
    assert len(all_components) == 15
