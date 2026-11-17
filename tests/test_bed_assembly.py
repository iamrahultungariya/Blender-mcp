import pytest

try:
    import bmesh
except ImportError:
    from luxury_bedroom.core.bmesh_utils import MockBMesh as bmesh

from luxury_bedroom.modules.bed_assembly import BedAssemblyBuilder
from luxury_bedroom.core.materials import MaterialLibrary


def test_bed_assembly_construction():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    builder = BedAssemblyBuilder(width=2.04, length=2.14, headboard_height=1.30)
    info = builder.build(bm, mat_lib)

    assert "mattress_top_z" in info
    assert "headboard_center" in info
    assert "bed_width" in info
    assert "bed_length" in info
    assert info["mattress_top_z"] > 0.45
    assert len(bm.verts) > 100
    assert len(bm.faces) > 50

    # Ensure multiple materials are assigned (Walnut frame + Velvet headboard + Linen mattress)
    assigned_mats = {f.material_index for f in bm.faces}
    walnut_idx = mat_lib.get_index("WALNUT_WOOD")
    velvet_idx = mat_lib.get_index("UPHOLSTERY_VELVET")
    linen_idx = mat_lib.get_index("LINEN_WHITE")

    assert walnut_idx in assigned_mats
    assert velvet_idx in assigned_mats
    assert linen_idx in assigned_mats
    bm.free()


def test_bed_assembly_dimensions_and_datums():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    builder = BedAssemblyBuilder(width=2.0, length=2.1, headboard_height=1.2)
    info = builder.build(bm, mat_lib)

    assert info["bed_width"] == 2.0
    assert info["bed_length"] == 2.1
    # Headboard should be positioned at the head (y > 0)
    assert info["headboard_center"][1] > 0
    bm.free()
