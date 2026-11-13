"""Tests for the Blender MCP Intelligence Triad Skills System (Skill 01, 02, 03)."""
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


def test_preproduction_intelligence_skill_exists():
    """Verify Skill 01 (blender-preproduction-intelligence) exists with complete templates and references."""
    skill_dir = SKILLS_DIR / "blender-preproduction-intelligence"
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists(), "Skill 01 SKILL.md missing"

    content = skill_file.read_text(encoding="utf-8")
    assert "name: blender-preproduction-intelligence" in content
    assert "Pre-Production Brief" in content
    assert "blender-artist-workflow" in content

    # Verify supporting references and templates
    playbook = skill_dir / "references" / "preproduction-research-and-decision-playbook.md"
    protocol = skill_dir / "references" / "research-and-evidence-protocol.md"
    template = skill_dir / "templates" / "pre-production-brief.md"

    assert playbook.exists(), "preproduction playbook missing"
    assert protocol.exists(), "research protocol missing"
    assert template.exists(), "pre-production-brief template missing"


def test_visual_reference_intelligence_skill_exists():
    """Verify Skill 02 (blender-visual-reference-intelligence) exists with complete templates and references."""
    skill_dir = SKILLS_DIR / "blender-visual-reference-intelligence"
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists(), "Skill 02 SKILL.md missing"

    content = skill_file.read_text(encoding="utf-8")
    assert "name: blender-visual-reference-intelligence" in content
    assert "Visual Reference Intelligence" in content

    # Verify supporting references and templates
    playbook = skill_dir / "references" / "visual-reference-analysis-playbook.md"
    template = skill_dir / "templates" / "visual-reference-analysis-report.md"

    assert playbook.exists(), "visual reference playbook missing"
    assert template.exists(), "visual-reference-analysis-report template missing"

