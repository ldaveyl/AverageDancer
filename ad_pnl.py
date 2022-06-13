import bpy

from bpy.types import Panel

from .constants import PROPS

class AD_PT_Panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Average Dancer"
    bl_category = "Average Dancer"

class AD_PT_Panel_Load_Animation(AD_PT_Panel, Panel):
    bl_idname = "AD_PT_Panel_Load_Animation"
    bl_label = "Average Dancer"

    def draw(self, context):

        layout = self.layout

        row = layout.row()

        col = row.column()
        col.operator("object.load_animation", text="Load Animation", icon="FILE")

class AD_PT_Panel_Create_Target(AD_PT_Panel, Panel):
    bl_parent_id = "AD_PT_Panel_Load_Animation"
    bl_label = "Create Target Armature"

    def draw(self, context):

        layout = self.layout

        row = layout.row()

        col = row.column()
        row.prop(context.scene, "distance")
        col.operator("object.create_target_armature", text="Create Target", icon="PIVOT_CURSOR")
        col.prop_search(context.scene, "source_armature", context.scene, "objects", icon='OBJECT_DATA')

class AD_PT_Panel_Calculate_Average(AD_PT_Panel, Panel):
    bl_parent_id = "AD_PT_Panel_Load_Animation"
    bl_label = "Calculate Average"

    def draw(self, context):

        layout = self.layout

        row = layout.row()

        col = row.column()
        row.prop(context.scene, "add_material")
        row.prop(context.scene, "material_color")
        col.operator("object.calculate_average", text="Average", icon="ARMATURE_DATA")
