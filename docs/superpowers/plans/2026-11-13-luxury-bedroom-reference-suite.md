# Contemporary Warm Luxury Master Bedroom Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a AAA photorealistic, non-boxy 5-Star Luxury Master Bedroom Suite in Blender matching the reference concept turnaround sheet (`media_1794550685111_b4341c92.jpg`) with a target geometric budget of ~300,000 triangles (~150k quads), broken into modular prefabs without monolithic files, and verified via the 4-phase procedural pipeline.

**Architecture:** Deconstruct the scene into decoupled, reusable Python modules under `luxury_bedroom/` (core PBR materials and high-density math kernels, plus individual prefabs for hero bed, nightstands, ottoman bench, lounge corner, media wall, wardrobe, window curtains, chandelier, and room envelope). All geometry is constructed in memory via `bmesh` within C-RAM (zero UI freeze), tagged with multi-material slots, and verified through Gate G2.

**Tech Stack:** Python 3.11, Blender 5.2 / 4.x `bpy`, `bmesh`, `mathutils`, `numpy`, Pytest.

**Spec:** [docs/superpowers/specs/2026-11-13-luxury-bedroom-reference-suite-design.md](file:///c:/Users/Rahul/OneDrive/Desktop/Blender%20MCP/docs/superpowers/specs/2026-11-13-luxury-bedroom-reference-suite-design.md)

---

## Global Constraints

- **90/10 Hybrid Pipeline Standard**: All procedural mesh synthesis must execute in Zone A (`bmesh` in C-RAM with `bmesh.ops.*` and `bm.to_mesh()`). Zero UI freezes, sub-second execution.
- **Zero Monolithic Scripts**: Every distinct asset component (bed, nightstands, bench, lounge corner, media wall, wardrobe, curtains, chandelier, envelope) must live in its own modular prefab file under `luxury_bedroom/prefabs/`.
- **Anti-Boxy Geometry Law**: Zero unfilleted/unbeveled 90° edges; all cushions and pillows must use parametric parabolic lofting $Z(u,v) = z_0 + crown \cdot (1 - u^2)(1 - v^2)$, curtains must feature sinusoidal pleats, and headboard must feature segmented cushions and wing panels.
- **300k Triangle Budget Utilization**: Allocate high subdivision resolution across fabrics, fluting, lathe profiles, and drapery to reach ~200k - 300k triangles matching the reference sheet.
- **No Export Step**: Focus strictly on Blender viewport 3D geometry, shaders, lighting, and internal camera rendering.

---

## Review Focus

1. **Gate G2 Validation Compliance**: Ensure all 10 component systems map to valid strategies (`subdivision_cage`, `boolean_bevel`, `bezier_curve`).
2. **Layering & Vertical Stacking**: Ensure no geometric clipping/Z-fighting across floor -> rug -> bed frame -> mattress -> sheet -> pillows -> duvet -> runner.
3. **Winged Headboard Alignment**: Ensure the 3 horizontal cushioned pads and 2 angled wingback side panels align seamlessly with the floating bed base width.
4. **Pleated Drapery Topology**: Sinusoidal cloth fold math for curtains and duvet must produce clean manifold geometry with authentic specular highlights.
5. **Multi-Material Tagging Integrity**: Ensure every face across the 300k triangle mesh receives its designated material slot index from `MaterialLibrary`.

---

### Task 1: Reference PBR Shader Palette & High-Density Math Kernels

**Files:**
- Modify: `luxury_bedroom/core/materials.py`
- Modify: `luxury_bedroom/core/bmesh_utils.py`
- Create: `tests/test_ref_materials.py`

**Interfaces:**
- Consumes: Reference image color palette & textures.
- Produces: `MaterialLibrary` with 10 reference shaders (`TRAVERTINE_TILES`, `WALNUT_WOOD`, `TAUPE_BOUCLE`, `LINEN_WHITE`, `CHARCOAL_PLEAT`, `BRUSHED_BRASS`, `MATTE_BLACK_METAL`, `TINTED_BRONZE_GLASS`, `SHEER_WHITE`, `LED_WARM_2700K`) and enhanced BMesh math operators for high-density curves and pleats.

- [ ] **Step 1: Write failing test for reference materials and high-density math**

```python
# tests/test_ref_materials.py
import pytest
from luxury_bedroom.core.materials import MaterialLibrary

def test_reference_materials_palette():
    mat_lib = MaterialLibrary()
    required = [
        "TRAVERTINE_TILES", "WALNUT_WOOD", "TAUPE_BOUCLE", "LINEN_WHITE",
        "CHARCOAL_PLEAT", "BRUSHED_BRASS", "MATTE_BLACK_METAL",
        "TINTED_BRONZE_GLASS", "SHEER_WHITE", "LED_WARM_2700K"
    ]
    names = mat_lib.get_material_names()
    for req in required:
        assert req in names
        assert isinstance(mat_lib.get_index(req), int)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_materials.py -v`  
Expected: FAIL (KeyError or missing materials)

- [ ] **Step 3: Update `luxury_bedroom/core/materials.py` and `luxury_bedroom/core/bmesh_utils.py`**

Add all 10 reference shaders with Principled BSDF node attributes (metallic, roughness, transmission, sheen, emission). Add helper for pleated sinusoidal drape sheets and lathe profile turning.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_materials.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/core/ tests/test_ref_materials.py
git commit -m "feat(ref_suite): implement 10 reference PBR shaders and high-density math operators"
```

---

### Task 2: Modular Hero Bed Assembly (Winged Headboard, Mattress, 6 Pillows, Duvet & Runner)

**Files:**
- Create: `luxury_bedroom/prefabs/bed_hero.py`
- Create: `tests/test_ref_bed_hero.py`

**Interfaces:**
- Consumes: `luxury_bedroom.core.bmesh_utils`, `luxury_bedroom.core.materials.MaterialLibrary`
- Produces: `HeroBedBuilder` generating ~85k triangles of hero bed geometry (winged segmented headboard, floating base, mattress, 6 layered pillows, draped duvet with folded cuff, and pleated charcoal bed runner).

- [ ] **Step 1: Write failing test for HeroBedBuilder**

```python
# tests/test_ref_bed_hero.py
import pytest
from luxury_bedroom.prefabs.bed_hero import HeroBedBuilder
from luxury_bedroom.core.materials import MaterialLibrary
from luxury_bedroom.core.bmesh_utils import MockBMesh

def test_hero_bed_construction():
    bm = MockBMesh.new()
    mat_lib = MaterialLibrary()
    builder = HeroBedBuilder()
    info = builder.build(bm, mat_lib)
    
    assert info["pillows_count"] == 6
    assert info["has_bed_runner"] is True
    assert info["has_winged_headboard"] is True
    assert len(bm.faces) > 500
    bm.free()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_bed_hero.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'luxury_bedroom.prefabs.bed_hero'`)

- [ ] **Step 3: Implement `luxury_bedroom/prefabs/bed_hero.py`**

Construct:
1. Floating bed base with recessed shadow gap plinth.
2. Winged headboard: 3 horizontal cushioned pads in `TAUPE_BOUCLE` flanked by angled side wingback panels.
3. Contoured ergonomic mattress with perimeter beveled welts in `LINEN_WHITE`.
4. 6 Pillows: 2 large sleeping pillows (tilted 15°), 2 square decorative pillows (`CHARCOAL_PLEAT`), 2 front rectangular lumbar pillows (`TAUPE_BOUCLE`).
5. Draped white duvet with turned-over cuff exposing inner sheet.
6. Charcoal pleated folded bed runner draped across lower third of bed with authentic gravity overhang.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_bed_hero.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/prefabs/bed_hero.py tests/test_ref_bed_hero.py
git commit -m "feat(ref_suite): implement hero winged bed, 6 layered pillows, draped duvet, and folded bed runner"
```

---

### Task 3: Secondary Furnishings: Floating Nightstands, Ottoman Bench & Lounge Corner

**Files:**
- Create: `luxury_bedroom/prefabs/nightstands.py`
- Create: `luxury_bedroom/prefabs/bench_ottoman.py`
- Create: `luxury_bedroom/prefabs/lounge_corner.py`
- Create: `tests/test_ref_secondary_furniture.py`

**Interfaces:**
- Consumes: `luxury_bedroom.core.bmesh_utils`, `luxury_bedroom.core.materials.MaterialLibrary`, `bed_datum`
- Produces: `NightstandsBuilder`, `OttomanBenchBuilder`, `LoungeCornerBuilder` generating ~75k triangles.

- [ ] **Step 1: Write failing test for secondary furnishings**

```python
# tests/test_ref_secondary_furniture.py
import pytest
from luxury_bedroom.prefabs.nightstands import NightstandsBuilder
from luxury_bedroom.prefabs.bench_ottoman import OttomanBenchBuilder
from luxury_bedroom.prefabs.lounge_corner import LoungeCornerBuilder
from luxury_bedroom.core.materials import MaterialLibrary
from luxury_bedroom.core.bmesh_utils import MockBMesh

def test_secondary_furnishings():
    bm = MockBMesh.new()
    mat_lib = MaterialLibrary()
    bed_datum = {"bed_width": 2.04, "headboard_center": (0.0, 1.2, 0.7), "bed_length": 2.14, "mattress_top_z": 0.65}
    
    ns_info = NightstandsBuilder().build(bm, bed_datum, mat_lib)
    bench_info = OttomanBenchBuilder().build(bm, bed_datum, mat_lib)
    lounge_info = LoungeCornerBuilder().build(bm, mat_lib)
    
    assert ns_info["dome_lamps_count"] == 2
    assert bench_info["cushions_count"] == 2
    assert lounge_info["armchair_placed"] is True
    assert lounge_info["floor_lamp_placed"] is True
    assert len(bm.faces) > 400
    bm.free()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_secondary_furniture.py -v`  
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 3: Implement `nightstands.py`, `bench_ottoman.py`, and `lounge_corner.py`**

Construct:
1. `nightstands.py`: Dual floating cantilevered 2-drawer walnut consoles with brass channel reveals, dual black mushroom dome lamps with glowing light, and tabletop ceramic potted plant.
2. `bench_ottoman.py`: Long upholstered bench at foot of bed with rounded double cushion and dark recessed plinth.
3. `lounge_corner.py`: Ergonomic curved tub/barrel armchair with wooden angled legs, round pedestal martini side table, and slim vertical floor lamp with cylindrical shade.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_secondary_furniture.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/prefabs/ tests/test_ref_secondary_furniture.py
git commit -m "feat(ref_suite): implement floating nightstands, ottoman bench, and lounge armchair corner"
```

---

### Task 4: Casework, Entertainment Wall & Window Drapery System

**Files:**
- Create: `luxury_bedroom/prefabs/media_wall.py`
- Create: `luxury_bedroom/prefabs/wardrobe.py`
- Create: `luxury_bedroom/prefabs/window_curtains.py`
- Create: `tests/test_ref_casework_drapes.py`

**Interfaces:**
- Consumes: `luxury_bedroom.core.bmesh_utils`, `luxury_bedroom.core.materials.MaterialLibrary`
- Produces: `MediaWallBuilder`, `WardrobeBuilder`, `WindowCurtainsBuilder` generating ~70k triangles.

- [ ] **Step 1: Write failing test for casework and drapery**

```python
# tests/test_ref_casework_drapes.py
import pytest
from luxury_bedroom.prefabs.media_wall import MediaWallBuilder
from luxury_bedroom.prefabs.wardrobe import WardrobeBuilder
from luxury_bedroom.prefabs.window_curtains import WindowCurtainsBuilder
from luxury_bedroom.core.materials import MaterialLibrary
from luxury_bedroom.core.bmesh_utils import MockBMesh

def test_casework_and_drapes():
    bm = MockBMesh.new()
    mat_lib = MaterialLibrary()
    
    media_info = MediaWallBuilder().build(bm, mat_lib)
    wardrobe_info = WardrobeBuilder().build(bm, mat_lib)
    curtain_info = WindowCurtainsBuilder().build(bm, mat_lib)
    
    assert media_info["tv_mounted"] is True
    assert wardrobe_info["doors_count"] == 4
    assert curtain_info["double_track_active"] is True
    assert len(bm.faces) > 400
    bm.free()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_casework_drapes.py -v`  
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 3: Implement `media_wall.py`, `wardrobe.py`, and `window_curtains.py`**

Construct:
1. `media_wall.py`: Long floating credenza with beveled drawers, wall-mounted 65" flat screen TV with beveled frame, and cascading potted shelf decor.
2. `wardrobe.py`: Full-height 4-door wardrobe with tinted bronze glass panels, vertical recessed handles, and interior lit shelving.
3. `window_curtains.py`: Window frame with double curtain track: sinusoidal pleated sheer inner curtains + heavy draped blackout side drapes.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_casework_drapes.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add luxury_bedroom/prefabs/ tests/test_ref_casework_drapes.py
git commit -m "feat(ref_suite): implement floating media credenza, TV, tinted glass wardrobe, and window drapery"
```

---

### Task 5: Architectural Envelope, Halo Chandelier, Master Assembler & 300k Budget Scene Generation

**Files:**
- Create: `luxury_bedroom/prefabs/room_envelope.py`
- Create: `luxury_bedroom/prefabs/chandelier.py`
- Modify: `luxury_bedroom/assembler.py`
- Create: `tests/test_ref_full_suite.py`

**Interfaces:**
- Consumes: All `luxury_bedroom/prefabs/*` modules, `SpatialThinkingEngine`, `validate_phase_gate`
- Produces: `assemble_luxury_bedroom_reference(dev_fast_mode: bool = False) -> dict` executing complete 300k triangle budget scene assembly in live Blender.

- [ ] **Step 1: Write failing test for full reference suite assembly**

```python
# tests/test_ref_full_suite.py
import pytest
from luxury_bedroom.assembler import assemble_luxury_bedroom_reference

def test_full_reference_suite_assembly():
    result = assemble_luxury_bedroom_reference(dev_fast_mode=True)
    assert result["status"] == "SUCCESS"
    assert result["phase_gate_status"] == "PASS"
    assert result["total_triangles"] >= 150000  # High-density 300k triangle budget target
    assert result["total_prefabs"] >= 9
    assert result["blueprint"]["archetype"] == "BEDROOM"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_full_suite.py -v`  
Expected: FAIL (`ImportError: cannot import name 'assemble_luxury_bedroom_reference'`)

- [ ] **Step 3: Implement `room_envelope.py`, `chandelier.py`, and update `assembler.py`**

Construct:
1. `room_envelope.py`: Travertine floor tiles with physical grout lines, plush area rug under bed, headboard feature wall (56 vertical walnut fluted slats on left and right, central warm-grey recessed wall panel, horizontal framed mountain landscape artwork, vertical warm LED light channels), and dropped ceiling tray with indirect LED cove trough.
2. `chandelier.py`: Suspended circular halo ring LED chandelier with inner warm emissive strip and 3 suspension wires.
3. `assembler.py`: Orchestrates Step 1 (`generate_spatial_blueprint`), Step 2 (`get_component_tree`), Step 3 (all 9 prefabs into single-buffer BMesh in C-RAM), and Step 4 (`validate_phase_gate(phase_id=2)`), generating live object `Luxury_Master_Bedroom_Reference_Suite`.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_ref_full_suite.py -v`  
Expected: PASS

- [ ] **Step 5: Run end-to-end assembly script and verify in live Blender scene**

Execute script in Blender to generate `Luxury_Master_Bedroom_Reference_Suite` with ~200k-300k tris, save `.blend` file and capture camera beauty render `luxury_bedroom_reference_preview.png`.

- [ ] **Step 6: Commit**

```bash
git add luxury_bedroom/ tests/test_ref_full_suite.py
git commit -m "feat(ref_suite): implement architectural envelope, halo chandelier, and complete 300k budget master assembler"
```
