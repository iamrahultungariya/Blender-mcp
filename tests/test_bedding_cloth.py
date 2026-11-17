import pytest

try:
    import bmesh
except ImportError:
    from luxury_bedroom.core.bmesh_utils import MockBMesh as bmesh

from luxury_bedroom.modules.bed_assembly import BedAssemblyBuilder
from luxury_bedroom.modules.bedding_cloth import BeddingClothBuilder
from luxury_bedroom.core.materials import MaterialLibrary


def test_bedding_cloth_generation():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    bed_builder = BedAssemblyBuilder(width=2.04, length=2.14)
    bed_info = bed_builder.build(bm, mat_lib)

    bedding_builder = BeddingClothBuilder()
    cloth_info = bedding_builder.build(bm, bed_info, mat_lib)

    assert cloth_info["pillows_count"] == 5  # 2 sleeping + 2 decorative + 1 lumbar
    assert cloth_info["chadar_draped"] is True
    assert "chadar_bounds" in cloth_info

    # Verify material tags are present
    mat_indices = {f.material_index for f in bm.faces}
    white_idx = mat_lib.get_index("LINEN_WHITE")
    accent_idx = mat_lib.get_index("LINEN_ACCENT")
    velvet_idx = mat_lib.get_index("UPHOLSTERY_VELVET")

    assert white_idx in mat_indices
    assert accent_idx in mat_indices
    assert velvet_idx in mat_indices

    # Total face count should show high-fidelity textile resolution
    assert len(bm.faces) > 200
    bm.free()


def test_pillow_elevation_above_mattress():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    bed_builder = BedAssemblyBuilder(width=2.0, length=2.1)
    bed_info = bed_builder.build(bm, mat_lib)

    bedding_builder = BeddingClothBuilder()
    cloth_info = bedding_builder.build(bm, bed_info, mat_lib)

    # All pillow vertices must be placed above or at the mattress top surface
    mattress_top_z = bed_info["mattress_top_z"]
    pillow_min_z = cloth_info["pillow_base_z"]
    assert pillow_min_z >= mattress_top_z - 0.05
    bm.free()
