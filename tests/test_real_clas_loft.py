import ast
import pytest
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_clas_loft_not_empty_stub():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # The old fake stub was literally:
    # mesh = bpy.data.meshes.new(name)
    # obj = bpy.data.objects.new(name, mesh)
    # return {"name": obj.name, "sections": len(sections), "resolution": resolution}
    
    assert "mesh.vertices.foreach_set" in content or "mesh.from_pydata" in content
    # Must actually use the sections parameter
    assert "for sec in sections" in content or "resampled_sections" in content

def test_numpy_loft_spline_math():
    from blender_mcp.kernel.clas_tensor_shaper import loft_spline_sections
    # 3 circular rings along Z
    num_pts = 8
    theta = np.linspace(0, 2*np.pi, num_pts, endpoint=False)
    sections = [
        np.column_stack([np.cos(theta), np.sin(theta), np.full(num_pts, z)])
        for z in [0.0, 1.0, 2.0]
    ]
    verts, quads, normals = loft_spline_sections(sections, resolution=16, closed=True)
    assert len(verts) == 3 * 16
    assert len(quads) == 2 * 16
    assert len(normals) == len(verts)
