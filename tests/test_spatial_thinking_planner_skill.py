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
