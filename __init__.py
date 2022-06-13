# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "AverageDancer",
    "author" : "Lucas Davey",
    "description" : "",
    "blender" : (3, 1, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from .ad_op import AD_OT_Load_Animation, AD_OT_Create_Target, AD_OT_Calculate_Average
from .ad_pnl import AD_PT_Panel, AD_PT_Panel_Load_Animation, AD_PT_Panel_Create_Target, AD_PT_Panel_Calculate_Average

from .constants import PROPS

classes = (
    AD_PT_Panel_Load_Animation,
    AD_PT_Panel_Create_Target,
    AD_PT_Panel_Calculate_Average,
    AD_OT_Load_Animation, 
    AD_OT_Create_Target,
    AD_OT_Calculate_Average
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)


