"""
.. module:: Switches to the Workspace of the given name
   :platform: OS X, Windows, Linux
   :synopsis: —

.. moduleauthor:: Original code by Blitzen


"""
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


#######################################################

## QuickSwitch Workspaces (Prior ScreenLayouts)	######
##
## 21-12-18 - Got 2.80 working
## 21-12-18 - Addd pie menu option
## 22-12-18 - Update user_preferences > preferences
## 			- Renamed all Screen items > workspace
##			- Updated unreg keymaps
##			- Added option to adjust pie positions according to popup menu
##			- Merge QuickSwitch into this one

## QuickSwitch Render Engine	######
##
## 20-12-18	- updated preferences to preferences
## 22-12-18 - Merge QuickSwitch into this one
##

## QuickSwitch Merged
##
## v0.0.3
## Changed
## 22-12-18 - Added order for WM menu

## v.0.0.3
## Changed
## 23-12-18 - General icons to workspace icons

#######################################################

bl_info = {
	"name": "QuickSwitch",
	"description": "QuickSwitch is a little helper to make it easier to switch render engines & workspaces",
	"location": "3D VIEW > Quick Switch",
	"author": "Rombout Versluijs",
	"version": (0, 0, 3),
	"blender": (2, 80, 0),
	"wiki_url": "https://github.com/schroef/quickswitch",
	"tracker_url": "https://github.com/schroef/quickswitch/issues",
	"category": "Viewport"
}

import bpy
import rna_keymap_ui
from bl_operators.presets import AddPresetBase, PresetMenu
#from . import AddPresetBase

from bpy.types import (
	Panel, WindowManager, AddonPreferences, Menu, Operator
	)
from bpy.props import (
	EnumProperty, StringProperty, BoolProperty, IntProperty, FloatProperty
	)

def avail_workspaces(self,context):
	'''
	enumerates available Workspaces and adding more items:
	Maximize Area - will toggle current area to maximum window size
	User Preferences - opens User Preferences window
	'''

	screen = bpy.data.workspaces
	screens = [ ("Preferences", "Preferences", "Preferences")]
			# (identifier, name, description) optionally: (.., icon name, unique number)

	for screen in bpy.data.workspaces:
		screens.append((screen.name, screen.name, screen.name))
	return screens


addon_keymaps = []

def add_hotkey():
	preferences = bpy.context.preferences
	addon_prefs = preferences.addons[__name__].preferences

	wm = bpy.context.window_manager

	kc = wm.keyconfigs.addon    # for hotkeys within an addon
	km = kc.keymaps.new(name = "Screen", space_type = "EMPTY")
	hKeys = [("NUMPAD_1"), ("NUMPAD_2"), ("NUMPAD_3"), ("NUMPAD_4"),("NUMPAD_5"),("NUMPAD_6"),("NUMPAD_7"),("NUMPAD_8"),("NUMPAD_9"),("NUMPAD_0")]
	i=0
	for screen in hKeys:
		kmi = km.keymap_items.new("workspace.set_layout", hKeys[i], "PRESS", oskey=True)  # ...and if not found then add it
		kmi.properties.layoutName = "WorkspaceSwitcher"+str(i)  # also set proper name
		kmi.active = True
		addon_keymaps.append((km, kmi)) # also append to global (addon level) hotkey list for easy management
		i+=1

	#Add quick menu
	kmi = km.keymap_items.new("wm.call_menu",  value='PRESS', type='W', ctrl=False, alt=True, shift=False, oskey=False)
	kmi.properties.name = "workspace.switch_menu"
	kmi.active = True
	addon_keymaps.append((km, kmi))

	#Add quick pie menu
	kmi = km.keymap_items.new("wm.call_menu_pie",  value='PRESS', type='W', ctrl=False, alt=True, shift=True, oskey=False)
	kmi.properties.name = "workspace.switch_pie_menu"
	kmi.active = True
	addon_keymaps.append((km, kmi))


	#Add QS Render Engine
	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
	kmi = km.keymap_items.new("wm.call_menu", value='PRESS', type='E', alt=True, shift=True)
	kmi.properties.name = "quick.switch_engine"
	kmi.active = True
	addon_keymaps.append((km, kmi))


class AddPresetQuickSwitch(AddPresetBase, Operator):
	"""Add or remove a QuickSwitch Preset"""
	bl_idname = "qs.preset_add"
	bl_label = "Add QuickSwitch Preset"
	preset_menu = "QS_PT_presets"

	preset_defines = [
		"qs = bpy.context.cloth"
	]

	preset_values = [
		"qs.",
		"qs.",
		"qs.",
		"qs.",
		"qs.",
		"qs.",
	]

	preset_subdir = "quickswitch"


class QS_PT_presets(PresetMenu):
	bl_label = "QuickSwitch Presets"
	preset_subdir = "quickswitch"
	preset_operator = "script.execute_preset"
	draw = Menu.draw_preset

#class RIGIFY_MT_SettingsPresetMenu(Menu):
#    bl_label = "Setting Presets"
#    preset_subdir = "rigify"
#    preset_operator = "script.execute_preset"
#    draw = Menu.draw_preset


class QS_OT_QuickSwitchEngine(Menu):
	bl_idname = "quick.switch_engine"
	bl_label = "Render"

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

		#layout.operator("render.view_show", text="View Render")
		layout.operator("render.view_show", text="View Render")
		layout.operator("render.play_rendered_anim", text="View Animation")
		layout.prop_menu_enum(rd, "display_mode", text="Display Mode")

		layout.separator()


def get_hotkey_entry_item(km, kmi_name, kmi_value):
	'''
	returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
	if there are multiple hotkeys!)
	'''
	for i, km_item in enumerate(km.keymap_items):
		if km.keymap_items.keys()[i] == kmi_name:
			try:
				if km.keymap_items[i].properties.name == kmi_value:
					return km_item
			except:
				pass
			try:
				if km.keymap_items[i].properties.layoutName == kmi_value:
					return km_item
			except:
				pass
	return None # not needed, since no return means None, but keeping for readability


class QS_MT_WorkspaceSwitchPieMenu(Menu):
	bl_label = "Workspaces"
	bl_idname = "workspace.switch_pie_menu"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()

		wm = bpy.context.window_manager
		kc = wm.keyconfigs.user
		km = kc.keymaps['Screen']

		icons = [('Layout','VIEW3D'),('Modeling','VIEW3D'),('Sculpting','SCULPTMODE_HLT'),('UV Editing','GROUP_UVS'),('Texture Paint','IMAGE'),('Shading','SHADING_RENDERED'),('Animation','RENDER_ANIMATION'),('Rendering','RENDER_STILL'),('Composition','NODE_COMPOSITING'),('Scripting','CONSOLE')]


		for i in range(0,8):
			kmi = get_hotkey_entry_item(km, "workspace.set_layout", "WorkspaceSwitcher"+str(i))
			if not kmi == None:
				for k in range(0,len(icons)):
					if kmi.properties.wslayoutMenu in icons[k][0]:
						icon = icons[k][1]
						break
					else:
						icon = 'PREFERENCES'
				pie.operator("workspace.set_layout", text='{}'.format(kmi.properties.wslayoutMenu),icon=icon).wslayoutMenu=kmi.properties.wslayoutMenu


class QS_MT_WorkspaceSwitchMenu(Menu):
	bl_label = "Workspaces"
	bl_idname = "workspace.switch_menu"

	def draw(self, context):
		layout = self.layout

		wm = bpy.context.window_manager
		kc = wm.keyconfigs.user
		km = kc.keymaps['Screen']

		## Alphabetical order
		#for i in range(0,len(avail_workspaces(self, context))):
		#	layout.operator("workspace.set_layout", text='{}'.format(avail_workspaces(self, context)[i][1]), icon='SEQ_SPLITVIEW').wslayoutMenu=avail_workspaces(self, context)[i][1]

		icons = [('Layout','VIEW3D'),('Modeling','VIEW3D'),('Sculpting','SCULPTMODE_HLT'),('UV Editing','GROUP_UVS'),('Texture Paint','IMAGE'),('Shading','SHADING_RENDERED'),('Animation','RENDER_ANIMATION'),('Rendering','RENDER_STILL'),('Composition','NODE_COMPOSITING'),('Scripting','CONSOLE')]

		## Custom order
		for i in range(0,len(avail_workspaces(self, context))):
			kmi = get_hotkey_entry_item(km, "workspace.set_layout", "WorkspaceSwitcher"+str(i))
			if not kmi == None:
				for k in range(0,len(icons)):
					if kmi.properties.wslayoutMenu in icons[k][0]:
						icon = icons[k][1]
						break
					else:
						icon = 'PREFERENCES'

				layout.operator("workspace.set_layout", text='{}'.format(kmi.properties.wslayoutMenu),icon=icon).wslayoutMenu=kmi.properties.wslayoutMenu
		layout.separator()


class QS_OT_SetWorkspace(Operator):
	"""Switches to the Workspace of the given name."""
	bl_idname="workspace.set_layout"
	bl_label="Switch to Workspace"

	wslayoutMenu: bpy.props.EnumProperty(name = "Workspace", items = avail_workspaces)
	layoutName: bpy.props.StringProperty()

	def execute(self,context):
		if self.wslayoutMenu == "Preferences":
			bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
			return{'FINISHED'}
		else:
			try:
				window = context.window
				bpy.context.window.workspace = bpy.data.workspaces[self.wslayoutMenu]
				return{'FINISHED'}
			except:
				# except layout doesn't exists
				self.report({'INFO'}, 'Workspace [{}] doesn\'t exist! Create it or pick another in addon settings.'.format(self.layoutName))

	def invoke(self,context,event):
		return self.execute(context)


########################################################


#-- ADDON PREFS --#
class QS_PT_AddonPreferences(AddonPreferences):
	""" Preference Settings Addin Panel"""
	bl_idname = __name__

	qsMenus: bpy.props.EnumProperty(name = "QuickSwitch Options", items = [("Workspaces","Workspaces","Workspaces"),("Render Menu","Render Menu","Render Menu")])

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		col = layout.column()

		col.label(text='Hotkeys:')
		col.label(text='Do NOT remove hotkeys, disable them instead!')

		row = layout.row()
		row.prop(self, "qsMenus", expand=True)
		#row.menu(QS_PT_presets.__name__, text=QS_PT_presets.bl_label)
		if getattr(self,"qsMenus") in ("Workspaces"):
			wm = bpy.context.window_manager
			kc = wm.keyconfigs.user
			km = kc.keymaps['Screen']

			box=layout.box()
			split = box.split()
			col = split.column()
			col.label(text='Set Menus:')
			kmi = get_hotkey_entry_item(km, "wm.call_menu", "workspace.switch_menu")
			if kmi:
				col.label(text='Quick Switch Menu:')
				col.context_pointer_set("keymap", km)
				rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
			else:
				col.label(text="restore hotkeys from interface tab")


			kmi = get_hotkey_entry_item(km, "wm.call_menu_pie", "workspace.switch_pie_menu")
			if kmi:
				col.label(text='Quick Switch Pie Menu:')
				col.context_pointer_set("keymap", km)
				rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
			else:
				col.label(text="restore hotkeys from interface tab")

			box=layout.box()
			split = box.split()
			col = split.column()
			col.label(text='Set Workspaces:')
			for i in range(0,len(avail_workspaces(self, context))):
	#			if km.keymap_items.keys()[i] == 'Switch to Workspace':
				kmi = get_hotkey_entry_item(km, "workspace.set_layout", "WorkspaceSwitcher"+str(i))
				if not kmi == None:
					if kmi:
						col.context_pointer_set("keymap", km)
						rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
					else:
						col.label(text="restore hotkeys from interface tab")
			col.label(text='Set each shortcut in the dropdown menu named "Workspace"')

		if getattr(self,"qsMenus") in ("Render Menu"):
			wm = bpy.context.window_manager
			kc = wm.keyconfigs.user
			km = kc.keymaps['3D View']
			box=layout.box()
			split = box.split()
			col = split.column()
			col.label(text='Set Render Menu:')
			kmi = get_hotkey_entry_item(km, "wm.call_menu", "quick.switch_engine")
			if kmi:
				col.context_pointer_set("keymap", km)
				rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
				col.label(text = "Quick export using last settings")

			else:
				col.label(text = "restore hotkeys from interface tab")



#Classes for register and unregister
classes = (
	AddPresetQuickSwitch,
	QS_PT_presets,
	QS_OT_QuickSwitchEngine,
	QS_MT_WorkspaceSwitchPieMenu,
	QS_MT_WorkspaceSwitchMenu,
	QS_OT_SetWorkspace,
	QS_PT_AddonPreferences,
	)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	# hotkey setup
	add_hotkey()



def unregister():
	# handle the keymap
	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
