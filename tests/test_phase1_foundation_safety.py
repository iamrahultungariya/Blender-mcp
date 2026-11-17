import pytest
import os
import shutil
from pathlib import Path
from blender_mcp.foundation import (
    OperationRisk,
    format_tool_response,
    validate_numeric_range,
    validate_object_exists
)
from blender_mcp.checkpoint_manager import (
    create_checkpoint,
    list_checkpoints,
    restore_checkpoint,
    delete_checkpoint,
    get_checkpoint_dir
)


@pytest.fixture(autouse=True)
def clean_checkpoints_dir(tmp_path, monkeypatch):
    test_dir = tmp_path / "test_checkpoints"
    monkeypatch.setenv("BLENDER_CHECKPOINT_DIR", str(test_dir))
    import blender_mcp.checkpoint_manager as cm
    cm.DEFAULT_CHECKPOINT_DIR = test_dir
    yield
    if test_dir.exists():
        shutil.rmtree(test_dir, ignore_errors=True)


def test_foundation_structured_response():
    resp = format_tool_response(
        tool_name="test_tool",
        result={"val": 42},
        success=True,
        warnings=["minor notice"],
        risk=OperationRisk.NON_DESTRUCTIVE
    )
    assert resp["success"] is True
    assert resp["tool"] == "test_tool"
    assert resp["risk"] == "NON_DESTRUCTIVE"
    assert resp["result"]["val"] == 42
    assert "minor notice" in resp["warnings"]
    assert "operation_id" in resp
    assert "timestamp" in resp


def test_foundation_numeric_validation():
    ok, err = validate_numeric_range(0.5, "roughness", min_val=0.0, max_val=1.0)
    assert ok is True
    assert err is None

    ok, err = validate_numeric_range(1.5, "roughness", min_val=0.0, max_val=1.0)
    assert ok is False
    assert "exceed 1.0" in err


def test_checkpoint_lifecycle():
    # 1. Create checkpoint
    res = create_checkpoint(label="pre_boolean_cut", description="Snapshot before cutting hood")
    assert res["success"] is True
    cp_id = res["result"]["checkpoint_id"]
    assert cp_id.startswith("cp_")

    # 2. List checkpoints
    listed = list_checkpoints()
    assert listed["success"] is True
    assert listed["result"]["count"] == 1
    item = listed["result"]["checkpoints"][0]
    assert item["label"] == "pre_boolean_cut"
    assert item["file_exists"] is True

    # 3. Restore checkpoint
    restored = restore_checkpoint("pre_boolean_cut")
    assert restored["success"] is True
    assert restored["risk"] == "DESTRUCTIVE"

    # 4. Delete checkpoint
    deleted = delete_checkpoint(cp_id)
    assert deleted["success"] is True
    assert cp_id == deleted["result"]["deleted_checkpoint_id"]

    # 5. Verify list is empty
    listed2 = list_checkpoints()
    assert listed2["result"]["count"] == 0
