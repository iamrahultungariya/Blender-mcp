import pytest
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_sdf_space_carve_not_fake_cube():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # The old fake stub was:
    # x = np.linspace(-1, 1, 2)
    # verts = [(float(i), float(j), float(k)) for i in x for j in x for k in x]
    # faces = [...]
    # mesh.from_pydata(verts, [], faces)
    
    assert "x = np.linspace(-1, 1, 2)" not in content
    # Must use front_png or masks
    assert "front_png" in content
    assert "extract_visual_hull_mesh" in content or "occupancy" in content

def test_visual_hull_extraction_numpy():
    from blender_mcp.kernel.clas_tensor_shaper import extract_visual_hull_mesh

    # Create synthetic circle silhouettes for front and side (forming a cylinder or sphere)
    R = 16
    yy, xx = np.mgrid[:R, :R]
    center = (R - 1) / 2.0
    circle = ((xx - center)**2 + (yy - center)**2) <= (center * 0.8)**2

    verts, quads = extract_visual_hull_mesh(
        front_mask=circle,
        side_mask=circle,
        top_mask=None,
        resolution=R
    )

    # Must produce actual 3D geometry with more than 8 vertices and 6 faces!
    assert len(verts) > 50
    assert len(quads) > 50
    # Every quad must have 4 vertex indices
    assert quads.shape[1] == 4
    # All vertex indices must be within range
    assert np.all(quads >= 0) and np.all(quads < len(verts))
