import pytest
import numpy as np

def test_vehicle_thinking_imports():
    from blender_mcp import vehicle_thinking
    assert hasattr(vehicle_thinking, "VehicleThinkingEngine")

def test_archetype_proportions_ambulance_van():
    from blender_mcp.vehicle_thinking import VehicleThinkingEngine
    engine = VehicleThinkingEngine()
    prop = engine.get_archetype_proportions("AMBULANCE_VAN")
    assert prop["length"] >= 5.0
    assert prop["width"] >= 1.9
    assert prop["height"] >= 2.4
    assert "wheelbase" in prop
    assert "front_overhang" in prop
    assert "rear_overhang" in prop
    # Wheelbase should be between 55% and 68% of total length
    assert 0.55 <= (prop["wheelbase"] / prop["length"]) <= 0.68

def test_aerodynamic_curvatures_ambulance():
    from blender_mcp.vehicle_thinking import VehicleThinkingEngine
    engine = VehicleThinkingEngine()
    curv = engine.get_aerodynamic_curvatures("AMBULANCE_VAN")
    # Hood must have a non-zero downward slope angle (at least 20 deg)
    assert curv["hood_rake_deg"] >= 20.0
    # Windshield must rake backward (at least 35 deg)
    assert curv["windshield_rake_deg"] >= 35.0
    # Windshield sagitta must be positive (curved, not flat)
    assert curv["windshield_curvature_sagitta"] > 0.03
    # Side glass tumblehome must tilt inward
    assert 3.0 <= curv["tumblehome_deg"] <= 12.0
    # Roof blister arc must exist for high roof
    assert curv["roof_blister_height"] > 0.1

def test_generate_van_chassis_profile():
    from blender_mcp.vehicle_thinking import VehicleThinkingEngine
    engine = VehicleThinkingEngine()
    profile = engine.generate_van_chassis_profile(length=5.9, width=2.05, height=2.75)
    
    assert "hood_spline" in profile
    assert "windshield_spline" in profile
    assert "roof_spline" in profile
    assert "wheel_arches" in profile
    assert "beltline_z" in profile
    
    # Check that hood slopes down toward front (+Y)
    hood = np.array(profile["hood_spline"])
    assert hood[0, 1] > hood[-1, 1]  # Front Y is greater than cowl Y
    assert hood[0, 2] < hood[-1, 2]  # Front Z is lower than cowl Z

def test_get_decal_and_lighting_spec():
    from blender_mcp.vehicle_thinking import VehicleThinkingEngine
    engine = VehicleThinkingEngine()
    spec = engine.get_decal_and_lighting_spec("AMBULANCE_VAN")
    assert "front_lightbar" in spec
    assert "rear_pods" in spec
    assert "star_of_life" in spec
    assert "chevron_stripes" in spec
    assert spec["front_lightbar"]["length"] > 1.0
