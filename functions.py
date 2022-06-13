import bpy

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

# def add_material(self, context):
#     '''add material to target armature'''
#     # select target armature mesh 
#     bpy.context.active_object.select_set(False)
#     target_armature_mesh = get_children(context, armature_target)[0]
#     bpy.context.view_layer.objects.active = target_armature_mesh

#     # create new material
#     new_mat = bpy.data.materials.new(name="Average_Dancer_Material")
#     new_mat.use_nodes = True
#     nodes = new_mat.node_tree.nodes

#     principled_bsdf = nodes.get("Principled BSDF")

#     cyan = (0, 0.8, 1, 1)
#     principled_bsdf.inputs[0].default_value = cyan # color
#     principled_bsdf.inputs[19].default_value = cyan # color
#     principled_bsdf.inputs[20].default_value = 1.5 # strength

#     # set render engine to eevee and turn on settings for aesthetics
#     bpy.context.space_data.shading.type = 'MATERIAL'
#     bpy.context.scene.render.engine = 'BLENDER_EEVEE'
#     bpy.context.scene.eevee.use_bloom = True
#     bpy.context.scene.eevee.use_ssr = True

#     # set new material to mesh
#     target_armature_mesh.data.materials.append(new_mat)