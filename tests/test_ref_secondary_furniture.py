import pytest

try:
    import bmesh
except ImportError:
    from luxury_bedroom.core.bmesh_utils import MockBMesh as bmesh

from luxury_bedroom.prefabs.nightstands import NightstandsBuilder
from luxury_bedroom.prefabs.bench_ottoman import OttomanBenchBuilder
from luxury_bedroom.prefabs.lounge_corner import LoungeCornerBuilder
from luxury_bedroom.core.materials import MaterialLibrary


def test_secondary_furnishings():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    bed_datum = {
        "bed_width": 2.12,
        "bed_length": 2.22,
        "headboard_center": (0.0, 1.2, 0.7),
        "mattress_top_z": 0.65,
    }

    ns_info = NightstandsBuilder().build(bm, bed_datum, mat_lib)
    bench_info = OttomanBenchBuilder().build(bm, bed_datum, mat_lib)
    lounge_info = LoungeCornerBuilder().build(bm, mat_lib)

    assert ns_info["dome_lamps_count"] == 2
    assert ns_info["has_tabletop_plant"] is True
    assert bench_info["cushions_count"] == 2
    assert bench_info["bench_placed"] is True
    assert lounge_info["armchair_placed"] is True
    assert lounge_info["side_table_placed"] is True
    assert lounge_info["floor_lamp_placed"] is True

    # Ensure required materials are assigned
    assigned_mats = {f.material_index for f in bm.faces}
    walnut_idx = mat_lib.get_index("WALNUT_WOOD")
    brass_idx = mat_lib.get_index("BRUSHED_BRASS")
    black_idx = mat_lib.get_index("MATTE_BLACK_METAL")
    led_idx = mat_lib.get_index("LED_WARM_2700K")
    boucle_idx = mat_lib.get_index("TAUPE_BOUCLE")

    assert walnut_idx in assigned_mats
    assert brass_idx in assigned_mats
    assert black_idx in assigned_mats
    assert led_idx in assigned_mats
    assert boucle_idx in assigned_mats

    # High geometric detail check
    assert len(bm.faces) > 400
    bm.free()


def test_nightstand_and_bench_positioning():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    bed_datum = {
        "bed_width": 2.12,
        "bed_length": 2.22,
        "headboard_center": (0.0, 1.2, 0.7),
        "mattress_top_z": 0.65,
    }

    ns_info = NightstandsBuilder().build(bm, bed_datum, mat_lib)
    bench_info = OttomanBenchBuilder().build(bm, bed_datum, mat_lib)

    # Left and right nightstand positions should be symmetrical
    left_x, _, _ = ns_info["left_stand_origin"]
    right_x, _, _ = ns_info["right_stand_origin"]
    assert abs(left_x + right_x) < 0.001
    assert left_x < -1.0
    assert right_x > 1.0

    # Ottoman bench must be placed at the foot of the bed (y < 0)
    _, bench_y, _ = bench_info["bench_origin"]
    assert bench_y < 0.0
    bm.free()
