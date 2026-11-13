import pytest

try:
    import bmesh
except ImportError:
    from luxury_bedroom.core.bmesh_utils import MockBMesh as bmesh

from luxury_bedroom.prefabs.bed_hero import HeroBedBuilder
from luxury_bedroom.core.materials import MaterialLibrary


def test_hero_bed_construction():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    builder = HeroBedBuilder()
    info = builder.build(bm, mat_lib)

    assert info["pillows_count"] == 6
    assert info["has_bed_runner"] is True
    assert info["has_winged_headboard"] is True
    assert info["mattress_top_z"] > 0.50
    assert "bed_width" in info
    assert "bed_length" in info

    # Ensure required materials are assigned
    assigned_mats = {f.material_index for f in bm.faces}
    boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")
    white_idx = mat_lib.get_index("LINEN_WHITE")
    charcoal_idx = mat_lib.get_index("CHARCOAL_PLEAT")

    assert boucle_idx in assigned_mats
    assert white_idx in assigned_mats
    assert charcoal_idx in assigned_mats

    # High geometric resolution verification
    assert len(bm.faces) > 500
    bm.free()


def test_hero_bed_pillow_stacking():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    builder = HeroBedBuilder()
    info = builder.build(bm, mat_lib)

    # 6 pillows = 2 white sleeping + 2 charcoal accent + 2 front lumbar
    assert info["pillows_breakdown"]["sleeping"] == 2
    assert info["pillows_breakdown"]["accent"] == 2
    assert info["pillows_breakdown"]["lumbar"] == 2
    bm.free()
