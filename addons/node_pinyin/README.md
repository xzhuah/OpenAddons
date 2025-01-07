# SZM/首字母

## 关于

此插件由[Xinyu Zhu(异次元学者)](email:xzhuah77@gmail.com)研发，由[执念净化](https://space.bilibili.com/3546704626321613)
赞助和测试。

### 功能

SZM/首字母是一个增强了Blender原生的节点搜索功能的插件，它让用户可以通过中文拼音首字母来快速搜索节点和修改器。
它还支持通过全拼、中文、英文名来搜索节点。用户可以通过插件设置来自定义索引。

SZM/首字母同时也支持模糊音设置 n=l f=h r=l, 你可以在插件设置中启用。

### 兼容性

我们提供了适用于Blender4.2及以后版本的扩展型插件。我们也提供了适用于旧版本Blender的插件。旧版本插件也兼容Blender4.2及以后版本。

插件内置的节点字典基于Blender4.3，不包含旧版本Blender中的一些废弃节点。

插件内置了一个静态字典，不支持自定义节点组、其他特殊Blender版本或插件中的节点。我们鼓励社区通过pull request来更新字典。

对于Blender4.0及以后版本，你可以在添加节点菜单中通过中文拼音首字母来搜索节点。

对于Blender3.X，你需要在F3搜索菜单中搜索。

### 维护建议

插件内置的节点字典数据来源参考了Blender源码:[NOD_static_types.h](https://github.com/blender/blender/blob/3e9578485f50b0d437fcbacb3b66218714867313/source/blender/nodes/NOD_static_types.h)

Blender原生菜单的扩充方法参考了Blender官方启动脚本[node_add_menu_geometry.py](https://github.com/blender/blender/blob/c9886ca90a7ece08d5ab742c8e07459ff9d3495e/scripts/startup/bl_ui/node_add_menu_geometry.py)

使用Blender原生翻译获取中文名称

```python
bpy.app.translations.pgettext(english_name)

# 极少数情况下，需要指定上下文 如Frame
bpy.app.translations.pgettext(english_name, "NodeTree")
```

使用拼音库[pypinyin](https://pypi.org/project/pypinyin/)，获取中文拼音
极少数情况下需要手动纠正，比如"行列式"的拼音是hanglieshi，而不是xinglieshi
"栅格"的拼音是shange，而不是zhage
"重新"的拼音是chongxin，而不是zhongxin

Blender官方内置资产库中的节点组(毛发，平滑法向等),需要参考Blender本身的代码提示

如果你希望扩充字典，请提供字典来源，以便我们审核

## About

This addon is developed by [Xinyu Zhu(异次元学者)](email:xzhuah77@gmail.com) and is sponsored and tested
by [执念净化](https://space.bilibili.com/3546704626321613).

### Features

SZM is a Blender addon that enhance search function on the add node menu and modifier menu by supporting search
with Chinese characters' PinYin initials.

It also supports searching with Full PinYin, Chinese characters, and English name. You can customize the index via the
addon preferences.

SZM also supports optional ambiguous phonetic settings n=l f=h r=l, you can enable it in the addon preferences.

### Compatibility

We provide extension addon for Blender4.2 and later. We also provide a legacy version for older Blender versions. The
legacy version is also compatible with Blender 4.2 and later.

The internal Node dictionary is based on Blender 4.3, it does not contain some deprecated nodes in older Blender
versions.

The addon maintains a static dictionary so it does not support custom node groups, node from other Blender Builds or
addons. We encourage the community to update the dictionary via pull request.

For Blender 4.0 and later, you can search with Chinese characters' PinYin initials from the add node menu.
For Blender 3.X, you need to search in the F3 search menu.

### Maintenance Suggestion

The internal node dictionary is referenced from Blender source
code:[NOD_static_types.h](https://github.com/blender/blender/blob/3e9578485f50b0d437fcbacb3b66218714867313/source/blender/nodes/NOD_static_types.h)

The method of extending Blender native menu is referenced from Blender official startup
script[node_add_menu_geometry.py](https://github.com/blender/blender/blob/c9886ca90a7ece08d5ab742c8e07459ff9d3495e/scripts/startup/bl_ui/node_add_menu_geometry.py)

Use Blender native API to get Chinese name

```python
bpy.app.translations.pgettext(english_name)

# In rare cases(e.g. Frame), you need to specify the context
bpy.app.translations.pgettext(english_name, "NodeTree")
```

Use pinyin library[pypinyin](https://pypi.org/project/pypinyin/)，to get Chinese PinYin
In very rare cases, you may need to manually correct the PinYin, e.g. the PinYin of "行列式" is hanglieshi, not
xinglieshi
The PinYin of "栅格" is shange, not zhage
The PinYin of "重新" is chongxin, not zhongxin

For Blender official built-in node groups from internal assert library(hair, smooth normal, etc.), you need to refer to
Blender's own code hints

If you want to expand the dictionary, please provide the source of the dictionary for our review

