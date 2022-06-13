from logging import root
import bpy
import math
import numpy as np

from bpy.props import StringProperty, PointerProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .constants import PROPS
from .functions import get_children, get_armatures

class AD_OT_Load_Animation(Operator, ImportHelper):

    bl_idname = "object.load_animation"
    bl_label = "Load Animation"
    bl_description = "Load an animation in fbx format"

    filter_glob: StringProperty( 
        default='*.fbx', 
        options={'HIDDEN'} 
    )

    def execute(self, context):
        bpy.ops.import_scene.fbx(filepath = self.filepath)
        return { "FINISHED" }

class AD_OT_Create_Target(Operator):

    bl_idname = "object.create_target_armature"
    bl_label = "Create target"
    bl_description = "Create target armature"

    def execute(self, context):

        if not context.scene.source_armature:
            self.report({"ERROR"}, "Please select source armature")
            return {"CANCELLED"}

        armatures_list = get_armatures(self, context)
        number_of_armatures = len(armatures_list)

        if number_of_armatures < 2:
            self.report({"ERROR"}, "Need at least 1 animation to create target")
            return {"CANCELLED"}

        if number_of_armatures > 4:
            self.report({"ERROR"}, "Currently only 4 animations are supported")
            return {"CANCELLED"}

        # space armatures away from center
        r = context.scene.distance

        position_dict = {
            # line
            "2": [ 
                (-r, 0, 0), 
                (r, 0, 0)
            ],
            # triangle
            "3": [ 
                (0, -r, 0), 
                (-r, 0, 0),
                (r, 0, 0)
            ],
            # square
            "4": [
                (0, -r, 0), 
                (-r, 0, 0), 
                (0, r, 0),
                (r, 0, 0)
            ]
        }

        # select source armature and duplicate it
        # rename target armature
        bpy.context.active_object.select_set(False)
        context.scene.source_armature.select_set(True)
        bpy.context.view_layer.objects.active = context.scene.source_armature
        source_armature_children = get_children(self, context, context.scene.source_armature)
        for child in source_armature_children:
            child.select_set(True)
        bpy.ops.object.duplicate()
        target_armature = context.active_object
        target_armature.name = "Target Armature"

        # move armatures into position
        for i, armature in enumerate(armatures_list):

            bpy.ops.object.empty_add(
                type='PLAIN_AXES', 
                align='WORLD', 
                location=(0, 0, 0),
                scale=(1, 1, 1)
            )
            armature.parent = bpy.context.active_object

            bpy.ops.transform.translate(
                value=position_dict[str(number_of_armatures)][i], 
                orient_type='GLOBAL'
            )

        return { "FINISHED" }

class AD_OT_Calculate_Average(Operator):

    bl_idname = "object.calculate_average"
    bl_label = "Calculate Average"
    bl_description = "Calculate average animation"

    def execute(self, context):

        armatures_list = get_armatures(self, context)
        number_of_armatures = len(armatures_list)

        if number_of_armatures < 2:
            self.report({"ERROR"}, "Need at least 1 animation to calculate average")
            return {"CANCELLED"}

        if number_of_armatures > 4:
            self.report({"ERROR"}, "Currently only 4 animations are supported")
            return {"CANCELLED"}

        # remove source and target armature from armatures list
        armatures_list_filtered = []
        for armature in armatures_list:
            if not armature.name in [context.scene.source_armature.name, "Target Armature"]:
                armatures_list_filtered.append(armature)

        for armature in armatures_list_filtered:
            
            # set target armature to active
            bpy.context.active_object.select_set(False)
            target_armature = bpy.data.objects['Target Armature']
            target_armature.select_set(True)
            bpy.context.view_layer.objects.active = target_armature
            print(f"active object: {bpy.context.view_layer.objects.active}, source armature: {armature}")

            if target_armature.mode == "OBJECT":
                bpy.ops.object.posemode_toggle()

            for bone_source, bone_target in zip(armature.pose.bones, target_armature.pose.bones):
                
                if bone_source.bone.name != bone_target.bone.name:
                    self.report({"ERROR"}, "Armature bones must be identical in naming")
                    return {"CANCELLED"}

                # print(f'Source: {bone_source.bone.name}, Target: {bone_target.bone.name}')

                # add copy rotation constraint
                target_armature.data.bones.active = bone_target.bone
                bpy.ops.pose.constraint_add(type='COPY_ROTATION')
                target_armature.pose.bones[bone_target.name].constraints["Copy Rotation"].target = armature
                target_armature.pose.bones[bone_target.name].constraints["Copy Rotation"].subtarget = bone_source.name
                target_armature.pose.bones[bone_target.name].constraints["Copy Rotation"].influence = 0.33

        if context.scene.add_material:
            
            # select target armature mesh 
            bpy.context.active_object.select_set(False)
            target_armature_mesh = get_children(self, context, bpy.data.objects['Target Armature'])[0]
            target_armature_mesh.select_set(True)
            bpy.context.view_layer.objects.active = target_armature_mesh

            # create new material
            new_mat = bpy.data.materials.new(name="Average_Dancer_Material")
            new_mat.use_nodes = True
            nodes = new_mat.node_tree.nodes

            principled_bsdf = nodes.get("Principled BSDF")

            print(context.scene.material_color)
            principled_bsdf.inputs[0].default_value = color # color
            principled_bsdf.inputs[19].default_value = color # color
            principled_bsdf.inputs[20].default_value = 1.5 # strength

            # set render engine to eevee and turn on settings for aesthetics
            bpy.context.space_data.shading.type = 'MATERIAL'
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.use_bloom = True
            bpy.context.scene.eevee.use_ssr = True

            # set new material to mesh
            target_armature_mesh.data.materials.append(new_mat)

        return { "FINISHED" }



    


