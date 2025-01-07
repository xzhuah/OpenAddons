import itertools
import os.path

import bpy
from bl_ui import node_add_menu
from bpy.types import Context

from ..config import __addon_name__
from ..data.data import PIN_YIN_NODE_LIST, SHADER_NODE_IN_GEOMETRY, HAIR_NODES, SMOOTH_BY_ANGLE, VRAY_NODE_LIST, \
    MODIFIER_DICT, MODIFIER_OBJECT_TYPES
from ..operator.Operators import AddModifierAndChangePropertiesContext, AddModifierNodeGroupAndChangePropertiesContext
from ..preference.AddonPreferences import MenuEnhancePreferences
from ....common.types.framework import ExpandableUi


def get_swapping_dict():
    preference = bpy.context.preferences.addons[__addon_name__].preferences
    assert isinstance(preference, MenuEnhancePreferences)
    swapping_dict = {}
    if preference.fuzzy_f_h:
        swapping_dict['f'] = ['f', 'h']
        swapping_dict['h'] = ['f', 'h']
    if preference.fuzzy_n_l:
        swapping_dict['n'] = ['n', 'l']
        swapping_dict['l'] = ['n', 'l']
    if preference.fuzzy_r_l:
        swapping_dict['r'] = ['r', 'l']
        swapping_dict['l'] = ['r', 'l']
    if preference.fuzzy_n_l and preference.fuzzy_r_l:
        swapping_dict['l'] = ['n', 'l', 'r']
    return swapping_dict


def fuzzy_list(szm: str) -> list[str]:
    """根据首字母拼音返回所有可能的模糊拼音，
    如输入lx 返回['lx', 'nx']
    输入 llx 返回['llx', 'nlx', 'lnx', 'nnx']
    """
    swap_dict = get_swapping_dict()
    if len(swap_dict) == 0:
        return [szm]
    possibilities = []
    for char in szm:
        if char in swap_dict:
            possibilities.append(swap_dict[char])
        else:
            possibilities.append([char])
    result = [''.join(combination) for combination in itertools.product(*possibilities)]
    return result


def index_list(pin_ying_list: list[str], ui_name: str):
    preference = bpy.context.preferences.addons[__addon_name__].preferences
    assert isinstance(preference, MenuEnhancePreferences)
    first_char = "".join([i[0] for i in pin_ying_list])
    full = "".join(pin_ying_list)
    result = []
    if preference.first_pinyin:
        result.append(" ".join(fuzzy_list(first_char)))
    if preference.full_pinyin:
        result.append(full)
    if preference.english_name:
        result.append(ui_name)
    return " ".join(result)


def modifier_label_name(item: list):
    ui_name = item[0]
    # chinese
    chinese_name = item[1]
    # pinyin
    pin_yin = item[2]
    return combine_label_name(chinese_name, pin_yin, ui_name)


def label_name(item: tuple):
    ui_name = item[2]
    # chinese
    chinese_name = item[3]
    # pinyin
    pin_yin = item[4]
    return combine_label_name(chinese_name, pin_yin, ui_name)


def vray_label_name(item: tuple):
    ui_name = item[0]
    # chinese
    chinese_name = item[1]
    # pinyin
    pin_yin = item[2]
    return combine_label_name(chinese_name, pin_yin, ui_name)


def combine_label_name(chinese, full, english):
    preference = bpy.context.preferences.addons[__addon_name__].preferences
    assert isinstance(preference, MenuEnhancePreferences)
    return chinese + " " + index_list(full, english)


def asset_label_name(key, items):
    preference = bpy.context.preferences.addons[__addon_name__].preferences
    assert isinstance(preference, MenuEnhancePreferences)
    result = []
    if preference.first_pinyin:
        result.append("".join([i[0] for i in items[1]]))
    if preference.full_pinyin:
        result.append("".join(items[1]))
    if preference.english_name:
        result.append(key)
    return items[0] + " " + " ".join(result)


def mix_vector_label_name():
    return combine_label_name("混合矢量", ["hun", "he", "shi", "liang"], "MixVector")


def mix_color_label_name():
    return combine_label_name("混合颜色", ["hun", "he", "yan", "se"], "MixColor")


class ChineseNodeSearchMenu(bpy.types.Menu):
    """PinYin Node Search Menu"""
    bl_idname = "NODE_MT_add_enhanced"
    bl_label = "Add Node"

    def draw(self, context: Context):
        layout = self.layout
        if context.space_data.tree_type == "ShaderNodeTree":
            for item in PIN_YIN_NODE_LIST:
                if item[0] == "ShaderNode" or item[0] == "Node":
                    opname = item[0] + item[1]
                    if hasattr(bpy.types, opname):
                        node_add_menu.add_node_type(layout, opname, label=label_name(item))

            if hasattr(bpy.types, "ShaderNodeMix"):
                props = node_add_menu.add_node_type(layout, "ShaderNodeMix", label=mix_color_label_name())
                ops = props.settings.add()
                ops.name = "data_type"
                ops.value = "'RGBA'"

        elif context.space_data.tree_type == "CompositorNodeTree":
            for item in PIN_YIN_NODE_LIST:
                if item[0] == "CompositorNode" or item[0] == "Node":
                    opname = item[0] + item[1]
                    if hasattr(bpy.types, opname):
                        node_add_menu.add_node_type(layout, opname, label=label_name(item))
        elif context.space_data.tree_type == "GeometryNodeTree":
            for item in PIN_YIN_NODE_LIST:
                opname = item[0] + item[1]
                if not hasattr(bpy.types, opname):
                    continue
                # https://github.com/blender/blender/blob/c9886ca90a7ece08d5ab742c8e07459ff9d3495e/scripts/startup/bl_ui/node_add_menu_geometry.py
                # if opname == "GeometryNodeToolFaceSet" or opname == "GeometryNodeToolSetFaceSet":
                #     if not context.space_data.geometry_nodes_type == 'TOOL':
                #         continue
                # if opname == "GeometryNodeMeshToDensityGrid" or opname == "GeometryNodeMeshToPoints" or opname == "GeometryNodeDistributePointsInGrid" or opname == "GeometryNodePointsToSDFGrid":
                #     if not context.preferences.experimental.use_new_volume_nodes:
                #         continue
                if item[0] == "GeometryNode" or item[0] == "Node" or item[
                    0] == "FunctionNode" or opname in SHADER_NODE_IN_GEOMETRY:
                    node_add_menu.add_node_type(layout, opname, label=label_name(item))
            if hasattr(bpy.types, "ShaderNodeMix"):
                props = node_add_menu.add_node_type(layout, "ShaderNodeMix",
                                                    label=mix_vector_label_name())
                ops = props.settings.add()
                ops.name = "data_type"
                ops.value = "'VECTOR'"

                props = node_add_menu.add_node_type(layout, "ShaderNodeMix", label=mix_color_label_name())
                ops = props.settings.add()
                ops.name = "data_type"
                ops.value = "'RGBA'"
            if hasattr(node_add_menu, "add_simulation_zone"):
                node_add_menu.add_simulation_zone(layout, label=combine_label_name("模拟", ["mo", "ni"], "Simulation"))

            if hasattr(node_add_menu, "add_foreach_geometry_element_zone"):
                node_add_menu.add_foreach_geometry_element_zone(layout, label=combine_label_name("遍历元素",
                                                                                                 ["bian", "li", "yuan",
                                                                                                  "su"],
                                                                                                 "For Each Element"))

            if hasattr(node_add_menu, "add_repeat_zone"):
                node_add_menu.add_repeat_zone(layout, label=combine_label_name("重复", ["chong", "fu"], "Repeat"))

            if hasattr(node_add_menu, "draw_root_assets"):
                layout.operator_context = "INVOKE_DEFAULT"
                for key in HAIR_NODES:
                    ops = layout.operator("node.add_group_asset", text=asset_label_name(key, HAIR_NODES[key]))
                    ops.asset_library_type = 'ESSENTIALS'
                    ops.asset_library_identifier = ""

                    ops.relative_asset_identifier = os.path.join("geometry_nodes", "procedural_hair_node_assets.blend",
                                                                 "NodeTree", key)

                for key in SMOOTH_BY_ANGLE:
                    ops = layout.operator("node.add_group_asset", text=asset_label_name(key, SMOOTH_BY_ANGLE[key]))
                    ops.asset_library_type = 'ESSENTIALS'
                    ops.asset_library_identifier = ""
                    ops.relative_asset_identifier = os.path.join("geometry_nodes", "smooth_by_angle.blend",
                                                                 "NodeTree", key)

        elif context.space_data.tree_type == "TextureNodeTree":
            for item in PIN_YIN_NODE_LIST:
                if item[0] == "TextureNode" or item[0] == "Node":
                    opname = item[0] + item[1]
                    if hasattr(bpy.types, opname):
                        node_add_menu.add_node_type(layout, opname, label=label_name(item))

        elif context.space_data.tree_type == "VRayNodeTreeEditor":
            for key in VRAY_NODE_LIST:
                node_add_menu.add_node_type(layout, key, label=vray_label_name(VRAY_NODE_LIST[key]))


class ChineseModifierSearchMenu(bpy.types.Menu):
    """PinYin Modifier Search Menu"""
    bl_idname = "OBJECT_MT_modifier_add_enhanced"
    bl_label = "Modifiers"

    @classmethod
    def operator_modifier_add(cls, layout, mod_type):
        layout.operator(
            # "object.modifier_add",
            AddModifierAndChangePropertiesContext.bl_idname,
            text=modifier_label_name(MODIFIER_DICT[mod_type]),
            # # Although these are operators, the label actually comes from an (enum) property,
            # # so the property's translation context must be used here.
            # text_ctxt=bpy.types.Modifier.bl_rna.properties["type"].translation_context
        ).type = mod_type

    def draw(self, context: Context):
        layout = self.layout
        active_object = bpy.context.active_object
        if active_object and len(context.selected_objects) > 0:
            if active_object.type in MODIFIER_OBJECT_TYPES:
                for mod_type in MODIFIER_DICT:
                    if mod_type.startswith("GREASE_PENCIL") and active_object.type != 'GREASEPENCIL':
                        continue
                    try:
                        self.operator_modifier_add(layout, mod_type)
                    except Exception as e:
                        # some modifiers are not available for some object types
                        # use try-except to skip them
                        pass
            if active_object.type == 'MESH':
                # add fur modifier
                for key in HAIR_NODES:
                    ops = layout.operator(AddModifierNodeGroupAndChangePropertiesContext.bl_idname,
                                          text=asset_label_name(key, HAIR_NODES[key]))
                    ops.relative_asset_identifier = os.path.join("geometry_nodes", "procedural_hair_node_assets.blend",
                                                                 "NodeTree", key)


class MenuToExpand(ExpandableUi):
    target_id = bpy.types.NODE_MT_add.__name__

    def draw(self, context: bpy.types.Context):
        self.layout.menu(ChineseNodeSearchMenu.bl_idname, text="Enhanced Search")


class ModifierMenuToExpand(ExpandableUi):
    target_id = bpy.types.OBJECT_MT_modifier_add.__name__

    def draw(self, context: bpy.types.Context):
        preference = bpy.context.preferences.addons[__addon_name__].preferences
        assert isinstance(preference, MenuEnhancePreferences)
        if preference.enable_modifiers_search:
            self.layout.menu(ChineseModifierSearchMenu.bl_idname, text="Enhanced Search")


# class ModifierMenuSearchToExpand(ExpandableUi):
#     target_id = bpy.types.OBJECT_MT_modifier_add.__name__
#     expand_mode = "PREPEND"
#
#     def draw(self, context: bpy.types.Context):
#         self.layout.operator("WM_OT_search_single_menu", text="Search...",
#                              icon='VIEWZOOM').menu_idname = "OBJECT_MT_modifier_add"


class ModifierMenuForEditorToExpand(ExpandableUi):
    target_id = bpy.types.VIEW3D_MT_editor_menus.__name__

    def draw(self, context: bpy.types.Context):
        preference = bpy.context.preferences.addons[__addon_name__].preferences
        assert isinstance(preference, MenuEnhancePreferences)
        if preference.enable_modifiers_search and context.edit_object and context.active_object.type in MODIFIER_OBJECT_TYPES:
            self.layout.menu(bpy.types.OBJECT_MT_modifier_add.__name__)

# class VIEW_3D_EDITOR_MENU_Search(ExpandableUi):
#     target_id = bpy.types.VIEW3D_MT_editor_menus.__name__
#     expand_mode = "PREPEND"
#
#     def draw(self, context: bpy.types.Context):
#         self.layout.operator("WM_OT_search_single_menu", text="Search...",
#                              icon='VIEWZOOM').menu_idname = "OBJECT_MT_modifier_add"
