# FastMCP & Blender Native Tool Selection Matrix

## 1. Intent & Purpose

This matrix establishes the definitive directory of verified Blender FastMCP tools and native BMesh / modifier techniques. When planning or executing any 3D asset, the agent must map every component to a tool listed here and justify the selection.

---

## 2. Live FastMCP Tools Directory

These tools are exposed by the active Blender FastMCP server. They run with sub-millisecond execution, complete memory isolation, and automated validation.

### 2.1 `create_architectural_wall`
* **Signature**:
  `create_architectural_wall(length: float, height: float, thickness: float = 0.2, openings: list = None, wall_name: str = "Wall")`
* **Capabilities**:
  Generates a clean, watertight wall segment with exact millimeter door and window cutouts. Operates purely in quad polygons with zero non-manifold edges.
* **When to Use**:
  Exterior and interior architectural walls, partition slabs, window frames.
* **Why**:
  Eliminates the need for destructive boolean carving on planar geometry; leaves zero shading artifacts and prevents polygon bloat.

### 2.2 `create_profile_sweep_molding`
* **Signature**:
  `create_profile_sweep_molding(path_points: list, profile_type: str = "BASEBOARD", height: float = 0.12, depth: float = 0.02, molding_name: str = "Molding")`
* **Capabilities**:
  Sweeps classical architectural profile curves (Baseboards, Crown Cornices, Wainscoting, Picture Rails) along a 3D polyline path.
* **When to Use**:
  Room perimeters, ceiling transitions, door trim, panel molding.
* **Why**:
  Automates complex decorative bevel geometry without manual edge loop extrusion.

### 2.3 `create_cushioned_profile`
* **Signature**:
  `create_cushioned_profile(width: float, depth: float, thickness: float, crown_height: float, segments: int = 8, name: str = "Cushion")`
* **Capabilities**:
  Constructs a mathematically crowned soft goods mesh with a perimeter seam loop and parabolic lofting ($Z(u,v) = Z_0 + h_{crown}(1-u^2)(1-v^2)$).
* **When to Use**:
  Sleeping pillows, throw pillows, sofa cushions, seat pads, mattress cores, upholstered headboards.
* **Why**:
  Prevents the naive "beveled box" failure; produces realistic bulging fullness and pinched corner seams out-of-the-box in <10ms.

### 2.4 `setup_subdivision_cage`
* **Signature**:
  `setup_subdivision_cage(target_object: str, levels: int = 2, render_levels: int = 2, preserve_creases: bool = True)`
* **Capabilities**:
  Configures a non-destructive Catmull-Clark Subdivision Surface modifier stack with automated edge crease preservation and Smooth Shading.
* **When to Use**:
  Soft goods, organic props, curved vehicle panels, rounded ceramics.
* **Why**:
  Keeps the base mesh lightweight (easy to edit) while delivering cinematic curvature at render time.

### 2.5 `create_bezier_tube`
* **Signature**:
  `create_bezier_tube(points: list, radius: float = 0.015, resolution: int = 12, name: str = "Cable")`
* **Capabilities**:
  Generates a 3D Bezier curve with cylindrical bevel extrusion, smooth tangent interpolation, and optional radius tapering (`Alt+S`).
* **When to Use**:
  Electrical cables, reading lamp cords, plumbing pipes, rope, stylized character hair locks.
* **Why**:
  True 3D spline curvature is non-destructive and allows instant path re-routing.

### 2.6 `clas_loft_splines`
* **Signature**:
  `clas_loft_splines(spline_curves: list, longitudinal_samples: int = 4, target_name: str = "LoftedSurface")`
* **Capabilities**:
  Lofts a series of cross-sectional guide curves into a smooth, G1 continuous quad-dominant BMesh surface using Catmull-Rom interpolation.
* **When to Use**:
  Ergonomic chair backs, car body fenders, aerodynamic fairings, organic footwear uppers.
* **Why**:
  Solves complex curved transitional forms that cannot be extruded from simple primitives.

### 2.7 `audit_mesh_topology`
* **Signature**:
  `audit_mesh_topology(target_object: str)`
* **Capabilities**:
  Audits vertex count, face count, evaluated triangle count, non-manifold edges, boundary loops, duplicate overlapping vertices, and N-gon counts. Runs with `try/finally: bm.free()` memory safety.
* **When to Use**:
  Mandatory QA gate before applying booleans, modifiers, or final export.
* **Why**:
  Guarantees zero non-manifold defects and verifies compliance with the evaluated triangle budget.

### 2.8 `apply_uv_unwrap` & `export_game_asset`
* **Signature**:
  `apply_uv_unwrap(target_object: str, angle_limit_deg: float = 66.0, island_margin: float = 0.02)`
  `export_game_asset(target_object: str, file_path: str, max_triangles: int = 0, auto_uv: bool = True)`
* **Capabilities**:
  Context-isolated Smart UV unwrapping and production glTF/FBX export with automatic budget decimation.
* **When to Use**:
  Asset completion and delivery phase.

---

## 3. Native BMesh & Modifier Toolkit (The 9 Video Principles)

When low-level mesh manipulation or specialized shading is required in Zone A (`bmesh`), adhere strictly to these proven workflows:

### 3.1 Pre-Boolean Uniform Grid & Quad Repair
* **Problem**: Cutting an aperture into a low-density mesh creates irregular N-gons and causes extreme shading stretching upon subdivision.
* **Workflow**:
  1. Add uniform edge loops (`Ctrl + R`) across the base surface before executing the boolean cut.
  2. Perform the boolean cut (or inset face + `LoopTools > Circle`).
  3. Merge closest vertices with `M > Merge by Distance`.
  4. Connect corner vertices with `J` (Vertex Join) or `Grid Fill` to maintain all-quad topology.
  5. *Remember*: Triangles on flat surfaces are acceptable; keep poles (5+ valence) away from curved boundaries.

### 3.2 The Shrinkwrap Shading Fix (Corner Artifact Elimination)
* **Problem**: Even with good quad flow, subdividing a sharp corner meeting a curved cylinder produces pinching highlights.
* **Workflow**:
  1. Duplicate the clean target curvature curve before cutting (`Shift + D > P` to separate).
  2. Extrude the duplicate to form a smooth reference guide mesh.
  3. On the cut mesh, assign the pinched transition vertices to a new Vertex Group: `VG_ArtifactFix`.
  4. Add a **Shrinkwrap Modifier**: Target = Reference Guide Mesh, Vertex Group = `VG_ArtifactFix`.
  5. The pinching highlights instantly disappear, yielding flawless specular reflections.

### 3.3 Non-Destructive Modifiers & Solidify with Vertex Groups
* **Workflow**:
  - Hollow containers (mugs, bottles, vehicle body panels): Never extrude wall thickness manually inside edit mode.
  - Apply `Solidify Modifier` with `Even Thickness: True`.
  - Use Vertex Groups to vary thickness (e.g., thicker bottom base, thin bottle neck).

### 3.4 Linked Instances (`Alt + D`) with Random Variation
* **Problem**: Copying identical meshes (`Shift + D`) wastes memory and prevents batch editing.
* **Workflow**:
  - Duplicate using `Alt + D` (creates a linked instance sharing `obj.data = master_mesh`).
  - In the shader editor, use the **`Object Info Node` > `Random` socket** plugged into a ColorRamp or Math node to drive subtle color, roughness, or texture coordinate offsets across instances.

### 3.5 Stylized Hair, Cables & Piping with Bezier Curves
* **Workflow**:
  1. Add `Curve > Path` or `Curve > Bezier`.
  2. Set `Object Data Properties > Geometry > Bevel > Object` to a small `Curve > Circle`.
  3. In Edit Mode, select individual curve vertices and press **`Alt + S`** (Curve Radius) to taper tips to zero or fatten centers.

### 3.6 Studio Lighting, Gobos & Light Linking
* **Workflow**:
  - Key, Fill, and Rim 3-point lighting setup.
  - **Gobos**: On Spot/Area lights, enable `Use Nodes`, add an image texture (window blinds, leaves) or `Wave Texture` plugged into light strength to project realistic environmental light breaks.
  - **Light Linking & Shadow Linking**: Isolate hero props (`Object Data Properties > Shading > Light Linking`) to prevent lights blowing out background walls.
