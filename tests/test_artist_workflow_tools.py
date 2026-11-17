import pytest
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_dispatch_artist_workflow_commands():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "create_bezier_tube" in content
    assert "setup_subdivision_cage" in content
    assert "crop_reference_region" in content
    assert "get_component_tree" in content

def test_component_tree_decomposition():
    from blender_mcp.bmesh_toolkit import get_component_tree

    tree = get_component_tree("VEHICLE")
    assert "systems" in tree
    systems = tree["systems"]
    assert "body_shell" in systems
    assert "aerodynamics" in systems
    assert "lighting" in systems
    assert "wheel_assembly" in systems
    assert "secondary_trim" in systems

    # Each component should declare its modeling strategy
    body = systems["body_shell"]
    assert "strategy" in body
    assert body["strategy"] in ["subdivision_cage", "loft", "bezier_curve"]

def test_crop_reference_region_pure_numpy():
    from blender_mcp.bmesh_toolkit import crop_image_array

    # Create synthetic 100x100 RGB image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[20:60, 30:70] = 255 # White box

    # Normalized box: [ymin, xmin, ymax, xmax]
    box = [0.2, 0.3, 0.6, 0.7]
    cropped = crop_image_array(img, box)
    assert cropped.shape == (40, 40, 3)
    assert np.all(cropped == 255)

def test_bezier_tube_points_math():
    from blender_mcp.bmesh_toolkit import calculate_spline_normals_and_lengths

    # 3 points along a line
    points = [[0, 0, 0], [0, 1, 0], [0, 2, 0]]
    lengths, tangents = calculate_spline_normals_and_lengths(points)
    assert len(lengths) == 3
    assert lengths[-1] == pytest.approx(2.0)
    # Tangents should point along +Y
    np.testing.assert_allclose(tangents[1], [0, 1, 0], atol=1e-5)
