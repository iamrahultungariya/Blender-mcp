import pytest

try:
    import bmesh
except ImportError:
    from luxury_bedroom.core.bmesh_utils import MockBMesh as bmesh

from luxury_bedroom.prefabs.media_wall import MediaWallBuilder
from luxury_bedroom.prefabs.wardrobe import WardrobeBuilder
from luxury_bedroom.prefabs.window_curtains import WindowCurtainsBuilder
from luxury_bedroom.core.materials import MaterialLibrary


def test_casework_and_drapes():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()

    media_info = MediaWallBuilder().build(bm, mat_lib)
    wardrobe_info = WardrobeBuilder().build(bm, mat_lib)
    curtain_info = WindowCurtainsBuilder().build(bm, mat_lib)

    assert media_info["tv_mounted"] is True
    assert media_info["credenza_placed"] is True
    assert wardrobe_info["doors_count"] == 4
    assert wardrobe_info["wardrobe_placed"] is True
    assert curtain_info["double_track_active"] is True
    assert curtain_info["curtains_placed"] is True

    # Material assignments check
    assigned_mats = {f.material_index for f in bm.faces}
    walnut_idx = mat_lib.get_index("WALNUT_WOOD")
    glass_idx = mat_lib.get_index("TINTED_BRONZE_GLASS")
    sheer_idx = mat_lib.get_index("SHEER_WHITE")
    charcoal_idx = mat_lib.get_index("CHARCOAL_PLEAT")
    black_idx = mat_lib.get_index("MATTE_BLACK_METAL")

    assert walnut_idx in assigned_mats
    assert glass_idx in assigned_mats
    assert sheer_idx in assigned_mats
    assert charcoal_idx in assigned_mats
    assert black_idx in assigned_mats

    # High geometric resolution check
    assert len(bm.faces) > 500
    bm.free()


def test_media_and_wardrobe_dimensions():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()

    media_info = MediaWallBuilder().build(bm, mat_lib)
    wardrobe_info = WardrobeBuilder().build(bm, mat_lib)

    assert media_info["credenza_width"] >= 2.0
    assert media_info["tv_screen_diagonal_inches"] >= 60.0
    assert wardrobe_info["doors_count"] == 4
    assert wardrobe_info["wardrobe_height"] >= 2.5
    bm.free()
