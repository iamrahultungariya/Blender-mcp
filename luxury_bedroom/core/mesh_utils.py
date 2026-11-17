"""BMesh Procedural Utilities & Helpers (Zone A - C-RAM Execution).

High-performance procedural geometry operators:
- Zero UI context (no bpy.ops inside construction loops)
- Anti-boxy beveled boxes, cylinders, and collection utilities
"""
from __future__ import annotations

import math
import bpy
import bmesh
from mathutils import Vector


def get_or_create_collection(name: str, parent: bpy.types.Collection | None = None) -> bpy.types.Collection:
    """Ensure a collection exists and is linked to parent."""
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    target_parent = parent or bpy.context.scene.collection
    target_parent.children.link(col)
    return col


def clear_collection_objects(col: bpy.types.Collection) -> None:
    """Safely unlink and remove all objects in a collection."""
    for obj in list(col.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def bmesh_to_object(
    bm: bmesh.types.BMesh,
    name: str,
    collection: bpy.types.Collection,
    material: bpy.types.Material | None = None,
    smooth: bool = True,
) -> bpy.types.Object:
    """Commit BMesh to a new Blender object and link to target collection."""
    mesh_data = bpy.data.meshes.new(name)
    bm.to_mesh(mesh_data)
    bm.free()

    if smooth:
        for p in mesh_data.polygons:
            p.use_smooth = True

    obj = bpy.data.objects.new(name, mesh_data)
    if material:
        obj.data.materials.append(material)

    collection.objects.link(obj)
    return obj


def create_beveled_box(
    width: float,
    length: float,
    height: float,
    bevel_radius: float = 0.02,
    segments: int = 2,
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bmesh.types.BMesh:
    """Construct an anti-boxy beveled solid box in memory via BMesh."""
    bm = bmesh.new()
    ox, oy, oz = offset

    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, length, height), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(ox, oy, oz + height / 2.0), verts=bm.verts)

    if bevel_radius > 0.001:
        edges = list(bm.edges)
        bmesh.ops.bevel(
            bm,
            geom=edges,
            offset=bevel_radius,
            offset_type="OFFSET",
            segments=segments,
            profile=0.5,
            affect="EDGES",
        )

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def create_cylinder(
    radius: float,
    height: float,
    segments: int = 24,
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bmesh.types.BMesh:
    """Generate a clean cylinder centered on offset."""
    bm = bmesh.new()
    ox, oy, oz = offset

    top_ring = []
    bot_ring = []

    for i in range(segments):
        theta = (2.0 * math.pi * i) / segments
        x = ox + radius * math.cos(theta)
        y = oy + radius * math.sin(theta)
        top_ring.append(bm.verts.new(Vector((x, y, oz + height))))
        bot_ring.append(bm.verts.new(Vector((x, y, oz))))

    for i in range(segments):
        next_i = (i + 1) % segments
        bm.faces.new((top_ring[i], top_ring[next_i], bot_ring[next_i], bot_ring[i]))

    bm.faces.new(top_ring)
    bm.faces.new(list(reversed(bot_ring)))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm
