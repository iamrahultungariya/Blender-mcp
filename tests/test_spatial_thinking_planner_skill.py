import os
import re
from pathlib import Path
import pytest

SKILL_DIR = Path("skills/blender-spatial-thinking-planner")

def test_skill_directory_and_frontmatter():
    skill_file = SKILL_DIR / "SKILL.md"
    assert skill_file.exists(), "SKILL.md must exist in blender-spatial-thinking-planner"
    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---"), "SKILL.md must have YAML frontmatter"
    assert "name: blender-spatial-thinking-planner" in content
    assert "description:" in content

def test_playbook_references_exist():
    refs = [
        "references/spatial-deconstruction-and-geometry-allocation-playbook.md",
        "references/mcp-and-blender-tool-selection-matrix.md",
        "references/modular-code-architecture-playbook.md",
        "templates/spatial-execution-plan-template.md",
    ]
    for rel_path in refs:
        target = SKILL_DIR / rel_path
        assert target.exists(), f"Reference file {rel_path} must exist"
        assert target.stat().st_size > 200, f"Reference file {rel_path} must have substantial content"

def test_spatial_thinking_rules_content():
    skill_file = SKILL_DIR / "SKILL.md"
    assert skill_file.exists()
    content = skill_file.read_text(encoding="utf-8")
    # Check 6 phases
    assert "Phase 1: Multi-Angle Reference & Domain Deconstruction" in content
    assert "Phase 2: Physical & Material Classification" in content
    assert "Phase 3: Geometry & Budget Allocation Matrix" in content
    assert "Phase 4: Live MCP & Native Tool Selection Matrix" in content
    assert "Phase 5: Socratic Clarification & Inquiry Gate" in content
    assert "Phase 6: Modular Code Architecture Mandate" in content
    # Check 9 video principles codified
    assert "Primary -> Secondary -> Tertiary" in content
    assert "Shrinkwrap" in content
    assert "create_cushioned_profile" in content
    assert "create_architectural_wall" in content
    assert "create_profile_sweep_molding" in content
    assert "create_bezier_tube" in content
    assert "setup_subdivision_cage" in content

def test_geometry_allocation_playbook_content():
    playbook = SKILL_DIR / "references/spatial-deconstruction-and-geometry-allocation-playbook.md"
    content = playbook.read_text(encoding="utf-8")
    # Mathematical crown loft formula
    assert "h_{crown}" in content or "crown_height" in content
    # 4 classes
    assert "Class A: Architectural Envelope" in content
    assert "Class B: Precision Hard CAD" in content
    assert "Class C: Organic Soft Goods" in content
    assert "Class D: Slender Curved Extrusions" in content
    # Pillow anatomy
    assert "Perimeter Seam" in content
    assert "Pinched Corners" in content
    assert "Subdivision Cage" in content

def test_tool_matrix_playbook_content():
    matrix = SKILL_DIR / "references/mcp-and-blender-tool-selection-matrix.md"
    content = matrix.read_text(encoding="utf-8")
    # Live tools
    assert "create_architectural_wall" in content
    assert "create_profile_sweep_molding" in content
    assert "create_cushioned_profile" in content
    assert "setup_subdivision_cage" in content
    assert "create_bezier_tube" in content
    assert "audit_mesh_topology" in content
    # Video principles
    assert "Shrinkwrap Shading Fix" in content
    assert "LoopTools" in content
    assert "Alt + S" in content or "Alt+S" in content
    assert "Alt + D" in content or "Alt+D" in content

def test_modular_architecture_playbook_content():
    playbook = SKILL_DIR / "references/modular-code-architecture-playbook.md"
    content = playbook.read_text(encoding="utf-8")
    # Anti-monolithic constraints
    assert "250 lines" in content or "250 lines of code" in content
    assert "core/materials.py" in content
    assert "core/mesh_utils.py" in content
    assert "prefabs/" in content
    assert "main.py" in content
    assert "Single-Buffer BMesh Merging" in content
