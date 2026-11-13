import pytest

try:
    import bmesh
except ImportError:
    from luxury_bedroom.core.bmesh_utils import MockBMesh as bmesh

from luxury_bedroom.core.materials import MaterialLibrary
from luxury_bedroom.core.bmesh_utils import (
    create_pleated_surface,
    create_lathe_mesh,
    create_cushion_loft,
)


def test_reference_materials_palette():
    mat_lib = MaterialLibrary()
    required = [
        "TRAVERTINE_TILES",
        "WALNUT_WOOD",
        "TAUPE_BOUCLE",
        "LINEN_WHITE",
        "CHARCOAL_PLEAT",
        "BRUSHED_BRASS",
        "MATTE_BLACK_METAL",
        "TINTED_BRONZE_GLASS",
        "SHEER_WHITE",
        "LED_WARM_2700K",
    ]
    names = mat_lib.get_material_names()
    for req in required:
        assert req in names, f"Missing required reference material: {req}"
        idx = mat_lib.get_index(req)
        assert isinstance(idx, int)
        assert idx >= 0


def test_create_pleated_surface():
    bm = bmesh.new()
    create_pleated_surface(
        bm,
        width=1.2,
        length=2.4,
        pleat_freq=8.0,
        pleat_amp=0.03,
        subdivisions_x=24,
        subdivisions_y=16,
        mat_index=4,
    )
    assert len(bm.verts) >= (25 * 17)
    assert len(bm.faces) >= (24 * 16)
    for f in bm.faces:
        assert f.material_index == 4
    bm.free()


def test_create_lathe_mesh():
    bm = bmesh.new()
    # Simple pedestal profile: [(r, z)]
    profile = [(0.2, 0.0), (0.15, 0.05), (0.05, 0.3), (0.05, 0.5), (0.25, 0.55)]
    create_lathe_mesh(bm, profile=profile, segs=16, center=(0, 0, 0), mat_index=5)
    assert len(bm.verts) >= (len(profile) * 16)
    assert len(bm.faces) >= ((len(profile) - 1) * 16)
    for f in bm.faces:
        assert f.material_index == 5
    bm.free()
