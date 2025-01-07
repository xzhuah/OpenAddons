import bpy


def switch_to_modifier_context():
    for area in bpy.context.screen.areas:
        if area.type == 'PROPERTIES':
            for space in area.spaces:
                if space.type == 'PROPERTIES':
                    # Set the context to the 'MODIFIER' tab
                    space.context = 'MODIFIER'


class AddModifierAndChangePropertiesContext(bpy.types.Operator):
    bl_idname = "node_pinyin.add_modifier"
    bl_label = "Add Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.StringProperty()

    def execute(self, context):
        try:
            bpy.ops.object.modifier_add(type=self.type)
            switch_to_modifier_context()
        except Exception as e:
            bpy.ops.wm.call_menu(name=bpy.types.OBJECT_MT_modifier_add.__name__)
            self.report({'WARNING'}, "This Object Type Does Not Support This Modifier")
        return {'FINISHED'}


class AddModifierNodeGroupAndChangePropertiesContext(bpy.types.Operator):
    bl_idname = "node_pinyin.add_modifier_node_group"
    bl_label = "Add Modifier Node Group"
    bl_options = {'REGISTER', 'UNDO'}

    relative_asset_identifier: bpy.props.StringProperty()

    def execute(self, context):
        try:
            bpy.ops.object.modifier_add_node_group(asset_library_type="ESSENTIALS", asset_library_identifier="",
                                                   use_selected_objects=True,
                                                   relative_asset_identifier=self.relative_asset_identifier)
            switch_to_modifier_context()
        except Exception as e:
            bpy.ops.wm.call_menu(name=bpy.types.OBJECT_MT_modifier_add.__name__)
            self.report({'WARNING'}, "This Object Type Does Not Support This Modifier")
        return {'FINISHED'}
