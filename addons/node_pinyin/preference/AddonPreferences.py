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
        default=True,
    )

    fuzzy_n_l: BoolProperty(
        name="n=l",
        default=False,
    )

    fuzzy_f_h: BoolProperty(
        name="f=h",
        default=False,
    )

    fuzzy_r_l: BoolProperty(
        name="r=l",
        default=False,
    )

    enable_modifiers_search: BoolProperty(
        name="Enable Search For Modifiers",
        default=True,
    )

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.label(text="Index Settings")
        row = layout.row()
        row.prop(self, "first_pinyin", text="First Letter")
        row.prop(self, "english_name", text="English Name")
        row.prop(self, "full_pinyin", text="Full Spelling")
        layout.label(text="Phonetic Confusion Setting For First Letter")
        row = layout.row()
        row.prop(self, "fuzzy_n_l", text="n=l")
        row.prop(self, "fuzzy_f_h", text="f=h")
        row.prop(self, "fuzzy_r_l", text="r=l")
        layout.label(text="Search Settings")
        row = layout.row()
        row.prop(self, "enable_modifiers_search", text="Enable Search For Modifiers")


