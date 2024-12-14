import bpy

from .config import __addon_name__
from .i18n.dictionary import dictionary
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties, remove_addon_cache
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

# Add-on info
bl_info = {
    "name": "szm/首字母",
    "author": "Xinyu Zhu(异次元学者)",
    "blender": (4, 0, 0),
    "version": (0, 0, 1),
    "description": "Enable node search with PinYin/支持节点中文拼音搜索",
    "doc_url": "",
    "tracker_url": "xzhuah77@gmail.com",
    "support": "COMMUNITY",
    "category": "Node"
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

def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)

    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    auto_load.unregister()
    remove_properties(_addon_properties)
    remove_addon_cache(__addon_name__)
    print("{} addon is uninstalled.".format(__addon_name__))
