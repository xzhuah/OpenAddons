import bpy

from common.class_loader import auto_load
from .config import __addon_name__
from .i18n.dictionary import dictionary
from .preference.AddonPreferences import MenuEnhancePreferences
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

# Add-on info
bl_info = {
    "name": "szm/首字母",
    "author": "Xinyu Zhu(异次元学者)",
    "blender": (4, 0, 0),
    "version": (1, 1, 0),
    "description": "Enable node and modifier search with PinYin/支持节点和修改器中英文拼音搜索",
    "doc_url": "https://github.com/xzhuah/OpenAddons/tree/master/addons/node_pinyin",
    "tracker_url": "https://github.com/xzhuah/OpenAddons/issues",
    "support": "COMMUNITY",
    "category": "Node"
}


def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)
    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    auto_load.unregister()
    print("{} addon is uninstalled.".format(__addon_name__))
