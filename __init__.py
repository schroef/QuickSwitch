bl_info = {
	"name": "QuickSwitch",
	"description": "QuickSwitch is a little helper to make it easier to switch render engines",
	"location": "3D VIEW > Properties > Headus UVlayout Panel",
	"author": "Rombout Versluijs",
	"version": (0, 0, 1),
	"blender": (2, 80, 0),
	"wiki_url": "https://github.com/schroef/quickswitch",
	"tracker_url": "https://github.com/schroef/quickswitch/issues",
	"category": "Render"
}

import bpy
import rna_keymap_ui
from . config.registers import get_hotkey_entry_item

from bpy.types import (
	Panel, WindowManager, AddonPreferences, Menu
	)
from bpy.props import (
	EnumProperty, StringProperty, BoolProperty, IntProperty, FloatProperty
	)



class WM_OT_QuickSwitchEngine(Menu):
	bl_idname = "quick.switch_engine"
	bl_label = "QuickSwitch Engine"

	def draw(self, context):
		layout = self.layout
		scene = bpy.context.scene
		rd = context.scene.render

		if rd.has_multiple_engines:
			layout.prop(rd, "engine",  expand=True)

		layout.separator()

		layout.operator("render.render", text="Render Image", icon='RENDER_STILL').use_viewport = True
		props = layout.operator("render.render", text="Render Animation", icon='RENDER_ANIMATION')
		props.animation = True
		props.use_viewport = True

		layout.separator()

		layout.operator("render.view_show", text="View Render")
		layout.operator("render.play_rendered_anim", text="View Animation")
		layout.prop_menu_enum(rd, "display_mode", text="Display Mode")

		layout.separator()




#-- ADDON PREFS --#
class QS_PT_AddonPreferences(AddonPreferences):
	""" Preference Settings Addin Panel"""
	bl_idname = __name__

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		box=layout.box()
		split = box.split()
		col = split.column()
		col.label(text = "Hotkeys:")
		col.label(text = "Do NOT remove hotkeys, disable them instead!")

		wm = bpy.context.window_manager
		kc = wm.keyconfigs.user

		km = kc.keymaps['3D View']
		kmi = get_hotkey_entry_item(km, "wm.call_menu", "quick.switch_engine", "name")
		if kmi:
			col.context_pointer_set("keymap", km)
			rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
			col.label(text = "Quick export using last settings")

		else:
			col.label(text = "restore hotkeys from interface tab")


#Classes for register and unregister
classes = (
	WM_OT_QuickSwitchEngine,
	QS_PT_AddonPreferences
	)

addon_keymaps = []

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	# handle the keymap
	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon

	#km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
	km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
	kmi = km.keymap_items.new("wm.call_menu", "E", "PRESS", alt = True, shift = True)
	kmi.properties.name = "quick.switch_engine"
	kmi.active = True
	addon_keymaps.append(km)
	#km = kc.keymaps.new(name = '3D View', space_type = 'VIEW_3D')
	#kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS', alt = True, shift = True)
	#kmi.properties.name = 'quick.switch_engine'
	#kmi.active = True
	#addon_keymaps.append((km, kmi))


def unregister():
	# handle the keymap
	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
