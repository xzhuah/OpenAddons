import bpy
from pypinyin import pinyin, Style
from .config import __addon_name__
import re
# Add-on info
bl_info = {
    "name": "Basic Add-on Sample",
    "author": "[You name]",
    "blender": (3, 5, 0),
    "version": (0, 0, 1),
    "description": "This is a template for building addons",
    "warning": "",
    "doc_url": "[documentation url]",
    "tracker_url": "[contact email]",
    "support": "COMMUNITY",
    "category": "3D View"
}

_addon_properties = {}


# You may declare properties like following, framework will automatically add and remove them.
# Do not define your own property group class in the __init__.py file. Define it in a separate file and import it here.
# 注意不要在__init__.py文件中自定义PropertyGroup类。请在单独的文件中定义它们并在此处导入。
# _addon_properties = {
#     bpy.types.Scene: {
#         "property_name": bpy.props.StringProperty(name="property_name"),
#     },
# }

def format_dict(dict_data: dict):
    for key, value in dict_data.items():
        print(f"\"{key}\" :[\"{value[0]}\", \"{value[1]}\", {value[2]}],")


def register():
    # Register classes
    MODIFIER_TYPES_TO_LABELS = {
        enum_it.identifier: enum_it.name
        for enum_it in bpy.types.Modifier.bl_rna.properties["type"].enum_items_static
    }
    # print(MODIFIER_TYPES_TO_LABELS)
    translate_context = bpy.types.Modifier.bl_rna.properties["type"].translation_context
    data_map = {}
    for name, value in MODIFIER_TYPES_TO_LABELS.items():
        pinyin_list = []
        chinese_labels = bpy.app.translations.pgettext(value, translate_context)

        for char in chinese_labels:
            if re.match(r'[a-zA-Z]', char):  # 如果是字母
                pinyin_list.append(char.lower())  # 英文字符转小写并添加到列表
            elif re.match(r'[\u4e00-\u9fff]', char):  # 如果是汉字
                the_list = pinyin(char, style=Style.NORMAL)
                pinyin_list.append(the_list[0][0])  # 汉字转拼音并添加到列表

        labels = [value, bpy.app.translations.pgettext(value, translate_context), pinyin_list]
        data_map[name] = labels
    format_dict(data_map)

    pass


def unregister():
    # Internationalization
    pass
