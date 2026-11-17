"""
Procedural Modern Living Room Generator for Blender 4.x / 5.x
Master Archviz Production Standard - 90/10 Hybrid Pipeline
Architectural Digest Penthouse Layout:
- Left Wall: Floor-to-ceiling panoramic window with sheer curtains & terrace.
- Right Wall: Fluted acoustic slat feature wall with floating credenza & OLED TV.
- Back Wall: Minimalist gallery art wall with dropped ceiling LED cove.
- Center: Boucle modular sofa facing TV, dual nesting marble/walnut coffee tables,
  terracotta accent lounge chair, arched brass floor lamp, fiddle-leaf fig plant.
"""

import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix, Euler

# ==============================================================================
# 0. CLEANUP & INITIALIZATION
# ==============================================================================
def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in list(bpy.data.lights):
        if block.users == 0:
            bpy.data.lights.remove(block)
    for block in list(bpy.data.cameras):
        if block.users == 0:
            bpy.data.cameras.remove(block)

def get_or_create_collection(name, parent=None):
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        if parent:
            parent.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    return col

# ==============================================================================
# 1. PBR PROCEDURAL MATERIALS
# ==============================================================================
def setup_materials():
    materials = {}
    
    def create_mat(name):
        mat = bpy.data.materials.get(name)
        if mat:
            bpy.data.materials.remove(mat)
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        return mat

    def set_bsdf_props(bsdf, **kwargs):
        for k, v in kwargs.items():
            if k in bsdf.inputs:
                bsdf.inputs[k].default_value = v

    # 1. Wall Plaster (Warm Greige)
    m = create_mat("Mat_Wall_Plaster")
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{"Base Color": (0.88, 0.86, 0.83, 1.0), "Roughness": 0.85, "Specular IOR Level": 0.3})
    tex_noise = nodes.new("ShaderNodeTexNoise")
    tex_noise.inputs["Scale"].default_value = 80.0
    tex_noise.inputs["Detail"].default_value = 3.0
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.02
    bump.inputs["Distance"].default_value = 0.05
    links.new(tex_noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    materials["plaster"] = m

    # 2. Charcoal Feature Backing
    m = create_mat("Mat_Charcoal_Backing")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{"Base Color": (0.06, 0.06, 0.07, 1.0), "Roughness": 0.95})
    materials["charcoal"] = m

    # 3. Oak Wood (Natural Scandinavian Oak Flooring)
    m = create_mat("Mat_Wood_Oak")
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    tex_coord = nodes.new("ShaderNodeTexCoord")
    mapping = nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (1.5, 6.0, 1.0)
    links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])
    wave = nodes.new("ShaderNodeTexWave")
    wave.wave_type = 'BANDS'
    wave.rings_direction = 'X'
    wave.inputs["Scale"].default_value = 3.0
    wave.inputs["Distortion"].default_value = 1.8
    wave.inputs["Detail"].default_value = 2.5
    links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.2
    ramp.color_ramp.elements[0].color = (0.42, 0.28, 0.16, 1.0)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.72, 0.54, 0.36, 1.0)
    links.new(wave.outputs["Color"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    set_bsdf_props(bsdf, **{"Roughness": 0.38, "Specular IOR Level": 0.5})
    bump_wood = nodes.new("ShaderNodeBump")
    bump_wood.inputs["Strength"].default_value = 0.03
    links.new(wave.outputs["Fac"], bump_wood.inputs["Height"])
    links.new(bump_wood.outputs["Normal"], bsdf.inputs["Normal"])
    materials["oak"] = m

    # 4. Walnut Wood (Slats & Media Console)
    m = create_mat("Mat_Wood_Walnut")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{"Base Color": (0.22, 0.13, 0.08, 1.0), "Roughness": 0.40, "Specular IOR Level": 0.45})
    materials["walnut"] = m

    # 5. Bouclé Sofa Fabric (Warm Cream Ivory)
    m = create_mat("Mat_Fabric_Boucle")
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.86, 0.83, 0.78, 1.0),
        "Roughness": 0.92,
        "Sheen Weight": 0.75,
        "Sheen Roughness": 0.5
    })
    tex_noise2 = nodes.new("ShaderNodeTexNoise")
    tex_noise2.inputs["Scale"].default_value = 160.0
    tex_noise2.inputs["Detail"].default_value = 4.0
    bump_f = nodes.new("ShaderNodeBump")
    bump_f.inputs["Strength"].default_value = 0.05
    bump_f.inputs["Distance"].default_value = 0.02
    links.new(tex_noise2.outputs["Fac"], bump_f.inputs["Height"])
    links.new(bump_f.outputs["Normal"], bsdf.inputs["Normal"])
    materials["boucle"] = m

    # 6. Accent Cushion Fabric (Warm Terracotta)
    m = create_mat("Mat_Cushion_Terracotta")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.65, 0.26, 0.14, 1.0),
        "Roughness": 0.85,
        "Sheen Weight": 0.6
    })
    materials["cushion_terra"] = m

    # 7. Accent Cushion Fabric (Graphite)
    m = create_mat("Mat_Cushion_Graphite")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.14, 0.15, 0.17, 1.0),
        "Roughness": 0.82,
        "Sheen Weight": 0.5
    })
    materials["cushion_graphite"] = m

    # 8. Woven Wool Rug
    m = create_mat("Mat_Rug_Wool")
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.80, 0.77, 0.71, 1.0),
        "Roughness": 0.95,
        "Sheen Weight": 0.8
    })
    tex_noise3 = nodes.new("ShaderNodeTexNoise")
    tex_noise3.inputs["Scale"].default_value = 85.0
    bump_r = nodes.new("ShaderNodeBump")
    bump_r.inputs["Strength"].default_value = 0.10
    links.new(tex_noise3.outputs["Fac"], bump_r.inputs["Height"])
    links.new(bump_r.outputs["Normal"], bsdf.inputs["Normal"])
    materials["rug"] = m

    # 9. Nero Marquina Dark Marble
    m = create_mat("Mat_Marble_Black")
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    tex_noise_m = nodes.new("ShaderNodeTexNoise")
    tex_noise_m.inputs["Scale"].default_value = 4.5
    tex_noise_m.inputs["Detail"].default_value = 8.0
    ramp_m = nodes.new("ShaderNodeValToRGB")
    ramp_m.color_ramp.elements[0].position = 0.58
    ramp_m.color_ramp.elements[0].color = (0.04, 0.04, 0.05, 1.0)
    ramp_m.color_ramp.elements[1].position = 0.64
    ramp_m.color_ramp.elements[1].color = (0.86, 0.87, 0.89, 1.0)
    links.new(tex_noise_m.outputs["Fac"], ramp_m.inputs["Fac"])
    links.new(ramp_m.outputs["Color"], bsdf.inputs["Base Color"])
    set_bsdf_props(bsdf, **{"Roughness": 0.12, "Coat Weight": 0.75, "Coat Roughness": 0.06})
    materials["marble_black"] = m

    # 10. White Calacatta Marble
    m = create_mat("Mat_Marble_White")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{"Base Color": (0.90, 0.90, 0.90, 1.0), "Roughness": 0.14, "Coat Weight": 0.5})
    materials["marble_white"] = m

    # 11. Brushed Warm Brass
    m = create_mat("Mat_Brushed_Brass")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.94, 0.75, 0.40, 1.0),
        "Metallic": 0.95,
        "Roughness": 0.26,
        "Specular IOR Level": 0.6
    })
    materials["brass"] = m

    # 12. Matte Black Metal
    m = create_mat("Mat_Metal_Black")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.07, 0.07, 0.08, 1.0),
        "Metallic": 0.85,
        "Roughness": 0.35
    })
    materials["metal_black"] = m

    # 13. Clear Architectural Glass
    m = create_mat("Mat_Glass_Clear")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.95, 0.98, 1.0, 1.0),
        "Roughness": 0.02,
        "Transmission Weight": 1.0,
        "IOR": 1.52
    })
    materials["glass"] = m

    # 14. Sheer Linen Curtain
    m = create_mat("Mat_Curtain_Sheer")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.92, 0.90, 0.86, 1.0),
        "Roughness": 0.85,
        "Transmission Weight": 0.35,
        "Sheen Weight": 0.7
    })
    materials["curtain"] = m

    # 15. OLED Modern Gallery Artwork ("The Frame" Gallery Screen)
    m = create_mat("Mat_OLED_Screen")
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{"Base Color": (0.03, 0.03, 0.04, 1.0), "Roughness": 0.08, "Specular IOR Level": 0.7})
    tex_noise_art = nodes.new("ShaderNodeTexNoise")
    tex_noise_art.inputs["Scale"].default_value = 2.5
    tex_noise_art.inputs["Detail"].default_value = 6.0
    ramp_art = nodes.new("ShaderNodeValToRGB")
    ramp_art.color_ramp.elements[0].position = 0.28
    ramp_art.color_ramp.elements[0].color = (0.04, 0.08, 0.16, 1.0)
    ramp_art.color_ramp.elements[1].position = 0.68
    ramp_art.color_ramp.elements[1].color = (0.80, 0.48, 0.24, 1.0)
    links.new(tex_noise_art.outputs["Fac"], ramp_art.inputs["Fac"])
    links.new(ramp_art.outputs["Color"], bsdf.inputs["Base Color"])
    set_bsdf_props(bsdf, **{"Emission Color": (0.75, 0.60, 0.45, 1.0), "Emission Strength": 0.9})
    materials["oled"] = m

    # 16. Warm Architectural LED (3000K)
    m = create_mat("Mat_LED_Warm")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (1.0, 0.82, 0.58, 1.0),
        "Emission Color": (1.0, 0.82, 0.58, 1.0),
        "Emission Strength": 12.0
    })
    materials["led_warm"] = m

    # 17. Indoor Plant Leaf
    m = create_mat("Mat_Plant_Leaf")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{
        "Base Color": (0.05, 0.20, 0.07, 1.0),
        "Roughness": 0.25,
        "Subsurface Weight": 0.15,
        "Coat Weight": 0.35,
        "Coat Roughness": 0.15
    })
    materials["plant_leaf"] = m

    # 18. Ceramic Pot (Warm Matte White)
    m = create_mat("Mat_Ceramic_White")
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_bsdf_props(bsdf, **{"Base Color": (0.88, 0.85, 0.81, 1.0), "Roughness": 0.65})
    materials["ceramic"] = m

    # 19. Modern Canvas Wall Art
    m = create_mat("Mat_Canvas_Art")
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    tex_wave_art = nodes.new("ShaderNodeTexWave")
    tex_wave_art.inputs["Scale"].default_value = 1.4
    ramp_canvas = nodes.new("ShaderNodeValToRGB")
    ramp_canvas.color_ramp.elements[0].position = 0.35
    ramp_canvas.color_ramp.elements[0].color = (0.10, 0.12, 0.16, 1.0)
    ramp_canvas.color_ramp.elements[1].position = 0.70
    ramp_canvas.color_ramp.elements[1].color = (0.80, 0.65, 0.48, 1.0)
    links.new(tex_wave_art.outputs["Fac"], ramp_canvas.inputs["Fac"])
    links.new(ramp_canvas.outputs["Color"], bsdf.inputs["Base Color"])
    set_bsdf_props(bsdf, **{"Roughness": 0.85})
    materials["art"] = m

    return materials

# ==============================================================================
# 2. BMESH GEOMETRY UTILITIES
# ==============================================================================
def assign_box_uvs(bm, uv_layer=None, scale=1.0):
    uv = uv_layer or bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = f.normal
        nx, ny, nz = abs(n.x), abs(n.y), abs(n.z)
        for loop in f.loops:
            v = loop.vert.co
            if nx >= ny and nx >= nz:
                loop[uv].uv = (v.y * scale, v.z * scale)
            elif ny >= nx and ny >= nz:
                loop[uv].uv = (v.x * scale, v.z * scale)
            else:
                loop[uv].uv = (v.x * scale, v.y * scale)

def add_box(bm, center, size):
    mat_t = Matrix.Translation(center) @ Matrix.Diagonal(Vector((size[0], size[1], size[2], 1.0)))
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=mat_t)
    return res['verts']

def add_beveled_box(bm, center, size, bevel_radius=0.04, segments=2):
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(center) @ Matrix.Diagonal(Vector((size[0], size[1], size[2], 1.0))))
    if bevel_radius > 0:
        edges = set()
        for v in res['verts']:
            for e in v.link_edges:
                edges.add(e)
        bmesh.ops.bevel(bm, geom=list(edges), offset=bevel_radius, segments=segments, affect='EDGES')
    return res['verts']

def create_mesh_object(name, bm, material=None, collection=None):
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    
    obj = bpy.data.objects.new(name, mesh)
    if material:
        obj.data.materials.append(material)
    (collection or bpy.context.scene.collection).objects.link(obj)
    return obj

# ==============================================================================
# 3. ARCHITECTURE GENERATION
# ==============================================================================
def build_architecture(col, mats):
    # Floor: 5.8m x 6.8m (X: -2.9 to 2.9, Y: -3.4 to 3.4)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1.0)
    bmesh.ops.scale(bm, vec=Vector((2.9, 3.4, 1.0)), verts=bm.verts)
    assign_box_uvs(bm, scale=0.8)
    create_mesh_object("Floor_Oak", bm, mats["oak"], col)
    
    # 1. Back Wall (Y = 3.4, warm plaster finish with gallery niche)
    bm_back = bmesh.new()
    add_box(bm_back, Vector((0.0, 3.4, 1.5)), Vector((5.8, 0.1, 3.0)))
    assign_box_uvs(bm_back, scale=0.5)
    create_mesh_object("Wall_Back_Plaster", bm_back, mats["plaster"], col)

    # 2. Front Wall (Y = -3.4, doorway opening for camera)
    bm_front = bmesh.new()
    add_box(bm_front, Vector((2.1, -3.4, 1.5)), Vector((1.6, 0.1, 3.0)))
    add_box(bm_front, Vector((-2.1, -3.4, 1.5)), Vector((1.6, 0.1, 3.0)))
    add_box(bm_front, Vector((0.0, -3.4, 2.75)), Vector((2.6, 0.1, 0.5)))
    assign_box_uvs(bm_front, scale=0.5)
    create_mesh_object("Wall_Front_Plaster", bm_front, mats["plaster"], col)

    # 3. Left Window Wall Surround (X = -2.9)
    bm_win_wall = bmesh.new()
    add_box(bm_win_wall, Vector((-2.9, 0.0, 2.85)), Vector((0.1, 6.8, 0.3)))
    add_box(bm_win_wall, Vector((-2.9, 0.0, 0.075)), Vector((0.1, 6.8, 0.15)))
    add_box(bm_win_wall, Vector((-2.9, -2.7, 1.5)), Vector((0.1, 1.4, 3.0)))
    add_box(bm_win_wall, Vector((-2.9, 2.7, 1.5)), Vector((0.1, 1.4, 3.0)))
    assign_box_uvs(bm_win_wall, scale=0.5)
    create_mesh_object("Wall_Window_Surround", bm_win_wall, mats["plaster"], col)

    # Architectural Window Frame & Mullions (X = -2.9)
    bm_frame = bmesh.new()
    win_w = 4.2
    win_h = 2.55
    z_mid = (0.15 + 2.70) / 2
    for y_pos in [-2.1, -0.7, 0.7, 2.1]:
        add_box(bm_frame, Vector((-2.9, y_pos, z_mid)), Vector((0.08, 0.06, win_h)))
    for z_pos in [0.15, 2.05, 2.7]:
        add_box(bm_frame, Vector((-2.9, 0.0, z_pos)), Vector((0.08, win_w, 0.06)))
    create_mesh_object("Window_Mullions", bm_frame, mats["metal_black"], col)

    # Window Glass Pane
    bm_glass = bmesh.new()
    add_box(bm_glass, Vector((-2.9, 0.0, z_mid)), Vector((0.015, win_w, win_h)))
    create_mesh_object("Window_Glass", bm_glass, mats["glass"], col)

    # Outdoor Balcony Terrace
    bm_out = bmesh.new()
    add_box(bm_out, Vector((-4.6, 0.0, -0.05)), Vector((3.2, 7.6, 0.2)))
    add_box(bm_out, Vector((-5.8, 0.0, 0.55)), Vector((0.05, 7.2, 1.1)))
    create_mesh_object("Balcony_Terrace", bm_out, mats["charcoal"], col)

    # Sheer Pleated Window Curtains (Left & Right)
    bm_curtains = bmesh.new()
    num_pleats = 16
    for side_idx, y_center in enumerate([-2.0, 2.0]):
        for z_i in range(12):
            z_curr = 0.15 + (z_i / 11.0) * 2.55
            for p_i in range(num_pleats):
                t = p_i / float(num_pleats - 1)
                y_p = y_center + (t - 0.5) * 0.75
                x_p = -2.78 + math.sin(t * math.pi * 8) * 0.04
                bm_curtains.verts.new((x_p, y_p, z_curr))
    bm_curtains.verts.ensure_lookup_table()
    for side_idx in range(2):
        base_v = side_idx * (12 * num_pleats)
        for z_i in range(11):
            for p_i in range(num_pleats - 1):
                i0 = base_v + z_i * num_pleats + p_i
                i1 = i0 + 1
                i2 = i0 + num_pleats + 1
                i3 = i0 + num_pleats
                bm_curtains.faces.new((bm_curtains.verts[i0], bm_curtains.verts[i1], bm_curtains.verts[i2], bm_curtains.verts[i3]))
    bmesh.ops.recalc_face_normals(bm_curtains, faces=bm_curtains.faces)
    create_mesh_object("Window_Curtains_Sheer", bm_curtains, mats["curtain"], col)

    # 4. Right Wall Shell (Surrounding Feature Slat Wall)
    bm_rw = bmesh.new()
    # Sections flanking the feature slat wall (slat wall is from Y: -1.7 to 1.7)
    add_box(bm_rw, Vector((2.9, -2.5, 1.5)), Vector((0.1, 1.8, 3.0)))
    add_box(bm_rw, Vector((2.9, 2.5, 1.5)), Vector((0.1, 1.8, 3.0)))
    add_box(bm_rw, Vector((2.9, 0.0, 2.925)), Vector((0.1, 3.4, 0.15)))
    add_box(bm_rw, Vector((2.9, 0.0, 0.05)), Vector((0.1, 3.4, 0.10)))
    assign_box_uvs(bm_rw, scale=0.5)
    create_mesh_object("Wall_Right_Surround", bm_rw, mats["plaster"], col)

    # 5. Ceiling with Recessed Perimeter Cove
    bm_ceil = bmesh.new()
    add_box(bm_ceil, Vector((0.0, 0.0, 2.96)), Vector((5.0, 6.0, 0.08)))
    create_mesh_object("Ceiling_Dropped", bm_ceil, mats["plaster"], col)

    bm_top = bmesh.new()
    add_box(bm_top, Vector((0.0, 0.0, 3.05)), Vector((5.8, 6.8, 0.1)))
    create_mesh_object("Ceiling_Main_Slab", bm_top, mats["plaster"], col)

    # Perimeter LED Cove Strip
    bm_cove = bmesh.new()
    add_box(bm_cove, Vector((0.0, 3.02, 2.98)), Vector((5.1, 0.03, 0.02)))
    add_box(bm_cove, Vector((0.0, -3.02, 2.98)), Vector((5.1, 0.03, 0.02)))
    add_box(bm_cove, Vector((2.52, 0.0, 2.98)), Vector((0.03, 6.1, 0.02)))
    add_box(bm_cove, Vector((-2.52, 0.0, 2.98)), Vector((0.03, 6.1, 0.02)))
    create_mesh_object("Ceiling_LED_Cove", bm_cove, mats["led_warm"], col)

    # Baseboards (Skirting)
    bm_skirt = bmesh.new()
    add_box(bm_skirt, Vector((0.0, 3.36, 0.05)), Vector((5.6, 0.02, 0.10)))
    add_box(bm_skirt, Vector((2.86, 0.0, 0.05)), Vector((0.02, 6.7, 0.10)))
    create_mesh_object("Baseboards", bm_skirt, mats["plaster"], col)

# ==============================================================================
# 4. RIGHT FEATURE WALL: FLUTED SLATS, FLOATING CREDENZA, 75" OLED TV
# ==============================================================================
def build_feature_slat_wall(col, mats):
    # Located along Right Wall (X = 2.9, spanning Y: -1.7 to 1.7, Z: 0.1 to 2.85)
    
    # 1. Acoustic Felt Backing (Charcoal)
    bm_back = bmesh.new()
    add_box(bm_back, Vector((2.88, 0.0, 1.475)), Vector((0.02, 3.42, 2.75)))
    create_mesh_object("Feature_Acoustic_Backing", bm_back, mats["charcoal"], col)

    # 2. Concealed LED Halo around slat panel
    bm_halo = bmesh.new()
    add_box(bm_halo, Vector((2.86, -1.71, 1.475)), Vector((0.02, 0.02, 2.70)))
    add_box(bm_halo, Vector((2.86, 1.71, 1.475)), Vector((0.02, 0.02, 2.70)))
    add_box(bm_halo, Vector((2.86, 0.0, 2.84)), Vector((0.02, 3.42, 0.02)))
    create_mesh_object("Feature_LED_Backlight", bm_halo, mats["led_warm"], col)

    # 3. Vertical Walnut Slats (Single-Buffer BMesh batching)
    bm_slats = bmesh.new()
    slat_d = 0.022 # Depth extending into room (-X)
    slat_w = 0.032 # Width along Y
    slat_h = 2.74 # Height in Z
    slat_gap = 0.036
    num_slats = 48
    start_y = -((num_slats - 1) * (slat_w + slat_gap)) / 2.0
    
    for i in range(num_slats):
        y = start_y + i * (slat_w + slat_gap)
        add_box(bm_slats, Vector((2.85, y, 1.475)), Vector((slat_d, slat_w, slat_h)))

    assign_box_uvs(bm_slats, scale=1.0)
    create_mesh_object("Feature_Wood_Slats", bm_slats, mats["walnut"], col)

    # 4. Floating Walnut Media Credenza (Mounted on right wall)
    bm_cred = bmesh.new()
    cred_d, cred_w, cred_h = 0.40, 2.4, 0.36
    cred_x = 2.85 - cred_d / 2.0
    cred_z = 0.28 + cred_h / 2.0
    add_beveled_box(bm_cred, Vector((cred_x, 0.0, cred_z)), Vector((cred_d, cred_w, cred_h)), bevel_radius=0.02, segments=2)
    # Nero Marquina Marble Slab Top
    add_beveled_box(bm_cred, Vector((cred_x - 0.01, 0.0, cred_z + cred_h/2.0 + 0.015)), Vector((cred_d + 0.03, cred_w + 0.04, 0.03)), bevel_radius=0.008, segments=2)
    assign_box_uvs(bm_cred, scale=0.8)
    create_mesh_object("Media_Credenza", bm_cred, mats["walnut"], col)

    # 5. 75-inch Ultra-Thin Modern OLED TV ("The Frame")
    bm_tv = bmesh.new()
    tv_w = 1.68
    tv_h = 0.96
    tv_z = 1.55
    tv_x = 2.83
    add_box(bm_tv, Vector((tv_x, 0.0, tv_z)), Vector((0.02, tv_w, tv_h)))
    create_mesh_object("TV_Bezel", bm_tv, mats["metal_black"], col)

    # TV Screen Face (Facing -X towards the room & sofa)
    bm_screen = bmesh.new()
    bmesh.ops.create_grid(bm_screen, x_segments=1, y_segments=1, size=1.0)
    # Rotate grid to face -X
    bmesh.ops.rotate(bm_screen, cent=Vector((0,0,0)), matrix=Euler((0, math.radians(-90), 0)).to_matrix(), verts=bm_screen.verts)
    bmesh.ops.scale(bm_screen, vec=Vector((1.0, tv_w * 0.495, tv_h * 0.495)), verts=bm_screen.verts)
    bmesh.ops.translate(bm_screen, vec=Vector((tv_x - 0.011, 0.0, tv_z)), verts=bm_screen.verts)
    assign_box_uvs(bm_screen, scale=1.0)
    create_mesh_object("TV_Display_Screen", bm_screen, mats["oled"], col)

# ==============================================================================
# 5. FURNITURE GENERATION (SOFA FACING TV ON RIGHT, COFFEE TABLES, CHAIR)
# ==============================================================================
def build_furniture(col, mats):
    # 1. Luxury Area Rug (Center of seating area)
    bm_rug = bmesh.new()
    rug_w, rug_l, rug_thick = 3.0, 3.6, 0.016
    # Placed under sofa and coffee table: X from -1.4 to 1.6, Y from -1.8 to 1.8
    add_box(bm_rug, Vector((0.10, 0.0, rug_thick / 2.0)), Vector((rug_w, rug_l, rug_thick)))
    assign_box_uvs(bm_rug, scale=1.5)
    rug_obj = create_mesh_object("Area_Rug", bm_rug, mats["rug"], col)
    bev = rug_obj.modifiers.new("Bevel", 'BEVEL')
    bev.width = 0.12
    bev.segments = 4

    # 2. Modern Low-Profile Modular Sofa (FACING +X TOWARDS THE TV WALL!)
    # Position: Left side of room (X = -0.7), facing +X!
    bm_sofa = bmesh.new()
    
    # A. Recessed Walnut/Dark Plinth Base
    # Main bench base: Y from -0.9 to +1.0, X from -1.15 to -0.25
    add_box(bm_sofa, Vector((-0.70, 0.05, 0.04)), Vector((0.90, 1.95, 0.08)))
    # Chaise base on rear/left: Y from +0.9 to +1.7, X from -1.15 to +0.45
    add_box(bm_sofa, Vector((-0.35, 1.30, 0.04)), Vector((1.60, 0.80, 0.08)))
    
    # B. Plush Seat Cushions (Facing +X)
    # 2 Main seat cushions (Front & Center)
    for y_pos in [-0.45, 0.45]:
        add_beveled_box(bm_sofa, Vector((-0.60, y_pos, 0.24)), Vector((0.85, 0.85, 0.32)), bevel_radius=0.06, segments=3)
    
    # Chaise Cushion extending towards +X
    add_beveled_box(bm_sofa, Vector((-0.25, 1.30, 0.24)), Vector((1.55, 0.80, 0.32)), bevel_radius=0.06, segments=3)

    # C. Backrest along the rear (at X = -1.05, running along Y, facing +X)
    add_beveled_box(bm_sofa, Vector((-1.05, 0.50, 0.50)), Vector((0.24, 2.70, 0.44)), bevel_radius=0.06, segments=3)

    # D. Front Armrest (at Y = -0.95, X = -0.60)
    add_beveled_box(bm_sofa, Vector((-0.60, -0.95, 0.40)), Vector((0.85, 0.24, 0.32)), bevel_radius=0.05, segments=3)

    assign_box_uvs(bm_sofa, scale=1.0)
    sofa_obj = create_mesh_object("Sofa_Modular_Boucle", bm_sofa, mats["boucle"], col)
    for p in sofa_obj.data.polygons:
        p.use_smooth = True

    # 3. Throw Pillows / Cushions (Resting against the backrest at X = -0.88, visible to camera)
    def build_pillow(name, pos, rot_z, scale_xyz, mat):
        bm_p = bmesh.new()
        bmesh.ops.create_grid(bm_p, x_segments=6, y_segments=6, size=1.0)
        r = bmesh.ops.extrude_face_region(bm_p, geom=bm_p.faces[:])
        verts_ext = [v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm_p, vec=Vector((0, 0, 0.12)), verts=verts_ext)
        for v in bm_p.verts:
            dist_center = math.sqrt(v.co.x**2 + v.co.y**2)
            z_factor = max(0.1, 1.0 - (dist_center * 1.3)**2)
            v.co.z = (v.co.z - 0.06) * z_factor
        
        # Leaning against backrest (tilted in Y and rotated)
        mat_t = Matrix.Translation(pos) @ Euler((math.radians(5), math.radians(-15), math.radians(rot_z))).to_matrix().to_4x4() @ Matrix.Diagonal(Vector((scale_xyz[0], scale_xyz[1], scale_xyz[2], 1.0)))
        bmesh.ops.transform(bm_p, matrix=mat_t, verts=bm_p.verts)
        bmesh.ops.recalc_face_normals(bm_p, faces=bm_p.faces)
        assign_box_uvs(bm_p, scale=1.0)
        p_obj = create_mesh_object(name, bm_p, mat, col)
        for poly in p_obj.data.polygons:
            poly.use_smooth = True
        sub = p_obj.modifiers.new("Subsurf", 'SUBSURF')
        sub.levels = 1
        return p_obj

    build_pillow("Pillow_Terra_1", Vector((-0.85, -0.40, 0.46)), 8, (0.40, 0.40, 1.0), mats["cushion_terra"])
    build_pillow("Pillow_Graphite_1", Vector((-0.85, 0.35, 0.46)), -12, (0.42, 0.42, 1.0), mats["cushion_graphite"])
    build_pillow("Pillow_Terra_2", Vector((-0.85, 1.15, 0.46)), 24, (0.38, 0.38, 1.0), mats["cushion_terra"])

    # 4. Nesting Designer Coffee Tables (Centered in front of the sofa)
    # Table A (Hero): Circular Nero Marquina Dark Marble Table
    bm_t1 = bmesh.new()
    radius_1 = 0.42
    height_1 = 0.38
    t1_center = Vector((0.40, -0.15, 0.0))
    bmesh.ops.create_cone(bm_t1, cap_ends=True, radius1=radius_1, radius2=radius_1, depth=0.025, segments=36,
                          matrix=Matrix.Translation(Vector((t1_center.x, t1_center.y, height_1 - 0.0125))))
    assign_box_uvs(bm_t1, scale=1.0)
    create_mesh_object("Coffee_Table_Marble_Top", bm_t1, mats["marble_black"], col)

    # Brass Legs for Table A
    bm_legs1 = bmesh.new()
    for angle in [30, 150, 270]:
        rad = math.radians(angle)
        lx = t1_center.x + math.cos(rad) * (radius_1 - 0.06)
        ly = t1_center.y + math.sin(rad) * (radius_1 - 0.06)
        bmesh.ops.create_cone(bm_legs1, cap_ends=True, radius1=0.016, radius2=0.016, depth=height_1 - 0.025, segments=16,
                              matrix=Matrix.Translation(Vector((lx, ly, (height_1 - 0.025) / 2.0))))
    create_mesh_object("Coffee_Table_Brass_Legs", bm_legs1, mats["brass"], col)

    # Table B (Nested Lower): Organic Smoked Walnut Table
    bm_t2 = bmesh.new()
    radius_2 = 0.30
    height_2 = 0.30
    t2_center = Vector((0.72, 0.38, 0.0))
    bmesh.ops.create_cone(bm_t2, cap_ends=True, radius1=radius_2, radius2=radius_2, depth=0.03, segments=32,
                          matrix=Matrix.Translation(Vector((t2_center.x, t2_center.y, height_2 - 0.015))))
    for angle in [45, 165, 285]:
        rad = math.radians(angle)
        lx = t2_center.x + math.cos(rad) * (radius_2 - 0.05)
        ly = t2_center.y + math.sin(rad) * (radius_2 - 0.05)
        bmesh.ops.create_cone(bm_t2, cap_ends=True, radius1=0.022, radius2=0.018, depth=height_2 - 0.03, segments=16,
                              matrix=Matrix.Translation(Vector((lx, ly, (height_2 - 0.03) / 2.0))))
    assign_box_uvs(bm_t2, scale=1.0)
    create_mesh_object("Coffee_Table_Walnut_Secondary", bm_t2, mats["walnut"], col)

    # 5. Designer Curved Accent Lounge Chair
    # Positioned at front-center, angled facing towards sofa and coffee table
    bm_chair = bmesh.new()
    chair_pos = Vector((0.25, -1.35, 0.0))
    chair_rot = math.radians(45) # Angled towards seating center
    
    # Rounded Seat Cushion
    bmesh.ops.create_cone(bm_chair, cap_ends=True, radius1=0.38, radius2=0.36, depth=0.12, segments=24,
                          matrix=Matrix.Translation(Vector((0, 0, 0.32))))
    
    # Barrel backrest volume
    arc_verts = []
    num_arc = 16
    for i in range(num_arc):
        a = math.pi * 0.15 + (i / float(num_arc - 1)) * math.pi * 1.05
        ax = math.cos(a) * 0.38
        ay = math.sin(a) * 0.38
        v_bot = bm_chair.verts.new((ax, ay, 0.34))
        v_top = bm_chair.verts.new((ax * 1.05, ay * 1.05, 0.72))
        arc_verts.append((v_bot, v_top))
    for i in range(num_arc - 1):
        b0, t0 = arc_verts[i]
        b1, t1 = arc_verts[i+1]
        bm_chair.faces.new((b0, b1, t1, t0))

    # Slim Dark Metal Legs
    for lx, ly in [(-0.25, -0.22), (0.25, -0.22), (-0.24, 0.25), (0.24, 0.25)]:
        bmesh.ops.create_cone(bm_chair, cap_ends=True, radius1=0.016, radius2=0.012, depth=0.36, segments=12,
                              matrix=Matrix.Translation(Vector((lx, ly, 0.18))))

    mat_chair_world = Matrix.Translation(chair_pos) @ Matrix.Rotation(chair_rot, 4, 'Z')
    bmesh.ops.transform(bm_chair, matrix=mat_chair_world, verts=bm_chair.verts)
    bmesh.ops.recalc_face_normals(bm_chair, faces=bm_chair.faces)
    assign_box_uvs(bm_chair, scale=1.0)
    chair_obj = create_mesh_object("Accent_Lounge_Chair", bm_chair, mats["cushion_terra"], col)
    for p in chair_obj.data.polygons:
        p.use_smooth = True
    sub_ch = chair_obj.modifiers.new("Subsurf", 'SUBSURF')
    sub_ch.levels = 1

    # 6. Sculptural Arched Floor Lamp (Standing behind sofa, arching over)
    bm_lamp_base = bmesh.new()
    lamp_base_pos = Vector((-1.65, -0.65, 0.0))
    bmesh.ops.create_cone(bm_lamp_base, cap_ends=True, radius1=0.18, radius2=0.18, depth=0.10, segments=24,
                          matrix=Matrix.Translation(Vector((lamp_base_pos.x, lamp_base_pos.y, 0.05))))
    create_mesh_object("Floor_Lamp_Marble_Base", bm_lamp_base, mats["marble_white"], col)

    # Curved Arched Brass Stem
    bm_lamp_stem = bmesh.new()
    stem_points = []
    num_stem = 20
    for i in range(num_stem):
        t = i / float(num_stem - 1)
        sz = 0.1 + math.sin(t * math.pi * 0.72) * 2.25
        sx = lamp_base_pos.x + t * 1.35
        sy = lamp_base_pos.y + t * 0.50
        stem_points.append(Vector((sx, sy, sz)))
    for i in range(num_stem - 1):
        pA = stem_points[i]
        pB = stem_points[i+1]
        diff = pB - pA
        dist = diff.length
        if dist > 0.001:
            mid = (pA + pB) / 2.0
            rot = Vector((0, 0, 1)).rotation_difference(diff).to_matrix().to_4x4()
            bmesh.ops.create_cone(bm_lamp_stem, cap_ends=False, radius1=0.012, radius2=0.012, depth=dist, segments=8,
                                  matrix=Matrix.Translation(mid) @ rot)
    create_mesh_object("Floor_Lamp_Arched_Stem", bm_lamp_stem, mats["brass"], col)

    # Dome Shade & Warm Bulb
    bm_shade = bmesh.new()
    shade_end = stem_points[-1]
    bmesh.ops.create_cone(bm_shade, cap_ends=True, radius1=0.20, radius2=0.06, depth=0.12, segments=24,
                          matrix=Matrix.Translation(shade_end + Vector((0, 0, 0.06))))
    create_mesh_object("Floor_Lamp_Dome_Shade", bm_shade, mats["brass"], col)

    bm_bulb = bmesh.new()
    bmesh.ops.create_icosphere(bm_bulb, radius=0.045, subdivisions=2,
                               matrix=Matrix.Translation(shade_end + Vector((0, 0, 0.02))))
    create_mesh_object("Floor_Lamp_Bulb_Emission", bm_bulb, mats["led_warm"], col)

# ==============================================================================
# 6. DECOR, FOLIAGE & ACCESSORIES
# ==============================================================================
def build_decor_and_props(col, mats):
    # 1. Back Wall Large Gallery Canvas Art
    bm_art = bmesh.new()
    add_box(bm_art, Vector((-0.2, 3.36, 1.65)), Vector((1.48, 0.04, 1.88)))
    create_mesh_object("Canvas_Art_Frame", bm_art, mats["brass"], col)

    bm_canvas = bmesh.new()
    bmesh.ops.create_grid(bm_canvas, x_segments=1, y_segments=1, size=1.0)
    bmesh.ops.rotate(bm_canvas, cent=Vector((0,0,0)), matrix=Euler((math.radians(90), 0, 0)).to_matrix(), verts=bm_canvas.verts)
    bmesh.ops.scale(bm_canvas, vec=Vector((1.40 * 0.5, 1.0, 1.80 * 0.5)), verts=bm_canvas.verts)
    bmesh.ops.translate(bm_canvas, vec=Vector((-0.2, 3.33, 1.65)), verts=bm_canvas.verts)
    assign_box_uvs(bm_canvas, scale=1.0)
    create_mesh_object("Canvas_Art_Painting", bm_canvas, mats["art"], col)

    # 2. Table Decor: Hardcover Architecture Book + Ceramic Coffee Cup
    bm_table_props = bmesh.new()
    # Book on Dark Marble Table
    mat_bk = Matrix.Translation(Vector((0.35, -0.12, 0.395))) @ Matrix.Rotation(math.radians(-18), 4, 'Z') @ Matrix.Diagonal(Vector((0.24, 0.32, 0.03, 1.0)))
    bmesh.ops.create_cube(bm_table_props, size=1.0, matrix=mat_bk)
    # Minimalist Ceramic Coffee Cup
    bmesh.ops.create_cone(bm_table_props, cap_ends=True, radius1=0.038, radius2=0.032, depth=0.07, segments=16,
                          matrix=Matrix.Translation(Vector((0.55, -0.15, 0.415))))
    # Sculptural Ceramic Dish on Walnut Table
    bmesh.ops.create_cone(bm_table_props, cap_ends=True, radius1=0.065, radius2=0.045, depth=0.035, segments=16,
                          matrix=Matrix.Translation(Vector((0.72, 0.38, 0.32))))
    create_mesh_object("Coffee_Table_Accessories", bm_table_props, mats["ceramic"], col)

    # 3. Lush Indoor Architectural Plant (Fiddle-Leaf Fig in corner near window)
    plant_pos = Vector((-2.25, 2.30, 0.0))
    bm_pot = bmesh.new()
    bmesh.ops.create_cone(bm_pot, cap_ends=True, radius1=0.22, radius2=0.20, depth=0.42, segments=24,
                          matrix=Matrix.Translation(Vector((plant_pos.x, plant_pos.y, 0.38))))
    bmesh.ops.create_circle(bm_pot, cap_ends=True, radius=0.21, segments=20,
                            matrix=Matrix.Translation(Vector((plant_pos.x, plant_pos.y, 0.56))))
    for a in [0, 120, 240]:
        rad = math.radians(a)
        lx = plant_pos.x + math.cos(rad) * 0.23
        ly = plant_pos.y + math.sin(rad) * 0.23
        bmesh.ops.create_cone(bm_pot, cap_ends=True, radius1=0.018, radius2=0.018, depth=0.48, segments=12,
                              matrix=Matrix.Translation(Vector((lx, ly, 0.24))))
    create_mesh_object("Indoor_Plant_Planter_Pot", bm_pot, mats["ceramic"], col)

    # Plant Stems & Broad Glossy Leaves
    bm_plant = bmesh.new()
    stem_branches = [
        (plant_pos + Vector((0, 0, 0.55)), plant_pos + Vector((0.08, 0.05, 1.45)), 7),
        (plant_pos + Vector((0, 0, 0.70)), plant_pos + Vector((0.35, -0.15, 1.25)), 5),
        (plant_pos + Vector((0, 0, 0.85)), plant_pos + Vector((-0.25, 0.20, 1.35)), 5),
        (plant_pos + Vector((0, 0, 0.65)), plant_pos + Vector((-0.18, -0.22, 1.10)), 4),
    ]
    
    for p_start, p_end, n_leaves in stem_branches:
        diff = p_end - p_start
        dist = diff.length
        rot = Vector((0, 0, 1)).rotation_difference(diff).to_matrix().to_4x4()
        bmesh.ops.create_cone(bm_plant, cap_ends=True, radius1=0.022, radius2=0.010, depth=dist, segments=8,
                              matrix=Matrix.Translation((p_start + p_end) / 2.0) @ rot)
        
        for leaf_i in range(n_leaves):
            frac = (leaf_i + 1) / float(n_leaves)
            leaf_origin = p_start + diff * frac
            leaf_angle = leaf_i * 2.39996 + frac * 3.14
            leaf_dir = Vector((math.cos(leaf_angle), math.sin(leaf_angle), 0.35)).normalized()
            leaf_len = 0.26 + random.uniform(-0.03, 0.05)
            leaf_w = 0.14
            
            v0 = bm_plant.verts.new(leaf_origin)
            v1 = bm_plant.verts.new(leaf_origin + leaf_dir * (leaf_len * 0.4) + Vector((-leaf_dir.y, leaf_dir.x, 0)) * (leaf_w * 0.5))
            v2 = bm_plant.verts.new(leaf_origin + leaf_dir * leaf_len + Vector((0, 0, -0.04)))
            v3 = bm_plant.verts.new(leaf_origin + leaf_dir * (leaf_len * 0.4) - Vector((-leaf_dir.y, leaf_dir.x, 0)) * (leaf_w * 0.5))
            bm_plant.faces.new((v0, v1, v2, v3))

    bmesh.ops.recalc_face_normals(bm_plant, faces=bm_plant.faces)
    plant_obj = create_mesh_object("Fiddle_Leaf_Fig_Foliage", bm_plant, mats["plant_leaf"], col)
    for p in plant_obj.data.polygons:
        p.use_smooth = True

# ==============================================================================
# 7. CINEMATIC LIGHTING & ARCHVIZ CAMERA
# ==============================================================================
def setup_lighting_and_camera(col_lights, col_cam):
    # World background: Soft sunny daylight
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.74, 0.84, 0.96, 1.0)
        bg.inputs["Strength"].default_value = 1.3

    # 1. Natural Sunlight Streaming Through the Window (Left Wall)
    sun_data = bpy.data.lights.new(name="Sun_Window_Light", type='SUN')
    sun_data.energy = 4.2
    sun_data.color = (1.0, 0.94, 0.84)
    sun_data.angle = math.radians(5.0)
    sun_obj = bpy.data.objects.new(name="Sun_Window_Light", object_data=sun_data)
    sun_obj.location = Vector((-5.5, -1.0, 3.8))
    sun_obj.rotation_euler = Euler((math.radians(48), math.radians(16), math.radians(-65)))
    col_lights.objects.link(sun_obj)

    # 2. Window Portal / Area Fill Light (Diffused Sky Daylight)
    sky_fill_data = bpy.data.lights.new(name="Sky_Window_Portal", type='AREA')
    sky_fill_data.energy = 140.0
    sky_fill_data.color = (0.86, 0.92, 1.0)
    sky_fill_data.size = 4.2
    sky_fill_data.size_y = 2.5
    sky_fill_obj = bpy.data.objects.new(name="Sky_Window_Portal", object_data=sky_fill_data)
    sky_fill_obj.location = Vector((-2.95, 0.0, 1.45))
    sky_fill_obj.rotation_euler = Euler((0, math.radians(90), 0))
    col_lights.objects.link(sky_fill_obj)

    # 3. Floor Lamp Practical Point Light
    lamp_pt_data = bpy.data.lights.new(name="Floor_Lamp_Light", type='POINT')
    lamp_pt_data.energy = 35.0
    lamp_pt_data.color = (1.0, 0.82, 0.58)
    lamp_pt_data.shadow_soft_size = 0.15
    lamp_pt_obj = bpy.data.objects.new(name="Floor_Lamp_Light", object_data=lamp_pt_data)
    lamp_pt_obj.location = Vector((-0.30, -0.15, 1.85))
    col_lights.objects.link(lamp_pt_obj)

    # 4. Recessed Ceiling Spotlights (Warm focused illumination)
    spots_config = [
        ("Spot_Credenza_L", Vector((2.4, -0.8, 2.92)), 55.0, 45, (0, math.radians(-14), 0)),
        ("Spot_Credenza_R", Vector((2.4, 0.8, 2.92)), 55.0, 45, (0, math.radians(-14), 0)),
        ("Spot_Art_Wall", Vector((-0.2, 2.6, 2.92)), 65.0, 42, (math.radians(-14), 0, 0)),
    ]
    for s_name, s_pos, s_nrg, s_cone, s_rot in spots_config:
        sp_data = bpy.data.lights.new(name=s_name, type='SPOT')
        sp_data.energy = s_nrg
        sp_data.color = (1.0, 0.88, 0.72)
        sp_data.spot_size = math.radians(s_cone)
        sp_data.spot_blend = 0.35
        sp_data.shadow_soft_size = 0.08
        sp_obj = bpy.data.objects.new(name=s_name, object_data=sp_data)
        sp_obj.location = s_pos
        sp_obj.rotation_euler = Euler(s_rot)
        col_lights.objects.link(sp_obj)

    # 5. Archviz Camera (Human Standing Eye Level, 28mm Lens)
    cam_data = bpy.data.cameras.new(name="Archviz_Hero_Camera")
    cam_data.lens = 28.0
    cam_data.sensor_width = 36.0
    cam_data.clip_start = 0.1
    cam_data.clip_end = 100.0
    cam_data.show_composition_thirds = True
    
    cam_obj = bpy.data.objects.new(name="Archviz_Hero_Camera", object_data=cam_data)
    # Position: Slightly left of center at entry (X = -0.35, Y = -3.20, Z = 1.35)
    cam_obj.location = Vector((-0.35, -3.20, 1.35))
    # Rotated slightly towards +X to encompass window on left, seating in middle, TV wall on right
    cam_obj.rotation_euler = Euler((math.radians(82.0), 0.0, math.radians(11.0)))
    
    col_cam.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # 6. EEVEE Next Raytracing & Quality
    scene = bpy.context.scene
    eevee = scene.eevee
    eevee.use_raytracing = True
    eevee.fast_gi_quality = 1.0
    eevee.fast_gi_ray_count = 4
    eevee.fast_gi_step_count = 16
    eevee.shadow_ray_count = 2
    eevee.shadow_step_count = 12
    eevee.taa_samples = 32

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    if hasattr(scene.view_settings, "view_transform"):
        try:
            scene.view_settings.view_transform = 'AgX'
            scene.view_settings.look = 'Medium High Contrast'
            scene.view_settings.exposure = -0.2
        except Exception:
            scene.view_settings.view_transform = 'Filmic'

# ==============================================================================
# 8. MASTER GENERATOR PIPELINE
# ==============================================================================
def generate_modern_living_room():
    print(">>> [ARCHVIZ PIPELINE] Starting Master Penthouse Living Room generation...")
    clean_scene()
    
    col_arch = get_or_create_collection("01_ARCHITECTURE")
    col_feat = get_or_create_collection("02_FEATURE_WALL")
    col_furn = get_or_create_collection("03_FURNITURE")
    col_prop = get_or_create_collection("04_PROPS_DECOR")
    col_lgt  = get_or_create_collection("05_LIGHTS")
    col_cam  = get_or_create_collection("06_CAMERA")

    print(">>> Generating PBR materials...")
    mats = setup_materials()

    print(">>> Building architecture shell (walls, floor, window, ceiling, cove)...")
    build_architecture(col_arch, mats)

    print(">>> Building fluted acoustic slat feature wall, OLED TV, floating credenza on right wall...")
    build_feature_slat_wall(col_feat, mats)

    print(">>> Building luxury modular sofa, pillows, nesting coffee tables, lounge chair, arch lamp...")
    build_furniture(col_furn, mats)

    print(">>> Building back wall gallery art, coffee table props, fiddle-leaf fig plant...")
    build_decor_and_props(col_prop, mats)

    print(">>> Rigging sunlight, sky fill, spotlights, practicals and 28mm hero camera...")
    setup_lighting_and_camera(col_lgt, col_cam)

    print(">>> [ARCHVIZ PIPELINE] Master Modern Living Room generated successfully!")

# Run immediately
generate_modern_living_room()
