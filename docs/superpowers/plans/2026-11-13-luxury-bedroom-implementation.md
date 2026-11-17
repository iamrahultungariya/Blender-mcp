# Modern Minimalist 5-Star Luxury Bedroom Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a high-fidelity, hyper-realistic 5-Star Luxury Bedroom procedural generation system in Blender via a modular 3D architecture adhering to the 4-phase spatial pipeline (`generate_spatial_blueprint` -> `get_component_tree` -> `bmesh construction` -> `validate_phase_gate(phase_id=2)`).

**Architecture:** Deconstruct the scene into reusable, decoupled Python modules under `luxury_bedroom/` (materials, bmesh math utilities, bed assembly, cloth/pillows bedding, nightstands/lighting, and room envelope). All geometry is synthesized strictly in memory via `bmesh` within C-RAM (zero UI freeze), tagged with multi-material slots, and verified through Gate G2.

**Tech Stack:** Python 3.11, Blender 4.x `bpy`, `bmesh`, `mathutils`, `numpy`, Pytest.

**Spec:** [2026-11-13-luxury-bedroom-design.md](file:///c:/Users/Rahul/OneDrive/Desktop/Blender%20MCP/docs/superpowers/specs/2026-11-13-luxury-bedroom-design.md)

---

## Global Constraints

- **90/10 Hybrid Pipeline Standard**: All procedural mesh synthesis must execute in Zone A (`bmesh` in C-RAM with `bmesh.ops.*` and `bm.to_mesh()`). `bpy.ops` is restricted to I/O and camera setup.
- **Zero Monolithic Scripts**: Geometry, materials, and modules must reside in separate files under `luxury_bedroom/`.
- **Anti-Boxy Mandates**: Zero unfilleted/unbeveled 90° edges; all cushions and pillows must use parametric parabolic lofting $Z(u,v) = z_0 + crown \cdot (1 - u^2)(1 - v^2)$.
- **Phase Gate Compliance**: Must successfully pass `validate_phase_gate(phase_id=2)` with valid strategies (`subdivision_cage`, `boolean_bevel`, `bezier_curve`).

---

## Review Focus

1. **Gate G2 Validation Failure**: If component strategies contain unregistered strings, `validate_phase_gate` rejects the phase; verify exact strategy names against `VALID_STRATEGIES`.
2. **BMesh Memory Leaks or UI Freezes**: Calling `bpy.ops.mesh.primitive_*` inside construction loops freezes Blender; ensure every module accepts/returns `bmesh.types.BMesh` or populates a shared object buffer.
3. **Pillow & Chadar Intersection / Z-Fighting**: Pillows or blanket clipping through mattress; ensure vertical $Z$-offsets respect physical layering ($Z_{frame} < Z_{mattress} < Z_{chadar} < Z_{pillow}$).
4. **Cloth Drape Topology Inversion**: Sinusoidal cloth fold math generating non-manifold self-intersecting normals; assert all generated BMesh meshes pass manifold checks (`is_valid` and no degenerate faces).
5. **Headboard Slat Spacing Alignment**: Vertical acoustic slats must be evenly distributed along the feature wall width without overlapping bed boundaries.

---

### Task 1: Spatial Pipeline Gate Integration & PBR Material Library

**Files:**
- Create: `luxury_bedroom/__init__.py`
- Create: `luxury_bedroom/core/__init__.py`
- Create: `luxury_bedroom/core/materials.py`
- Create: `tests/test_luxury_materials_and_gates.py`

**Interfaces:**
- Consumes: `src.blender_mcp.spatial_thinking.SpatialThinkingEngine`, `src.blender_mcp.pipeline_gates.validate_phase_gate`
- Produces: `MaterialLibrary` class providing shader generation for `WALNUT_WOOD`, `UPHOLSTERY_VELVET`, `LINEN_WHITE`, `LINEN_ACCENT`, `BRUSHED_BRASS`, `PARQUET_OAK`, `WARM_PLASTER`, `LED_WARM_COVE`.

- [ ] **Step 1: Write failing test for MaterialLibrary and Gate 2 validation**

```python
# tests/test_luxury_materials_and_gates.py
import pytest
from luxury_bedroom.core.materials import MaterialLibrary
from blender_mcp.pipeline_gates import validate_phase_gate
from blender_mcp.spatial_thinking import SpatialThinkingEngine

def test_spatial_blueprint_resolution():
    engine = SpatialThinkingEngine()
    bp = engine.generate_spatial_blueprint("luxury bedroom with king bed and pillows")
    assert bp["domain"] == "INTERIOR_SPACES"
    assert bp["archetype"] == "BEDROOM"
    assert bp["dimensions"]["length"] >= 4.0

def test_phase_gate_g2_bedroom_strategies():
    strategies = {
        "bed_frame": "boolean_bevel",
        "fluted_headboard": "subdivision_cage",
        "mattress_cushion": "subdivision_cage",
        "pillows_layered": "subdivision_cage",
        "chadar_duvet": "subdivision_cage",
        "nightstands": "boolean_bevel",
        "pendant_lighting": "bezier_curve",
        "room_envelope": "boolean_bevel",
    }
    result = validate_phase_gate(phase_id=2, evidence={"component_strategies": strategies})
    assert result["status"] == "PASS"

def test_material_library_definitions():
    mat_lib = MaterialLibrary()
    keys = mat_lib.get_material_names()
    expected = ["WALNUT_WOOD", "UPHOLSTERY_VELVET", "LINEN_WHITE", "LINEN_ACCENT", "BRUSHED_BRASS", "PARQUET_OAK", "WARM_PLASTER", "LED_WARM_COVE"]
    for k in expected:
        assert k in keys
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_luxury_materials_and_gates.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'luxury_bedroom'`)

- [ ] **Step 3: Implement `luxury_bedroom/core/materials.py`**

Implement `MaterialLibrary` with safe fallback when `bpy` is headless or running in tests, mapping material slots and node trees for roughness, metallic, normal, and base color attributes.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_luxury_materials_and_gates.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/ tests/test_luxury_materials_and_gates.py
git commit -m "feat(luxury_bedroom): add package structure, material library, and Gate 2 integration"
```

---

### Task 2: Procedural BMesh Geometric Operators & Organic Cloth/Cushion Lofting

**Files:**
- Create: `luxury_bedroom/core/bmesh_utils.py`
- Create: `tests/test_bmesh_utils.py`

**Interfaces:**
- Consumes: `mathutils.Vector`, `mathutils.Matrix`, `bmesh`
- Produces: 
  - `create_beveled_box(bm, width, length, height, bevel_radius, segments, offset, mat_index)`
  - `create_cushion_loft(bm, width, length, height, crown, subdivisions_u, subdivisions_v, offset, mat_index)`
  - `create_draped_cloth_surface(bm, width, length, drape_drop, folds_freq, folds_amp, subdivisions_x, subdivisions_y, offset, mat_index)`
  - `create_fluted_panel(bm, width, height, depth, num_flutes, flute_radius, offset, mat_index)`

- [ ] **Step 1: Write failing test for bmesh procedural operators**

```python
# tests/test_bmesh_utils.py
import pytest
import bmesh
from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_cushion_loft,
    create_draped_cloth_surface,
    create_fluted_panel,
)

def test_create_beveled_box():
    bm = bmesh.new()
    create_beveled_box(bm, 1.0, 1.0, 0.5, bevel_radius=0.05, segments=3)
    assert len(bm.verts) > 8
    assert len(bm.faces) > 6
    bm.free()

def test_create_cushion_loft():
    bm = bmesh.new()
    create_cushion_loft(bm, 0.8, 0.5, 0.15, crown=0.06, subdivisions_u=8, subdivisions_v=8)
    assert len(bm.verts) >= 64
    # Highest vert must be crowned above base height
    max_z = max(v.co.z for v in bm.verts)
    assert max_z > 0.15
    bm.free()

def test_create_draped_cloth_surface():
    bm = bmesh.new()
    create_draped_cloth_surface(bm, 2.0, 1.8, drape_drop=0.2, folds_freq=4.0, folds_amp=0.02, subdivisions_x=12, subdivisions_y=12)
    assert len(bm.faces) > 50
    bm.free()

def test_create_fluted_panel():
    bm = bmesh.new()
    create_fluted_panel(bm, 2.4, 1.3, 0.1, num_flutes=8)
    assert len(bm.faces) > 16
    bm.free()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_bmesh_utils.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'luxury_bedroom.core.bmesh_utils'`)

- [ ] **Step 3: Implement procedural geometry functions in `luxury_bedroom/core/bmesh_utils.py`**

Implement pure BMesh math-based operators with parabolic cushion lofting $Z(u,v)$, sine-wave cloth wrinkle ripples, and beveled box primitives with proper face material index assignment.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_bmesh_utils.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/core/bmesh_utils.py tests/test_bmesh_utils.py
git commit -m "feat(luxury_bedroom): implement procedural BMesh geometry kernel and cloth/cushion lofting"
```

---

### Task 3: Modular Hero Bed Frame, Headboard & Mattress Assembly

**Files:**
- Create: `luxury_bedroom/modules/__init__.py`
- Create: `luxury_bedroom/modules/bed_assembly.py`
- Create: `tests/test_bed_assembly.py`

**Interfaces:**
- Consumes: `luxury_bedroom.core.bmesh_utils`, `luxury_bedroom.core.materials.MaterialLibrary`
- Produces: `BedAssemblyBuilder` with method `build(bm: bmesh.types.BMesh, mat_lib: MaterialLibrary) -> dict` returning bounds and datum points (mattress surface Z, headboard center, frame origin).

- [ ] **Step 1: Write failing test for BedAssemblyBuilder**

```python
# tests/test_bed_assembly.py
import pytest
import bmesh
from luxury_bedroom.modules.bed_assembly import BedAssemblyBuilder
from luxury_bedroom.core.materials import MaterialLibrary

def test_bed_assembly_construction():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    builder = BedAssemblyBuilder(width=2.0, length=2.1, headboard_height=1.3)
    info = builder.build(bm, mat_lib)
    
    assert "mattress_top_z" in info
    assert "headboard_center" in info
    assert info["mattress_top_z"] > 0.45
    assert len(bm.verts) > 200
    assert len(bm.faces) > 100
    bm.free()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_bed_assembly.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'luxury_bedroom.modules.bed_assembly'`)

- [ ] **Step 3: Implement `BedAssemblyBuilder` in `luxury_bedroom/modules/bed_assembly.py`**

Construct:
1. Floating recessed plinth (shadow-gap base).
2. Chamfered hardwood outer frame in `WALNUT_WOOD`.
3. 12-channel fluted vertical headboard in `UPHOLSTERY_VELVET` with chamfered perimeter frame.
4. Contoured ergonomic mattress in `LINEN_WHITE` with beveled edges.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_bed_assembly.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/modules/bed_assembly.py tests/test_bed_assembly.py
git commit -m "feat(luxury_bedroom): implement modular bed platform, fluted headboard, and mattress assembly"
```

---

### Task 4: High-Realism Bedding System: Layered Pillows & Draped Chadar (Duvet)

**Files:**
- Create: `luxury_bedroom/modules/bedding_cloth.py`
- Create: `tests/test_bedding_cloth.py`

**Interfaces:**
- Consumes: `luxury_bedroom.core.bmesh_utils`, `luxury_bedroom.core.materials.MaterialLibrary`
- Produces: `BeddingClothBuilder` with method `build(bm: bmesh.types.BMesh, mattress_datum: dict, mat_lib: MaterialLibrary) -> dict`

- [ ] **Step 1: Write failing test for BeddingClothBuilder**

```python
# tests/test_bedding_cloth.py
import pytest
import bmesh
from luxury_bedroom.modules.bed_assembly import BedAssemblyBuilder
from luxury_bedroom.modules.bedding_cloth import BeddingClothBuilder
from luxury_bedroom.core.materials import MaterialLibrary

def test_bedding_cloth_generation():
    bm = bmesh.new()
    mat_lib = MaterialLibrary()
    bed_builder = BedAssemblyBuilder(width=2.0, length=2.1)
    bed_info = bed_builder.build(bm, mat_lib)
    
    bedding_builder = BeddingClothBuilder()
    cloth_info = bedding_builder.build(bm, bed_info, mat_lib)
    
    assert cloth_info["pillows_count"] >= 4
    assert cloth_info["chadar_draped"] is True
    assert len(bm.faces) > 500
    bm.free()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_bedding_cloth.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'luxury_bedroom.modules.bedding_cloth'`)

- [ ] **Step 3: Implement `BeddingClothBuilder` in `luxury_bedroom/modules/bedding_cloth.py`**

Construct:
1. **Layer 1 (Sleeping Pillows)**: 2 large sleeping pillows tilted 15° against the headboard with crowned loft and perimeter welt seams.
2. **Layer 2 (Decorative Accent Pillows)**: 2 medium front pillows angled slightly inward with contrasting linen material.
3. **Layer 3 (Lumbar Cushion)**: 1 centered small lumbar pillow with button or seam detail.
4. **Chadar / Duvet**: Draped blanket covering lower 75% of the bed with sinusoidal cloth ripple deformation, realistic drape overhang down the left, right, and foot sides of the bed, and a turned-down top cuff exposing the underside sheet.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_bedding_cloth.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/modules/bedding_cloth.py tests/test_bedding_cloth.py
git commit -m "feat(luxury_bedroom): implement layered organic pillows and draped chadar/duvet bedding system"
```

---

### Task 5: Architectural Envelope, Nightstands, Designer Lighting & Assembly Pipeline

**Files:**
- Create: `luxury_bedroom/modules/nightstand_lighting.py`
- Create: `luxury_bedroom/modules/room_envelope.py`
- Create: `luxury_bedroom/assembler.py`
- Create: `tests/test_full_suite_assembly.py`

**Interfaces:**
- Consumes: All `luxury_bedroom` modules, `SpatialThinkingEngine`, `validate_phase_gate`
- Produces: `assemble_luxury_bedroom(dev_fast_mode: bool = True) -> dict` executing complete 4-phase procedural pipeline.

- [ ] **Step 1: Write failing test for full bedroom assembly pipeline**

```python
# tests/test_full_suite_assembly.py
import pytest
from luxury_bedroom.assembler import assemble_luxury_bedroom

def test_full_assembly_pipeline():
    result = assemble_luxury_bedroom(dev_fast_mode=True)
    assert result["status"] == "SUCCESS"
    assert result["phase_gate_status"] == "PASS"
    assert result["total_components"] >= 6
    assert result["mesh_face_count"] > 1000
    assert result["blueprint"]["archetype"] == "BEDROOM"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_full_suite_assembly.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'luxury_bedroom.assembler'`)

- [ ] **Step 3: Implement `nightstand_lighting.py`, `room_envelope.py`, and `assembler.py`**

1. `nightstand_lighting.py`: Dual floating cantilever nightstands with beveled drawers & suspended brushed brass cylindrical pendant lights with emissive warm diffusers.
2. `room_envelope.py`: Finished walls, acoustic wood slat feature wall behind bed, herringbone/parquet floor, recessed cove LED ceiling tray, and plush beveled floor rug.
3. `assembler.py`: Orchestrates Step 1 (`generate_spatial_blueprint`), Step 2 (`get_component_tree`), Step 3 (`bmesh procedural construction` in C-RAM using shared buffer), and Step 4 (`validate_phase_gate(phase_id=2)`).

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_full_suite_assembly.py -v`  
Expected: PASS

- [ ] **Step 5: Run end-to-end assembly script and verify scene in Blender**

Execute: `.venv\Scripts\python.exe -c "from luxury_bedroom.assembler import assemble_luxury_bedroom; r = assemble_luxury_bedroom(); print('Result:', r)"`  
Expected: PASS with status SUCCESS and Gate 2 PASS.

- [ ] **Step 6: Commit**

```bash
git add luxury_bedroom/ tests/test_full_suite_assembly.py
git commit -m "feat(luxury_bedroom): implement room envelope, nightstands, pendant lighting, and 4-phase assembler pipeline"
```
