import bpy
from bpy.props import BoolProperty
from bpy.types import AddonPreferences

from ..config import __addon_name__


class MenuEnhancePreferences(AddonPreferences):
    # this must match the add-on name (the folder name of the unzipped file)
    bl_idname = __addon_name__

    # https://docs.blender.org/api/current/bpy.props.html
    # The name can't be dynamically translated during blender programming running as they are defined
    # when the class is registered, i.e. we need to restart blender for the property name to be correctly translated.
    first_pinyin: BoolProperty(
        name="first",
        default=True,
    )

    full_pinyin: BoolProperty(
        name="full",
        default=False,
    )

    english_name: BoolProperty(
        name="english",
        default=False,
    )

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.label(text="Search Settings")
        row = layout.row()
        row.prop(self, "first_pinyin", text="First Letter")
        row.prop(self, "full_pinyin", text="Full Spelling")
        row.prop(self, "english_name", text="English Name")
