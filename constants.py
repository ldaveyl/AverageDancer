import bpy

from bpy.props import IntProperty, BoolProperty, FloatVectorProperty, StringProperty, PointerProperty
from .functions import armature_poll, add_material

PROPS = [
    ('distance', IntProperty(name='Distance', default=2, min=1, max=10)),
    ('add_material', BoolProperty(name='Material', default=False)),
    ('source_armature', PointerProperty(name='Source', type=bpy.types.Object, poll=armature_poll)),
    ('material_color', FloatVectorProperty(name="", subtype="COLOR", default=[0.0, 0.8, 1.0], update=add_material))
]