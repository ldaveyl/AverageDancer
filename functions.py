import bpy
import re

def armature_poll(self, object):
    return object.type == 'ARMATURE'

def get_children(self, context, my_object):
    '''make list of all children of object'''
    children = []
    for ob in bpy.data.objects: 
        if ob.parent == my_object: 
            children.append(ob) 
    return children

def get_armatures(self, context):
    '''make list of all armatures in scene'''
    armatures_list = []
    objects = bpy.context.scene.objects
    for obj in objects: 
        if obj.type == "ARMATURE":
            armatures_list.append(obj)
    return armatures_list

def add_material(self, context):

    if context.scene.add_material:

        # select target armature mesh 
        bpy.context.active_object.select_set(False)
        target_armature_mesh = get_children(self, context, bpy.data.objects['Target Armature'])[0]
        target_armature_mesh.select_set(True)
        bpy.context.view_layer.objects.active = target_armature_mesh

        # if there is no active material, create a new material
        if not target_armature_mesh.active_material:
            mat = bpy.data.materials.new(name="Average_Dancer_Material")
            target_armature_mesh.data.materials.append(mat)
        elif not re.search("Average_Dancer_Material", target_armature_mesh.active_material.name):
            mat = bpy.data.materials.new(name="Average_Dancer_Material")
            target_armature_mesh.data.materials.append(mat)
        else:
            mat = target_armature_mesh.active_material

        mat.use_nodes = True
        nodes = mat.node_tree.nodes
 
        principled_bsdf = nodes.get("Principled BSDF")

        # set color of principled bsdf
        color = [c for c in context.scene.material_color] + [0]
        principled_bsdf.inputs[0].default_value = color
        principled_bsdf.inputs[19].default_value = color
        principled_bsdf.inputs[20].default_value = 1.5 # strength

        # set render engine to eevee and turn on settings for aesthetics
        bpy.context.space_data.shading.type = 'MATERIAL'
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.use_ssr = True