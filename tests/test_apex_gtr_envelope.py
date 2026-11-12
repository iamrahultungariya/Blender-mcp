"""Unit tests for Apex GT-R Concept dimension envelope and collection hierarchy."""
import pytest
from scripts.generate_apex_gtr import (
    APEX_GTR_ENVELOPE,
    COLLECTION_HIERARCHY,
    calculate_bounding_dimensions,
)


def test_apex_gtr_envelope_specs():
    """Verify exact blueprint dimensions from user reference sheet."""
    assert APEX_GTR_ENVELOPE["length"] == 4.610
    assert APEX_GTR_ENVELOPE["width"] == 1.870
    assert APEX_GTR_ENVELOPE["height"] == 1.180
    assert APEX_GTR_ENVELOPE["wheelbase"] == 2.700
    assert APEX_GTR_ENVELOPE["front_axle_y"] == 1.350
    assert APEX_GTR_ENVELOPE["rear_axle_y"] == -1.350


def test_apex_gtr_collection_hierarchy():
    """Verify required 12 modular component collections are defined."""
    expected_categories = [
        "01_Body_Structure",
        "02_Aero_Fascia",
        "03_Glass_and_Mirrors",
        "04_Lighting",
        "05_Wheels",
    ]
    for cat in expected_categories:
        assert cat in COLLECTION_HIERARCHY


def test_calculate_bounding_dimensions():
    """Verify bounding dimension helper math."""
    min_v = (-0.935, -2.305, 0.0)
    max_v = (0.935, 2.305, 1.180)
    dims = calculate_bounding_dimensions(min_v, max_v)
    assert pytest.approx(dims["length"], 0.001) == 4.610
    assert pytest.approx(dims["width"], 0.001) == 1.870
    assert pytest.approx(dims["height"], 0.001) == 1.180
