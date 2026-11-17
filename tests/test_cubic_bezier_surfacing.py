import pytest
import numpy as np

def test_cubic_bezier_evaluation_math():
    from blender_mcp.bmesh_toolkit import eval_cubic_bezier_curve

    p0 = np.array([0.0, 0.0, 0.0])
    p1 = np.array([0.0, 1.0, 2.0])
    p2 = np.array([0.0, 2.0, 2.0])
    p3 = np.array([0.0, 3.0, 0.0])

    curve = eval_cubic_bezier_curve(p0, p1, p2, p3, num_samples=17)
    assert len(curve) == 17
    # Start and end endpoints must match exactly
    np.testing.assert_allclose(curve[0], p0, atol=1e-5)
    np.testing.assert_allclose(curve[-1], p3, atol=1e-5)
    # Midpoint (t=0.5) must match Bernstein formula: 0.125*p0 + 0.375*p1 + 0.375*p2 + 0.125*p3 = [0, 1.5, 1.5]
    expected_mid = 0.125 * p0 + 0.375 * p1 + 0.375 * p2 + 0.125 * p3
    np.testing.assert_allclose(curve[8], expected_mid, atol=1e-5)

def test_vehicle_thinking_aerodynamic_windshield_curvature():
    from blender_mcp.vehicle_thinking import VehicleThinkingEngine

    engine = VehicleThinkingEngine()
    profile = engine.generate_van_chassis_profile()

    ws = np.array(profile["windshield_spline"])
    assert len(ws) >= 6
    # Non-linear check: If pure linear, second differences along Z/Y would be ~0.
    # In aerodynamic compound curvature, second difference must be non-zero!
    d2 = np.diff(ws, n=2, axis=0)
    assert np.max(np.abs(d2)) > 1e-4, "Windshield spline must have non-zero curvature (not straight linear segment)"
