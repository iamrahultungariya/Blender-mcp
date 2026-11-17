import pytest
from pathlib import Path

def test_reference_analyzer_module_exists():
    from blender_mcp import reference_analyzer
    assert hasattr(reference_analyzer, "reconcile_reference_datums")
    assert hasattr(reference_analyzer, "ReferenceEvidenceMatrix")

def test_reconcile_reference_datums_consistent():
    from blender_mcp.reference_analyzer import reconcile_reference_datums

    dimensions = {
        "length": 5.92,
        "width": 2.02,
        "height": 2.75,
        "wheelbase": 3.665,
        "front_overhang": 1.01,
        "rear_overhang": 1.245,
    }
    views = ["front", "side", "top", "perspective"]
    report = reconcile_reference_datums(views=views, archetype="VEHICLE", dimensions=dimensions)

    assert report["status"] == "PASS"
    assert "evidence_matrix" in report
    matrix = report["evidence_matrix"]
    assert "bounding_envelope" in matrix
    assert matrix["bounding_envelope"]["status"] in ["OBSERVED", "INFERRED"]
    assert report["reconciled_datums"]["length"] == 5.92
    assert len(report["discrepancies"]) == 0

def test_reconcile_reference_datums_flags_conflict():
    from blender_mcp.reference_analyzer import reconcile_reference_datums

    # Front width 2.02 vs Top width 2.40 -> >15% discrepancy
    conflicting_dims = {
        "length": 5.92,
        "front_width": 2.02,
        "top_width": 2.45,
        "height": 2.75,
        "wheelbase": 3.665,
    }
    report = reconcile_reference_datums(
        views=["front", "top"],
        archetype="VEHICLE",
        dimensions=conflicting_dims
    )

    assert report["status"] == "DISCREPANCY_FLAGGED"
    assert len(report["discrepancies"]) > 0
    assert any("width" in d.lower() for d in report["discrepancies"])

def test_server_reference_analyzer_tool_exposed():
    from blender_mcp import server
    assert hasattr(server, "reconcile_reference_datums")
