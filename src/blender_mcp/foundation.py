"""Foundation architecture, structured response schemas, and risk classification for Rahul 3D Engine.

Provides unified result formatting, input validation, and risk gating across all MCP tools.
"""

from __future__ import annotations
from enum import Enum
import time
import uuid
from typing import Any, Dict, List, Optional, Union

try:
    import bpy
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


class OperationRisk(str, Enum):
    """Operation risk classifications for Rahul 3D Engine."""
    READ_ONLY = "READ_ONLY"              # State inspect, bounding box check, topology read
    NON_DESTRUCTIVE = "NON_DESTRUCTIVE"  # Additive object creation, procedural instance
    REVERSIBLE = "REVERSIBLE"            # Non-destructive modifier add, material assign with slot record
    DESTRUCTIVE = "DESTRUCTIVE"          # Remesh, boolean collapse, checkpoint restore, object delete


def format_tool_response(
    tool_name: str,
    result: Any = None,
    success: bool = True,
    warnings: Optional[List[str]] = None,
    errors: Optional[List[str]] = None,
    validation: Optional[Dict[str, Any]] = None,
    risk: OperationRisk = OperationRisk.NON_DESTRUCTIVE,
    operation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Return consistent, production-grade structured result envelope."""
    return {
        "success": bool(success),
        "tool": str(tool_name),
        "operation_id": operation_id or f"op_{int(time.time()*1000)}_{uuid.uuid4().hex[:6]}",
        "risk": risk.value if isinstance(risk, OperationRisk) else str(risk),
        "result": result if result is not None else {},
        "warnings": list(warnings or []),
        "errors": list(errors or []),
        "validation": validation or {"passed": bool(success), "checks": []},
        "timestamp": time.time(),
    }


def validate_object_exists(object_name: str) -> tuple[bool, Optional[str]]:
    """Validate that named object exists in the current Blender scene.
    
    Returns (exists: bool, error_msg: Optional[str]).
    """
    if not object_name:
        return False, "Target object_name cannot be empty"
    if not HAS_BPY:
        return True, None  # Mocked environment passes validation
    
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        available = [o.name for o in bpy.data.objects[:10]]
        suffix = f" (Available: {', '.join(available)}...)" if available else " (Scene is empty)"
        return False, f"Object '{object_name}' not found in active scene{suffix}"
    return True, None


def validate_numeric_range(
    val: Union[int, float],
    name: str,
    min_val: Optional[Union[int, float]] = None,
    max_val: Optional[Union[int, float]] = None,
) -> tuple[bool, Optional[str]]:
    """Validate numeric value is within bounds."""
    if not isinstance(val, (int, float)):
        return False, f"Parameter '{name}' must be numeric, got {type(val).__name__}"
    if min_val is not None and val < min_val:
        return False, f"Parameter '{name}' ({val}) cannot be less than {min_val}"
    if max_val is not None and val > max_val:
        return False, f"Parameter '{name}' ({val}) cannot exceed {max_val}"
    return True, None
