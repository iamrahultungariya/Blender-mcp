# PBR Material & Procedural Shader Engine (System 01)
**Rahul 3D Engine — Phase 2 Documentation**

---

## 1. Overview
The PBR Material & Procedural Shader Engine eliminates the need for agents to write custom 40-line `bpy` boilerplate scripts to configure shaders. It features:
- **Version-Aware Principled BSDF Sockets**: Automatically maps socket names between Blender 3.x, 4.x, and 5.x LTS (`Coat Weight` / `Clearcoat`, `Specular IOR Level` / `Specular`, `Transmission Weight` / `Transmission`, `Emission Color` / `Emission`).
- **15 Procedural Presets**: High-fidelity, physically calibrated procedural node graphs with texture coordinates, mapping, color ramps, and surface bump.
- **Node Tree Inspection & Validation**: Structured inspection of shader graphs and automated defect detection.

---

## 2. FastMCP Tool Interface

### `assign_pbr_material`
Quickly assign a standard PBR Principled BSDF material with custom values.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `material_name` (str): Name of material to create or reuse.
  - `base_color` (list[float]): RGBA values [0.0 - 1.0].
  - `metallic` (float): Metallic ratio [0.0 - 1.0].
  - `roughness` (float): Microfacet roughness [0.0 - 1.0].
  - `alpha` (float): Opacity [0.0 - 1.0].
  - `emission_color` (list[float]): RGBA emission tint.
  - `emission_strength` (float): Light output in Watts/m².
  - `assign_mode` (str): `ACTIVE_OR_NEW` (default) or `REPLACE_ALL`.
- **Risk**: `REVERSIBLE`.

### `create_procedural_shader`
Generates a complete procedural shader network.
- **Parameters**:
  - `material_name` (str): Name of material.
  - `preset` (str): One of 15 presets:
    - `wood`: Natural wavy grain with micro-bump.
    - `brushed_metal`: Stretched directional noise with anisotropic scratches.
    - `polished_metal`: Pure chrome specular finish.
    - `concrete`: Layered aggregate voronoi and fine mortar bump.
    - `marble`: Distorted wave veining with subtle subsurface scatter.
    - `leather`: Organic voronoi cell boundaries with soft specular sheen.
    - `fabric_weave`: Micro crosshatch pattern with soft velvet sheen.
    - `plastic`: Clean dielectric with crisp specular highlight.
    - `ceramic`: High-gloss clearcoat glaze over porcelain base.
    - `rubber`: High roughness, low specular, vulcanized appearance.
    - `painted_wall`: Subtle plaster orange-peel micro-stipple bump.
    - `aged_wood`: Darkened weathered grain ridges and cracks.
    - `rusted_metal`: Procedural oxidation mask blending steel and rough rust.
    - `stone`: Multi-octave natural mineral noise displacement.
    - `glass`: Realistic optical transmission (IOR 1.52).
  - `object_name` (str, optional): Target object to assign material to immediately.
  - `scale` (float): Global texture mapping scale.
  - `color_tint` (list[float], optional): Custom RGBA tint override.
  - `roughness_multiplier` (float): Multiplier for default roughness.
- **Risk**: `NON_DESTRUCTIVE`.

### `inspect_material_nodes`
Returns structured node data including node types, input sockets, links, and output verification.
- **Risk**: `READ_ONLY`.

### `modify_material_property`
Safely tweaks a single socket value (e.g. `roughness`, `metallic`, `base_color`) without rebuilding the shader tree.
- **Risk**: `REVERSIBLE`.

### `validate_material_setup`
Checks for missing Material Output nodes, disconnected BSDF outputs, and broken links.
- **Risk**: `READ_ONLY`.
