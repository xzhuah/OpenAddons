from ....common.class_loader.auto_load import preprocess_dictionary

dictionary = {
    "zh_CN": {
        "Search Settings": "搜索设置",
        "Full Spelling": "全拼",
        "First Letter": "首字母",
        "English Name": "英文名",
        "PinYin Node Search Menu": "拼音节点搜索菜单",
        "Add Node": "添加节点",
        "Enhanced Search": "增强搜索",
    }
}

dictionary = preprocess_dictionary(dictionary)

dictionary["zh_HANS"] = dictionary["zh_CN"]
