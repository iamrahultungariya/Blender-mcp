"""Phase Gate & Execution Validator for Blender MCP.

Enforces Section 14 (Phase Gate Checklist & Enforcement Summary) of the
Reference-to-Asset Pipeline v2 Contract. Prevents skipping critical stages
(e.g. jumping directly to detailing before primary form sub-d cage is verified).
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

PHASE_METADATA = {
    1: {
        "name": "Multi-View Reference Intake & Datum Alignment",
        "required_evidence": ["datums_reconciled", "evidence_matrix_compiled"],
        "description": "Establish orthographic datum planes (L, W, H, wheelbase). Classify features into OBSERVED/INFERRED/DESIGNED.",
    },
    2: {
        "name": "Component Breakdown & Modeling Strategy Selection",
        "required_evidence": ["component_strategies"],
        "description": "Deconstruct model into functional assemblies and map each to Sub-D, Boolean/Bevel, Curve, or Sculpt.",
    },
    3: {
        "name": "Primary Form Sub-D Cage & Visual Hull Carving",
        "required_evidence": ["specular_clay_verified", "topology_passed"],
        "description": "Author low-poly quad cage with Catmull-Clark sub-d. Pass specular reflection clay test without dents or pinching.",
    },
    4: {
        "name": "Secondary Assemblies & Precision Cutouts",
        "required_evidence": ["wheelhouse_recessed", "cutouts_carved"],
        "description": "Recess wheel arches with inner liner depth. Carve window/door panel cutouts via boolean difference or inset.",
    },
    5: {
        "name": "Detailing, Mechanical Hardware & Accessories",
        "required_evidence": ["hero_depth_verified"],
        "description": "Model hero assemblies with genuine 3D depth (>2cm). Angled radiator slats, multi-element light housings.",
    },
    6: {
        "name": "Multi-Material PBR Shading, Decals & Studio QA Gate",
        "required_evidence": ["materials_assigned", "studio_render_verified"],
        "description": "Tag face material indices for automotive clearcoat, glass, plastics. Render 4-quadrant studio turnaround.",
    },
}

VALID_STRATEGIES = {"subdivision_cage", "boolean_bevel", "bezier_curve", "sculpt_and_bake"}

# Bidirectional alias mapping from Geometry Engineering skill (G0-G6) to pipeline phases (1-6)
GATE_ALIAS_MAP: Dict[str, int] = {
    "G0": 1,
    "G1": 1,
    "PHASE 1": 1,
    "PHASE1": 1,
    "STAGE 1": 1,
    "G2": 2,
    "PHASE 2": 2,
    "PHASE2": 2,
    "STAGE 2": 2,
    "G3": 3,
    "PHASE 3": 3,
    "PHASE3": 3,
    "STAGE 3": 3,
    "G4": 4,
    "PHASE 4": 4,
    "PHASE4": 4,
    "STAGE 4": 4,
    "G5": 5,
    "PHASE 5": 5,
    "PHASE5": 5,
    "STAGE 5": 5,
    "G6": 6,
    "PHASE 6": 6,
    "PHASE6": 6,
    "STAGE 6": 6,
}


def resolve_phase_id(phase_id: Union[int, str]) -> int:
    """Resolve integer phase_id or string aliases ('G1'-'G6', 'Phase 1', etc.) to 1-6."""
    if isinstance(phase_id, int):
        return phase_id
    if isinstance(phase_id, str):
        cleaned = phase_id.strip().upper()
        if cleaned in GATE_ALIAS_MAP:
            return GATE_ALIAS_MAP[cleaned]
        try:
            return int(cleaned)
        except ValueError:
            pass
    return -1


class PhaseGateManager:
    """State machine governing 6-phase reference-to-asset execution with persistence."""

    def __init__(self, state_file: Optional[Union[Path, str]] = None) -> None:
        self.state_file: Optional[Path] = Path(state_file) if state_file else None
        self.phases: Dict[int, Dict[str, Any]] = {}
        self.reset(save=False)
        if self.state_file and self.state_file.exists():
            self.load_state()

    def save_state(self, filepath: Optional[Union[Path, str]] = None) -> bool:
        """Persist active pipeline phase states to JSON disk storage."""
        target = Path(filepath) if filepath else self.state_file
        if not target:
            return False
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "version": 2,
                "saved_at": time.time(),
                "phases": {str(k): v for k, v in self.phases.items()},
            }
            target.write_text(json.dumps(data, indent=2), encoding="utf-8")
            return True
        except Exception:
            return False

    def load_state(self, filepath: Optional[Union[Path, str]] = None) -> bool:
        """Load pipeline phase states from JSON disk storage."""
        target = Path(filepath) if filepath else self.state_file
        if not target or not target.exists():
            return False
        try:
            data = json.loads(target.read_text(encoding="utf-8"))
            saved_phases = data.get("phases", {})
            for k, v in saved_phases.items():
                p_id = int(k)
                if p_id in PHASE_METADATA:
                    self.phases[p_id] = v
            return True
        except Exception:
            return False

    def reset(self, save: bool = True) -> None:
        """Reset all phases to initial unexecuted state."""
        self.phases = {}
        for p_id, meta in PHASE_METADATA.items():
            self.phases[p_id] = {
                "phase_id": p_id,
                "name": meta["name"],
                "status": "NOT_STARTED",
                "verified_at": None,
                "evidence": {},
                "notes": "",
            }
        if save and self.state_file:
            self.save_state()

    def validate_gate(self, phase_id: Union[int, str], evidence: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate whether a phase meets all acceptance criteria to pass."""
        p_id = resolve_phase_id(phase_id)
        if p_id not in PHASE_METADATA:
            return {
                "status": "ERROR",
                "error": f"Invalid phase_id: '{phase_id}'. Must be 1 to 6 or valid alias ('G0'-'G6', 'Phase 1'-'Phase 6').",
            }

        evidence = evidence or {}

        # 1. Sequential prerequisite check: previous phase must be PASS
        if p_id > 1:
            prev_status = self.phases[p_id - 1]["status"]
            if prev_status != "PASS":
                return {
                    "status": "BLOCKED",
                    "phase_id": p_id,
                    "error": (
                        f"Prerequisite Phase {p_id - 1} ('{PHASE_METADATA[p_id - 1]['name']}') "
                        f"has not PASSED yet. Current status: {prev_status}. "
                        "Jumping ahead without passing prior gates is strictly prohibited by Section 14."
                    ),
                }

        # 2. Evidence validation
        missing: List[str] = []

        if p_id == 1:
            has_datums = evidence.get("datums_reconciled") is True or bool(evidence.get("evidence_matrix"))
            has_matrix = evidence.get("evidence_matrix_compiled") is True or bool(evidence.get("evidence_matrix"))
            if not has_datums and not has_matrix:
                missing.append("datums_reconciled or evidence_matrix")

        elif p_id == 2:
            strategies = evidence.get("component_strategies")
            if not isinstance(strategies, dict) or len(strategies) == 0:
                missing.append("component_strategies dict mapping components to valid strategies")
            else:
                for comp, strat in strategies.items():
                    if strat not in VALID_STRATEGIES:
                        missing.append(f"Component '{comp}' has invalid strategy '{strat}'. Must be one of {sorted(VALID_STRATEGIES)}")

        elif p_id == 3:
            if not evidence.get("specular_clay_verified"):
                missing.append("specular_clay_verified (G1/G2 reflection continuity test)")
            if not (evidence.get("topology_passed") or evidence.get("topology_audited") or evidence.get("topology_repaired") or evidence.get("quad_remeshed")):
                missing.append("topology_passed (zero non-manifold edges, watertight manifold test)")

        elif p_id == 4:
            if not (evidence.get("wheelhouse_recessed") or evidence.get("wheel_arches_carved") or evidence.get("secondary_assemblies_modeled")):
                missing.append("wheelhouse_recessed (wheel arches must be carved cavities, not flat walls)")
            if not (evidence.get("cutouts_carved") or evidence.get("boolean_applied") or evidence.get("modifier_stack_applied")):
                missing.append("cutouts_carved (precision boolean or inset cutouts)")

        elif p_id == 5:
            if not (evidence.get("hero_depth_verified") or evidence.get("depth_modeled") or evidence.get("rig_hierarchy_verified") or evidence.get("cloth_simulated")):
                missing.append("hero_depth_verified (no flat stickers; radiator slats and lights must have true 3D depth)")

        elif p_id == 6:
            if not (evidence.get("materials_assigned") or evidence.get("shaders_applied") or evidence.get("pbr_material_assigned")):
                missing.append("materials_assigned (PBR automotive shaders tagged on faces)")
            if not (evidence.get("studio_render_verified") or evidence.get("render_quadrants_captured") or (evidence.get("studio_lighting_configured") and evidence.get("camera_framed"))):
                missing.append("studio_render_verified (4-quadrant studio render QA)")

        if missing:
            self.phases[p_id]["status"] = "FAIL"
            self.phases[p_id]["evidence"] = evidence
            if self.state_file:
                self.save_state()
            return {
                "status": "FAIL",
                "phase_id": p_id,
                "name": PHASE_METADATA[p_id]["name"],
                "gate_verdict": "REJECTED",
                "missing_criteria": missing,
            }

        # Gate approved
        self.phases[p_id]["status"] = "PASS"
        self.phases[p_id]["verified_at"] = time.time()
        self.phases[p_id]["evidence"] = evidence
        if self.state_file:
            self.save_state()

        next_phase = p_id + 1 if p_id < 6 else "COMPLETE"
        return {
            "status": "PASS",
            "phase_id": p_id,
            "name": PHASE_METADATA[p_id]["name"],
            "gate_verdict": "APPROVED_TO_PROCEED",
            "next_phase": next_phase,
        }

    def get_status(self) -> Dict[str, Any]:
        """Return the complete 6-stage pipeline progress state."""
        passed_count = sum(1 for p in self.phases.values() if p["status"] == "PASS")
        current_phase = next((p_id for p_id, p in self.phases.items() if p["status"] != "PASS"), 7)
        return {
            "phases": self.phases,
            "passed_count": passed_count,
            "total_phases": 6,
            "current_active_phase": current_phase if current_phase <= 6 else "ALL_COMPLETE",
            "pipeline_verdict": "APPROVED_FOR_EXPORT" if passed_count == 6 else "IN_PROGRESS",
        }


# Singleton instance for the running session with persistence
_DEFAULT_STATE_FILE = Path(".pipeline_state.json")
_DEFAULT_GATE_MANAGER = PhaseGateManager(state_file=_DEFAULT_STATE_FILE)


def validate_phase_gate(phase_id: Union[int, str], evidence: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Validate a pipeline phase gate against the active session manager."""
    return _DEFAULT_GATE_MANAGER.validate_gate(phase_id, evidence)


def get_pipeline_status() -> Dict[str, Any]:
    """Retrieve full pipeline status across all 6 phases."""
    return _DEFAULT_GATE_MANAGER.get_status()


def reset_pipeline() -> None:
    """Reset the pipeline gates state."""
    _DEFAULT_GATE_MANAGER.reset()
