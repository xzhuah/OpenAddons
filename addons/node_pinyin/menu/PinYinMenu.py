import os.path

import bpy
from bl_ui import node_add_menu
from bpy.types import Context

from ..config import __addon_name__
from ..data.data import PIN_YIN_NODE_LIST, SHADER_NODE_IN_GEOMETRY, HAIR_NODES, SMOOTH_BY_ANGLE
from ..preference.AddonPreferences import MenuEnhancePreferences


def index_list(pin_ying_list: list[str], ui_name: str):
    preference = bpy.context.preferences.addons[__addon_name__].preferences
    assert isinstance(preference, MenuEnhancePreferences)
    first_char = "".join([i[0] for i in pin_ying_list])
    full = "".join(pin_ying_list)
    result = []
    if preference.first_pinyin:
        result.append(first_char)
    if preference.full_pinyin:
        result.append(full)
    if preference.english_name:
        result.append(ui_name)
    return " ".join(result)


def label_name(item: tuple):
    ui_name = item[2]
    # chinese
    chinese_name = item[3]
    # pinyin
    pin_yin = item[4]
    return chinese_name + " " + index_list(pin_yin, ui_name)


def special_label_name(chinese, first, full, english):
    preference = bpy.context.preferences.addons[__addon_name__].preferences
    assert isinstance(preference, MenuEnhancePreferences)
    result = []
    if preference.first_pinyin:
        result.append(first)
    if preference.full_pinyin:
        result.append(full)
    if preference.english_name:
        result.append(english)
    return chinese + " " + " ".join(result)


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
    return special_label_name("混合矢量", "hhsl", "hunheshiliang", "MixVector")


def mix_color_label_name():
    return special_label_name("混合颜色", "hhys", "hunheyanse", "MixColor")


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
                node_add_menu.add_simulation_zone(layout, label=special_label_name("模拟", "mn", "moni", "Simulation"))

            if hasattr(node_add_menu, "add_foreach_geometry_element_zone"):
                node_add_menu.add_foreach_geometry_element_zone(layout, label=special_label_name("遍历元素", "blyy",
                                                                                                 "bianliyuansu",
                                                                                                 "For Each Element"))

            if hasattr(node_add_menu, "add_repeat_zone"):
                node_add_menu.add_repeat_zone(layout, label=special_label_name("重复", "cf", "chongfu", "Repeat"))

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
                                                                 "NodeTree" + key)

        elif context.space_data.tree_type == "TextureNodeTree":
            for item in PIN_YIN_NODE_LIST:
                if item[0] == "TextureNode" or item[0] == "Node":
                    opname = item[0] + item[1]
                    if hasattr(bpy.types, opname):
                        node_add_menu.add_node_type(layout, opname, label=label_name(item))


def expand_menu(self, context):
    layout = self.layout
    layout: bpy.types.UILayout
    # layout.
    layout.menu(ChineseNodeSearchMenu.bl_idname, text="Enhanced Search")
