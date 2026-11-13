# Modular Code Architecture Playbook for Blender MCP

## 1. Intent & Purpose

This playbook codifies the structural rules that prevent AI agents from generating fragile, unmaintainable, 1,000-line monolithic Blender scripts. All procedural geometry, architectural environments, and hero assets must adhere to this modular standard.

---

## 2. The Strict Anti-Monolithic Rule

> **Iron Law**: No single procedural generation file may exceed **250 lines of code**. Any modeling script attempting to define materials, utility math, architectural boundaries, and prop geometry inside a single file is immediately rejected.

### Why Monolithic Scripts Fail in Blender MCP:
1. **Context Window Saturation**: When an error occurs at line 842 of a 1,000-line script, diagnosing and editing it consumes massive context and frequently truncates tokens.
2. **Crash & Timeout Cascades**: If a boolean operator fails mid-script, the entire scene generation halts, leaving half-built orphan objects in memory.
3. **Zero Code Reusability**: Materials and helpers written inside monolithic scripts cannot be shared across different assets.
4. **Surgical Patching Impossibility**: Tweaking the height of a pillow requires re-running the entire 1,000-line script, re-generating walls, floors, and furniture from scratch.

---

## 3. The 4-Tier Modular Directory Blueprint

Every asset or scene generation task must be structured as a decoupled Python package:

```
<project_root>/
├── core/
│   ├── __init__.py
│   ├── materials.py       # Tier 1: Shared PBR shader nodes, material slots
│   └── mesh_utils.py      # Tier 2: BMesh primitives, matrix transforms, tagging
├── prefabs/
│   ├── __init__.py
│   ├── arch_kit.py        # Tier 3: Walls, floor slabs, ceiling, baseboards
│   ├── <asset>_kit.py     # Tier 3: Main prop geometry (e.g. bed_kit.py, desk_kit.py)
│   └── soft_goods_kit.py  # Tier 3: Pillows, cushions, duvets, drapery
└── main.py                # Tier 4: Scene assembler, Alt+D instancing, lights, camera
```

---

## 4. Tier Responsibilities & Contract

### Tier 1: `core/materials.py`
* **Responsibility**: Define pure material creation functions returning `bpy.types.Material`.
* **Rules**:
  - Always check `bpy.data.materials.get(mat_name)` before creating a new material to prevent duplicate `.001` proliferation.
  - Use modern Principled BSDF socket connections (`Base Color`, `Roughness`, `Metallic`, `Normal`).
  - Keep material definitions completely decoupled from geometry objects.

```python
import bpy

def get_or_create_fabric_material(name="Mat_VelvetFabric", color=(0.15, 0.18, 0.22, 1.0), roughness=0.85):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        if "Sheen Weight" in bsdf.inputs:
            bsdf.inputs["Sheen Weight"].default_value = 0.5
    return mat
```

### Tier 2: `core/mesh_utils.py`
* **Responsibility**: Math helpers and in-memory BMesh operations.
* **Rules**:
  - Functions must operate on `bmesh.types.BMesh` or create clean BMesh objects.
  - Zero UI operators (`bpy.ops`) allowed here.
  - Helper functions for matrix transformations, vertex grouping, and normal recalculation.

```python
import bmesh
from mathutils import Matrix

def transform_bmesh(bm, location=(0,0,0), rotation_z_rad=0.0, scale=(1,1,1)):
    mat_trans = Matrix.Translation(location)
    mat_rot = Matrix.Rotation(rotation_z_rad, 4, 'Z')
    mat_scale = Matrix.Diagonal((*scale, 1.0))
    bmesh.ops.transform(bm, matrix=mat_trans @ mat_rot @ mat_scale, verts=bm.verts)
```

### Tier 3: `prefabs/*_kit.py`
* **Responsibility**: Specialized component geometry generators.
* **Rules**:
  - Each kit owns one specific domain (e.g., `arch_kit.py` owns walls and baseboards; `soft_goods_kit.py` owns pillows and cushions).
  - Kit functions should return either a created `bpy.types.Object` or an evaluated `bpy.types.Mesh` that can be instanced.
  - Assign materials via material slots rather than creating new materials inside the kit.

### Tier 4: `main.py`
* **Responsibility**: High-level scene coordination and assembly.
* **Rules**:
  - Sets scene units and frame configuration.
  - Instantiates prefabs and places them at world coordinates.
  - Enforces **Linked Mesh Instancing (`Alt+D`)**:
    ```python
    # Master mesh generated once:
    master_pillow_mesh = soft_goods_kit.create_pillow_mesh("MasterPillowMesh")
    
    # Instanced with individual transforms:
    for loc, rot in [((0.5, 1.2, 0.6), 0.1), ((-0.5, 1.2, 0.6), -0.1)]:
        obj = bpy.data.objects.new("Pillow_Instance", master_pillow_mesh)
        obj.location = loc
        obj.rotation_euler.z = rot
        bpy.context.collection.objects.link(obj)
    ```
  - Configures 3-point studio lighting, gobos, and camera.
  - Governed by `DEV_FAST_MODE`: Guard final rendering behind a debug flag.

---

## 5. Single-Buffer BMesh Merging

When scattering repeated items (e.g., floor tiles, wall cladding slats, books on shelves), **never create 100 individual `bpy.data.objects`**.

```python
# PRO WAY: Single-Buffer BMesh Merging
master_bm = bmesh.new()

for i in range(20):
    slat_bm = bmesh.new()
    bmesh.ops.create_cube(slat_bm, size=1.0)
    transform_bmesh(slat_bm, location=(i * 0.1, 0, 0), scale=(0.04, 0.02, 2.4))
    
    # Merge into master buffer in memory (0.001s in C RAM)
    slat_bm.to_mesh(temp_mesh := bpy.data.meshes.new("tmp"))
    master_bm.from_mesh(temp_mesh)
    bpy.data.meshes.remove(temp_mesh)
    slat_bm.free()

# Write ONE object to scene
final_mesh = bpy.data.meshes.new("SlattedWallCladding")
master_bm.to_mesh(final_mesh)
master_bm.free()
final_obj = bpy.data.objects.new("SlattedWallCladding", final_mesh)
bpy.context.collection.objects.link(final_obj)
```
