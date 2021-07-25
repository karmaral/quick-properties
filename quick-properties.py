import bpy

bl_info = {
    "name": "Quick Properties",
    "description": "Quickly switch between the property tabs",
    "author": "Amaral Krichman",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Property Editor",
    "warning": "",
    "wiki_url": "",
    "category": "Interface",
}

class QUICKPROPS_OT_switch_tab(bpy.types.Operator):
    '''Switch Property Tab'''
    bl_idname = "quickprops.switch_tab"
    bl_label = "Switch to Tab"
    bl_options = {'REGISTER', 'INTERNAL'}

    tab_type: bpy.props.EnumProperty(items=[
                                    ('TOOL', "Tool", "", "TOOL_SETTINGS", 0),
                                    ('RENDER', "Render", "", "SCENE", 1),
                                    ('OUTPUT', "Output", "", "OUTPUT", 2),
                                    ('VIEW_LAYER', "View Layer", "", "RENDERLAYERS", 3),
                                    ('SCENE', "Scene", "", "SCENE_DATA", 4),
                                    ('WORLD', "World", "", "WORLD", 5),
                                    ('OBJECT', "Object", "", "OBJECT_DATA", 6),
                                    ('MODIFIER', "Modifier", "", "MODIFIER", 7),
                                    ('PARTICLES', "Particle", "", "PARTICLES", 8),
                                    ('PHYSICS', "Physics", "", "PHYSICS", 9),
                                    ('CONSTRAINT', "Object Constraint", "", "CONSTRAINT", 10),
                                    ('DATA', "Object Data", "", "MESH_DATA", 11),
                                    ('MATERIAL', "Material", "", "MATERIAL_DATA", 12),
                                    ('TEXTURE', "Texture", "", "TEXTURE", 13)],
                                    name="Property Tab", default='OBJECT')
    
    @classmethod
    def poll(cls, context):
        return context.area.type in {'PROPERTIES'}

    def invoke(self, context, _event):
        selected_tab = self.tab_type

        try:
            context.space_data.context = selected_tab
        except:
            self.report({'INFO'}, f"Selected object does not have {selected_tab} as a property.")
        return {'FINISHED'}


class QUICKPROPS_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        # Thanks to Bookyakuno for this solution, this feature had me pinned for ages!
        import rna_keymap_ui
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label(text="Keymap List:", icon="KEYINGSET")

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        old_km_name = ""
        get_kmi_l = []
        for (km_add, kmi_add) in addon_keymaps:
            for km_con in kc.keymaps:
                if km_add.name == km_con.name:
                    km = km_con
                    break

            for kmi_con in km.keymap_items:
                if kmi_add.idname == kmi_con.idname:
                    if kmi_add.name == kmi_con.name:
                        get_kmi_l.append((km, kmi_con))

        get_kmi_l = sorted(set(get_kmi_l), key=get_kmi_l.index)

        for (km, kmi) in get_kmi_l:
            if not km.name == old_km_name:
                col.label(text=str(km.name), icon="DOT")
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            col.separator()
            old_km_name = km.name


# --------------------- Registration ---------------------

addon_keymaps = []
classes = (QUICKPROPS_OT_switch_tab, QUICKPROPS_Preferences)

def register():

    for c in classes:
        bpy.utils.register_class(c)

    addon_keymaps.clear()

    idname = QUICKPROPS_OT_switch_tab.bl_idname
    wm = bpy.context.window_manager
    addon_keyconfig = wm.keyconfigs.addon

    kc = addon_keyconfig
    km = kc.keymaps.new(name='Property Editor', space_type='PROPERTIES')

    kmi = km.keymap_items.new(idname, 'TAB', 'PRESS', shift=True)
    kmi.properties.tab_type = 'TOOL'
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new(idname, 'FOUR', 'PRESS', shift=True)
    kmi.properties.tab_type = 'MATERIAL'
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new(idname, 'THREE', 'PRESS', shift=True)
    kmi.properties.tab_type = 'MODIFIER'
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new(idname, 'TWO', 'PRESS', shift=True)
    kmi.properties.tab_type = 'DATA'
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new(idname, 'ONE', 'PRESS', shift=True)
    kmi.properties.tab_type = 'OBJECT'
    addon_keymaps.append((km, kmi))


def unregister():

    for (km, kmi) in addon_keymaps:
        km.keymap_items.remove(kmi)

    for c in classes:
        bpy.utils.unregister_class(c)
