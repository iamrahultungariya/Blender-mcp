import pytest
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_gbuffer_quad_not_fake_single_shot():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # The old fake stub was:
    # res = self.get_viewport_screenshot(max_size=1024, filepath=filepath)
    # res["quadrant_layout"] = ["top", "front", "side", "perspective"]
    # return res

    assert 'res["quadrant_layout"] = ["top", "front", "side", "perspective"]' not in content
    # Must compute or tile 4 quadrant views
    assert "tile_quadrants" in content or "draw_quad_view" in content or "sub_w" in content or "quadrants" in content

def test_tile_quadrants_numpy():
    from blender_mcp.bmesh_toolkit import tile_quadrant_buffers

    # Create 4 distinct test images (2x2 pixels each)
    q1 = np.full((10, 10, 4), 1.0, dtype=np.float32)  # White
    q2 = np.full((10, 10, 4), 0.5, dtype=np.float32)  # Gray
    q3 = np.full((10, 10, 4), 0.2, dtype=np.float32)  # Dark Gray
    q4 = np.full((10, 10, 4), 0.0, dtype=np.float32)  # Black

    tiled = tile_quadrant_buffers(q1, q2, q3, q4)
    # Tiled result should be (20, 20, 4)
    assert tiled.shape == (20, 20, 4)
    # Verify quadrants are preserved in the 4 corners
    np.testing.assert_allclose(tiled[:10, :10], q1)
    np.testing.assert_allclose(tiled[:10, 10:], q2)
    np.testing.assert_allclose(tiled[10:, :10], q3)
    np.testing.assert_allclose(tiled[10:, 10:], q4)
