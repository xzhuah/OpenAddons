import bpy

from .config import __addon_name__
from .i18n.dictionary import dictionary
from .menu.PinYinMenu import ChineseNodeSearchMenu, expand_menu
from .preference.AddonPreferences import MenuEnhancePreferences
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

# Add-on info
bl_info = {
    "name": "szm/首字母",
    "author": "Xinyu Zhu(异次元学者)",
    "blender": (4, 0, 0),
    "version": (1, 0, 0),
    "description": "Enable node search with PinYin/支持节点中文拼音搜索",
    "doc_url": "https://github.com/xzhuah/OpenAddons/tree/master/addons/node_pinyin",
    "tracker_url": "https://github.com/xzhuah/OpenAddons/issues",
    "support": "COMMUNITY",
    "category": "Node"
}


def register():
    # Register classes
    bpy.utils.register_class(MenuEnhancePreferences)
    bpy.utils.register_class(ChineseNodeSearchMenu)
    bpy.types.NODE_MT_add.append(expand_menu)
    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    bpy.types.NODE_MT_add.remove(expand_menu)
    bpy.utils.unregister_class(ChineseNodeSearchMenu)
    bpy.utils.unregister_class(MenuEnhancePreferences)
    print("{} addon is uninstalled.".format(__addon_name__))
