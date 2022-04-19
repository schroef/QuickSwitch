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
## 			- Fixed typo in icons

## v.0.0.4
## Changed
## 23-12-18 - Quick render now visible in all screens

## v.0.0.5
## Added
## 25-12-18 - Keep Mode stores last Object Interaction Mode and falls back to this instead of Default Workspace Object Interaction Mode

## v.0.0.6
## Changed
## 26-12-18 - Fixed basic Workspace modes, using PropertyGroup & PointerProperty to store defaults

## v.0.0.7
## Changed
## 10-01-19 - Fixed typo in workspace Texture Paint > was TEXTURE_PAINTING

## v.0.0.8
## Fixed
## 13-02-19 - Issue with quick render menu. Now render window will show like as dropdown menu (mentioned by Jacques Lucke)

## v0.0.9
## 2019-08-21
### Fixed
## - Method how menu class is import
## - Added proper Prefix & Suffix to menu classes
## - Some keymaps not show in Preference panel
## - Clearing keymaps

## v0.1.0
## 2019-08-28
### Added
## - Viewport render & render animation to render menu

## v0.1.1
## 2019-09-10
### Added
## - Display Log Info (is missing in UI)

## v0.1.2
## 2019-09-11
### Added
## - 3D_view save location

## v0.1.3
## 2019-11-11
### Added
## - Sync View Settings

## v0.1.4
## 2019-12-20
### Added
## - Save preset

## v0.1.5
## 2020-01-15
### Fixed
## - Viewport render animation operator was missing part

## v0.1.6
## 2020-03-11
### Fixed
## - Render Display changed named
##
### Changed
## - Moved Render in to render section

## v0.1.7
## 2020-03-17
### Fixed
## - Space in enumproperty

## v0.1.8
## 2020-03-20
### Fixed
## - Warning error Panel class

## v0.1.9
## 2021-02-26
### Added
## - Show console (Windows)
## - Viewport Render Frames

## v0.1.9
## 2021-03-05
### Added
## - Operator to go to file location > missing since old blender
## 

## v0.2.0
## 2021-08-05
### Fixed
## - Menu operator for console > hode for OSX
## 

## v0.2.1
## 2022-01-20
### Fixed
## - Store view after looking at MACHIN3 method. I was close > Set store view as a default
## - If workspace are not in default names, revert to a default name and interaction mode > needs work for keymaps

## v0.2.2
## 2022-01-21
### Changed
## - WIP try to storre workspaces using ID, workspace is saved by alphabetical list. Causes issue on name change
##   ^ Try to save names workspaces, issue is still present when name is changed. Workspaces dont have any info order  

"""

	TODO
	- When adjusting workarea name, replace stored item with new item name
	^ We need to store the screenspace(orden in order so we can easily check them), run a check if false replace with new name
	- Expand to order workflows: greasepencil, see other starting templates
"""
#######################################################

bl_info = {
	"name": "QuickSwitch",
	"description": "QuickSwitch is a little helper to make it easier to switch render engines & workspaces",
	"location": "3D VIEW > Quick Switch (see hotkeys)",
	"author": "Rombout Versluijs",
	"version": (0, 2, 2),
	"blender": (2, 80, 0),
	"wiki_url": "https://github.com/schroef/quickswitch",
	"tracker_url": "https://github.com/schroef/quickswitch/issues",
	"category": "Viewport"
}

import bpy, sys, os, subprocess
import rna_keymap_ui
from sys import platform
from bpy.app.handlers import persistent
from bpy_extras.io_utils import ImportHelper
# from bl_operators.presets import AddPresetBase, PresetMenu
# from . import AddPresetBase

from bpy.types import (
	Panel, WindowManager, AddonPreferences, Menu, Operator, Scene, PropertyGroup
	)
from bpy.props import (
	EnumProperty, StringProperty, BoolProperty, IntProperty, PointerProperty, FloatProperty, FloatVectorProperty
	)


def get_names_workspaces(self,context):
	'''
	enumerates available Workspaces and adding more items:
	store it using id
	https://blender.stackexchange.com/questions/78133/dynamic-enumproperty-values-changing-unexpectedly
	'''
	ws = bpy.data.workspaces
	items_store = []
	wsNames = []
	wsNames.append(("Preferences","Preferences","Preferences", 0))
	#Scan the list of IDs to see if we already have one for this mesh
	maxid = -1
	id = -1
	found = False
	for ws in bpy.data.workspaces:
		for idrec in items_store:
			# print("idrec %s - %s" % (idrec[0],idrec[1]))
			id = idrec[0]
			if id > maxid:
				maxid = id
			if idrec[1] == ws.name:
				found = True
				break
		if not found:
			items_store.append((maxid+1, ws.name,ws.name))
		# AMENDED CODE - include the ID	
		# print("ws %s - %s" % (ws.name, id))
		wsNames.append( (ws.name, ws.name, ws.name, id) )
	# print(wsNames)
	return wsNames

	
	# wsNames = [ ("Preferences", "Preferences", "", 0)]
	# 		# (identifier, name, description) optionally: (.., icon name, unique number)

	# i = 1
	# for ws in bpy.data.workspaces:
	# 	wsNames.append((ws.name, ws.name, "", i))
	# 	i+=1
	# return wsNames

# def get_names_workspaces(self,context):
# 	'''
# 	enumerates available Workspaces and adding more items:
# 	Maximize Area - will toggle current area to maximum window size
# 	User Preferences - opens User Preferences window
# 	'''

# 	ws = bpy.data.workspaces
# 	wsNames = [ ("Preferences", "Preferences", "", 0)]
# 			# (identifier, name, description) optionally: (.., icon name, unique number)

# 	i = 1
# 	for ws in bpy.data.workspaces:
# 		wsNames.append((ws.name, ws.name, "", i))
# 		i+=1
# 	return wsNames


def update_names_workspaces(self,context):
	'''
	check order of workspace and see what has changed since last call
	'''
	print(self)



#def defaultWSSmodes(self, context):
#	'''
#	Stores all default Object Modes when switching Workspaces
#	Used to set them back to default if "Keep Mode" is OFF
#	'''
#
#	#ws = bpy.data.workspaces
#	wsModes = []
#	i = 0
#	for ws in bpy.data.workspaces:
#		wsM = ws.object_mode
#		wsModes.append((str(i), wsM, ws.name))
#		i+=1
#	return wsModes


class QS_workspaceStore(PropertyGroup):
	qsWS0 : StringProperty(
		name = "ws0",
		default='Layout')


class QS_defaultWSSmodes(PropertyGroup):
	Layout : StringProperty(
		name = "Layout",
		default='OBJECT')
	Modeling : StringProperty(
		name = "Modeling",
		default='EDIT')
	Sculpting : StringProperty(
		name = "Sculpting",
		default='SCULPT')
	UV_Editing : StringProperty(
		name = "UV_Editing",
		default='EDIT')
	Texture_Paint : StringProperty(
		name = "Texture_Paint",
		default='TEXTURE_PAINT')
	Shading : StringProperty(
		name = "Shading",
		default='OBJECT')
	Rendering : StringProperty(
		name = "Rendering",
		default='OBJECT')
	Animation : StringProperty(
		name = "Animation",
		default='POSE')
	Compositing : StringProperty(
		name = "Compositing",
		default='OBJECT')
	Scripting : StringProperty(
		name = "Scripting",
		default='OBJECT')
	Default : StringProperty(
		name = "Default",
		default='OBJECT')

@persistent
def on_scene_update(scene):
	context = bpy.context
	scene = context.scene
	ws = context.workspace
	# settings = scene["qsWSsmode"]
	settings = scene.qsWSsmode
	wsstore = scene.qsWSstore
	wsstore.qsWS0 = bpy.data.workspaces['Modeling'].object_mode
	# print(wsstore.qsWS0)
	settings.Layout = 'OBJECT'
	# settings.Modeling = bpy.data.workspaces['Modeling'].object_mode
	settings.Modeling = 'EDIT'
	settings.Sculpting = 'SCULPT'
	settings.UV_Editing = 'EDIT'
	settings.Texture_Paint = 'TEXTURE_PAINT'
	settings.Shading = 'OBJECT'
	settings.Animation = 'POSE'
	settings.Rendering = 'OBJECT'
	settings.Compositing = 'OBJECT'
	settings.Scripting = 'OBJECT'
	settings.Default = 'OBJECT'

#class SetWSmodes(Operator):
#	bl_idname = "qs.set_ws_modes"
#	bl_label = "Set"
#	bl_description = "Saves standard workspace modes"
#
#	#@classmethod
#	#def poll(clss, context):
#	#    return ats_poll(context)
#
#	def execute(self, context):
#		if do_set_tile_size(context):
#			return {'FINISHED'}
#		return {'CANCELLED'}


viewLoc =  (0.0, 0.0, 0.0)
distance = 0
matrix = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
rotation = (0,0,0,0)
#bpy.types.Scene.qsDefWSmodes = bpy.props.EnumProperty(name = "Def WorkSpace Modes", items=defaultWSSmodes)
bpy.types.Scene.qsStore3dView = bpy.props.BoolProperty(name = "Store View", default=True, description="This stores the view in 3D View and sets this view to the workspace you are moving to.")

bpy.types.Scene.qsKeepMode = bpy.props.BoolProperty(name = "Keep Mode", default=False, description="This stores the current Object Interaction Mode, now when you switch workspaces you will return to prior mode and not the default one.")

# class QS_StoreView():
# 	## https://stackoverflow.com/questions/9028398/change-viewport-angle-in-blender-using-python
# 	#"""Get current view in the 3D View and store it for reuse"""
# 	#bl_idname = "qs.store_view"
# 	#bl_label = "Store View"

# 	def __init__(self, context):
# 		self.context = context
# 		#self.ViewPort = self.ViewPort()

# 	@property
# 	def view(self, context):
# 		""" Returns the set of 3D views.
# 		"""
# 		rtn = []
# 		# for a in self.context.window.screen.areas:
# 		for a in context.area:
# 			if a.type == 'VIEW_3D':
# 				rtn.append(a)
# 		return rtn

# 	def ViewPort(self, context):
# 		""" Return position, rotation data about a given view for the first space attached to it """
# 		global viewLoc, distance, rotation

# 		# for area in bpy.context.screen.areas:
# 		for area in context.area:
# 			if area.type == 'VIEW_3D':

# 				rv3d = area.spaces[0].region_3d
# 				view_Loc = rv3d.view_location
# 				viewloc = rv3d.view_location
# 				#viewloc = view_Loc[0],view_Loc[1],view_Loc[2]
# 				distance = rv3d.view_distance
# 				matrix = rv3d.view_matrix
# 				print(distance, "distannce")
# 				#camera_pos = self.camera_position(matrix)
# 				rotation = rv3d.view_rotation
# 				#rotation = rotation[0],rotation[1],rotation[2],rotation[3]
# 				#return view_Loc, rotation, distance #camera_pos,
# 		return

def ViewPort(wsn):
		""" Return position, rotation data about a given view for the first space attached to it """
		global viewLoc, distance, matrix, rotation

		for i, area in enumerate(bpy.context.screen.areas):
			if area.type == 'VIEW_3D':
				wsp = bpy.context.window.workspace
				rv3d = area.spaces[0].region_3d
				viewLoc = rv3d.view_location
				distance = rv3d.view_distance
				matrix = rv3d.view_matrix
				rotation = rv3d.view_rotation
				#camera_pos = self.camera_position(matrix)
				#rotation = rotation[0],rotation[1],rotation[2],rotation[3]
				#return view_Loc, rotation, distance #camera_pos,
				# print("Vloc: %s | Dist %s | Mtrx %s | Rot %s" % (viewLoc, distance, matrix, rotation))


class QS_Store3DView(PropertyGroup):
	distance: FloatProperty()
	viewLoc: FloatVectorProperty (
		subtype='TRANSLATION')
	rotation: FloatVectorProperty (
		subtype='QUATERNION',
		size=4)
	name: StringProperty()


@persistent
def on_ws_switch(scene):
	context = bpy.context
	scene = context.scene
	qssv = scene.qsStoreView

	wsn = context.workspace
	#try:
	ViewPort(wsn)

	global viewLoc, distance, matrix, rotation
	# viewport = QS_StoreView.ViewPort(context, context)
	qssv.viewLoc = viewLoc#str(viewLoc)
	qssv.distance = distance#str(distance)
	qssv.rotation = rotation#str(rotation)

	# viewLoc = viewLoc
	# distance = distance
	# matrix = matrix 
	# rotation = rotation

	# print("## %s - %s -%s" % (viewLoc,distance, rotation))
	#except:
	#	pass
	getView(context)


addon_keymaps = []

def add_hotkey():
	# preferences = bpy.context.preferences
	# addon_prefs = preferences.addons[__name__].preferences

	# Use alt or cmd for windows and osx
	cmdK = False if platform == "win32" else True
	altK = True if platform == "win32" else False

	# print("QS hotkeys added")
	wm = bpy.context.window_manager

	kc = wm.keyconfigs.addon    # for hotkeys within an addon
	km = kc.keymaps.new(name = "Screen", space_type = "EMPTY")

	#Add quick menu
	kmi = km.keymap_items.new("wm.call_menu",  value='PRESS', type='Q', ctrl=False, alt=altK, shift=False, oskey=cmdK)
	kmi.properties.name = "QS_MT_WorkspaceSwitchMenu"
	kmi.active = True
	addon_keymaps.append((km, kmi))

	#Add quick pie menu
	kmi = km.keymap_items.new("wm.call_menu_pie",  value='PRESS', type='Q', ctrl=False, alt=altK, shift=True, oskey=cmdK)
	kmi.properties.name = "QS_MT_WorkspaceSwitchPieMenu"
	kmi.active = True
	addon_keymaps.append((km, kmi))

	#Add QS Render Engine
	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	km = kc.keymaps.new(name = "Screen", space_type = "EMPTY")
	kmi = km.keymap_items.new("wm.call_menu", value='PRESS', type='E', alt=altK, shift=True, oskey=cmdK)
	kmi.properties.name = "QS_MT_QuickSwitchEngine"
	kmi.active = True
	addon_keymaps.append((km, kmi))

	hKeys = [("NUMPAD_1"), ("NUMPAD_2"), ("NUMPAD_3"), ("NUMPAD_4"),("NUMPAD_5"),("NUMPAD_6"),("NUMPAD_7"),("NUMPAD_8"),("NUMPAD_9"),("NUMPAD_0")]
	i=0
	
	for screen in hKeys:
		kmi = km.keymap_items.new("qs.workspace_set_layout", hKeys[i], "PRESS", alt=altK, oskey=cmdK)  # ...and if not found then add it
		kmi.properties.layoutName = "WorkspaceSwitcher"+str(i)  # also set proper name
		kmi.active = True
		addon_keymaps.append((km, kmi)) # also append to global (addon level) hotkey list for easy management
		i+=1

#class AddPresetQuickSwitch(AddPresetBase, Operator):
#	"""Add or remove a QuickSwitch Preset"""
#	bl_idname = "qs.preset_add"
#	bl_label = "Add QuickSwitch Preset"
#	preset_menu = "QS_PT_presets"
#
#	preset_defines = [
#		"qs = bpy.context.scene.quickswit"
#	]
#
#	preset_values = [
#		"qs.",
#		"qs.",
#		"qs.",
#		"qs.",
#		"qs.",
#		"qs.",
#	]
#
#	preset_subdir = "quickswitch"
#
#
#class QS_PT_presets(PresetMenu):
#	bl_label = "QuickSwitch Presets"
#	preset_subdir = "quickswitch"
#	preset_operator = "script.execute_preset"
#	draw = Menu.draw_preset

#class RIGIFY_MT_SettingsPresetMenu(Menu):
#    bl_label = "Setting Presets"
#    preset_subdir = "rigify"
#    preset_operator = "script.execute_preset"
#    draw = Menu.draw_preset


## TEST GITHUB CALL
#import ssl
#import urllib.request
#
#
#class QS_OT_AddonUpdater(Operator):
#	"""Quick check addonupdater 2.80"""
#	bl_idname="qs.addon_updater"
#	bl_label="Addon Updater"
#
#	def execute(self,context):
#		print(ssl.OPENSSL_VERSION)
#		api_url = 'https://api.github.com'
#		user = "schroef"
#		repo = "theaforblender"
#
#		url = "{}{}{}{}{}{}".format(api_url,"/repos/",user,"/",repo,"/tags")
#
#		request = urllib.request.Request(url)
#		context = ssl._create_unverified_context()
#		result = urllib.request.urlopen(request,context=context) # issue occurs here within blender
#		result_string = result.read()
#		result.close()
#		get = result_string.decode()
#		return {'FINISHED'}


class QS_MT_QuickSwitchEngine(Menu):
	bl_idname = "QS_MT_QuickSwitchEngine"
	bl_label = "Switch Engine & Render"

	def draw(self, context):
		layout = self.layout
		layout.operator_context = "INVOKE_AREA"
		prefs = context.preferences
		view = prefs.view

		scene = context.scene
		rd = scene.render

		if rd.has_multiple_engines:
			layout.prop(rd, "engine",  expand=True)

		# TEST GITHUB CALL
		#layout.separator()
		#layout.operator("qs.addon_updater", text="Addon Updater", icon='FILE_REFRESH')
		layout.separator()

		layout.operator("render.render", text="Render Image", icon='RENDER_STILL').use_viewport = True
		props = layout.operator("render.render", text="Render Animation", icon='RENDER_ANIMATION')
		props.animation = True
		props.use_viewport = True
		layout.prop_menu_enum(view, "render_display_type", text="Render in")

		layout.separator()
		layout.operator("render.view_show", text="View Render")
		layout.operator("render.play_rendered_anim", text="View Animation")

		layout.separator()

		layout.operator("render.opengl", text="Viewport Render Image", icon='RENDER_STILL')
		layout.operator("render.opengl", text="Viewport Render Animation", icon='RENDER_ANIMATION').animation = True
		if bpy.app.version > (2, 91):
			props = layout.operator("render.opengl",text="Viewport Render Keyframes",icon='RENDER_ANIMATION',
                                )
			props.animation = True
			props.render_keyed_only = True

		layout.separator()
		if bpy.app.version > (2, 81):
			layout.operator("screen.info_log_show", text="Display Log Info", icon='INFO')
			if not sys.platform == 'darwin':
				layout.operator("wm.console_toggle", text="Toggle System Console", icon='CONSOLE')
		
		layout.separator()
		layout.operator("wm.qs_path_open", text="Reveal Blend file", icon='FILE_FOLDER')


def get_hotkey_entry_item(km, kmi_name, kmi_value, properties):
	'''
	returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
	if there are multiple hotkeys!)
	'''
	
	for i, km_item in enumerate(km.keymap_items):
		if km.keymap_items.keys()[i] == kmi_name:
			# Use for Switch Engine, PopupMenu & PieMenu
			if properties == 'name':
				if km.keymap_items[i].properties.name == kmi_value:
					return km_item
			try:
				if km.keymap_items[i].properties.layoutName == kmi_value:
					# print(properties)
					# print(km.keymap_items[i].properties.layoutName)
					# print(km.keymap_items[i].properties.wslayoutMenu)
					# print("\n\n")
					# print("%s - %s" % (km.keymap_items[i].properties.layoutName, kmi_value))
					return km_item
			except:
				pass
	return None # not needed, since no return means None, but keeping for readability


class QS_MT_WorkspaceSwitchPieMenu(Menu):
	bl_idname = "QS_MT_WorkspaceSwitchPieMenu"
	bl_label = "Workspaces Pie Menu"

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		#pie = layout.menu_pie()

		wm = bpy.context.window_manager
		kc = wm.keyconfigs.user
		km = kc.keymaps['Screen']
		
		icons = [('Layout','VIEW3D'),('Modeling','VIEW3D'),('Sculpting','SCULPTMODE_HLT'),('UV Editing','UV'),('Texture Paint','IMAGE'),('Shading','SHADING_RENDERED'),('Animation','RENDER_ANIMATION'),('Rendering','RENDER_STILL'),('Compositing','NODE_COMPOSITING'),('Scripting','CONSOLE'),('Default','WORKSPACE')]

		for i in range(0,8):
			kmi = get_hotkey_entry_item(km, 'qs.workspace_set_layout', 'WorkspaceSwitcher'+str(i), 'layoutname')
			if not kmi == None:
				for k in range(0,len(icons)):
					if kmi.properties.wslayoutMenu in icons[k][0]:
						icon = icons[k][1]
						break
					elif kmi.properties.wslayoutMenu == "Preferences":
						icon = 'PREFERENCES'
					else:
						icon = 'WORKSPACE'
				if i == 3:
					pie = layout.menu_pie()
					split = pie.split()
					col = split.column(align=True)
					#Plain ol Booleans
					#row = col.row(align=True)
					col.scale_y=1.5
					col.scale_x=1.5
					col.prop(scene,"qsStore3dView")
					col.prop(scene,"qsKeepMode")
					col.operator("qs.workspace_set_layout", text='{}'.format(kmi.properties.wslayoutMenu),icon=icon).wslayoutMenu=kmi.properties.wslayoutMenu
				else:
					pie = layout.menu_pie()
					pie.operator("qs.workspace_set_layout", text='{}'.format(kmi.properties.wslayoutMenu),icon=icon).wslayoutMenu=kmi.properties.wslayoutMenu


class QS_MT_WorkspaceSwitchMenu(Menu):
	bl_idname = "QS_MT_WorkspaceSwitchMenu"
	bl_label = "Workspaces Menu"

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		layout.prop(scene,"qsStore3dView")
		layout.prop(scene,"qsKeepMode")
		layout.separator()

		wm = bpy.context.window_manager
		kc = wm.keyconfigs.user
		km = kc.keymaps['Screen']

		## Alphabetical order
		#for i in range(0,len(get_names_workspaces(self, context))):
		#	layout.operator("qs.workspace_set_layout", text='{}'.format(get_names_workspaces(self, context)[i][1]), icon='SEQ_SPLITVIEW').wslayoutMenu=get_names_workspaces(self, context)[i][1]

		icons = [('Layout','VIEW3D'),('Modeling','VIEW3D'),('Sculpting','SCULPTMODE_HLT'),('UV Editing','GROUP_UVS'),('Texture Paint','IMAGE'),('Shading','SHADING_RENDERED'),('Animation','RENDER_ANIMATION'),('Rendering','RENDER_STILL'),('Compositing','NODE_COMPOSITING'),('Scripting','CONSOLE'),('Default','WORKSPACE')]

		## Custom order
		for i in range(0,len(get_names_workspaces(self, context))):
			kmi = get_hotkey_entry_item(km, 'qs.workspace_set_layout', 'WorkspaceSwitcher'+str(i), 'layoutname')
			if not kmi == None:
				for k in range(0,len(icons)):
					if kmi.properties.wslayoutMenu in icons[k][0]:
						icon = icons[k][1]
						break
					elif kmi.properties.wslayoutMenu == "Preferences":
						icon = 'PREFERENCES'
					else:
						icon = 'WORKSPACE'

				layout.operator("qs.workspace_set_layout", text='{}'.format(kmi.properties.wslayoutMenu),icon=icon).wslayoutMenu=kmi.properties.wslayoutMenu
		layout.separator()

# def getView(context):
# 	for area in bpy.context.screen.areas:
# 		if area.type == 'VIEW_3D':
# 			qssw = context.scene.qsStoreView
# 			rv3d = area.spaces[0].region_3d
# 			rv3d.view_location = qssw.viewLoc#float(qssw.viewLoc[0]).strip(", ") #,float(qssw.viewLoc[1]),float(qssw.viewLoc[2]))
# 			rv3d.view_distance = qssw.distance#float(qssw.distance)
# 			rv3d.view_rotation = qssw.rotation#float(qssw.rotation)
# 			# rv3d.view_matrix = matrix#float(qssw.rotation)

# 			return


class QS_OT_SetWorkspace(Operator):
	"""Switches to the Workspace of the given name."""
	bl_idname="qs.workspace_set_layout"
	bl_label="Switch to Workspace"

	wslayoutMenu: bpy.props.EnumProperty(name = "Workspace", items = get_names_workspaces) #, update=update_names_workspaces)
	layoutName: bpy.props.StringProperty()

	def execute(self,context):
		scene = context.scene
		ws = context.workspace # returns name before we set it, this is
		
		# from MACHIN3tools
		wsp = bpy.data.workspaces.get(self.wslayoutMenu)
		view = self.getView(context, wsp)

		if self.wslayoutMenu == "Preferences":
			bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
			# Go to Quickswitch addon
			bpy.context.preferences.active_section = 'ADDONS'
			bpy.context.window_manager.addon_search = 'quickswitch'
			# force panel redraw
			context.area.tag_redraw()

			return{'FINISHED'}
		else:
			if scene.qsKeepMode:
				obj = bpy.context.object
				for obj in bpy.context.scene.objects:
					if obj.type == 'MESH':
						ws = context.workspace
						if ws.object_mode != obj.mode:
							ws.object_mode=obj.mode
							break
			else:
				wsN = ws.name
				#print(ws.name)
				if wsN == 'UV Editing':
					wsN = 'UV_Editing'
				if wsN == 'Texture Paint':
					wsN = 'Texture_Paint'
			
				# Set interaction mode
				ws.object_mode = scene.qsWSsmode[wsN]

			# if not ws.name in scene.qsWSsmode:
			# 	print("default mode")
			# # else:
			# # 	# Revert to default object mode, if default names are not used or workspace are cahnged after opening
			# 	ws.object_mode = scene.qsWSsmode['Default']
			# # 	print(self.wslayoutMenu)
			# # 	print(self.layoutName)

			# wsn = context.workspace
			# ViewPort(wsn)
			bpy.context.window.workspace = bpy.data.workspaces[self.wslayoutMenu]
			
			if scene.qsStore3dView:
				# items = scene.qsStoreView
				# print("Viewloc: %s" % items.viewLoc)
				self.setView(context, wsp, view)

		return {'FINISHED'}

	def getView(self,context, wsp):
		""" Return position, rotation data about a given view for the first space attached to it """
		global viewLoc, distance, matrix, rotation

		view = {}
		
		for i, area in enumerate(context.screen.areas):
			if area.type == 'VIEW_3D':
				for space in area.spaces:
					if space.type == 'VIEW_3D':
						# wsp = context.window.workspace
						rv3d = space.region_3d
						
						# from MACHIN3tools
						view["viewLoc"] = rv3d.view_location
						view["distance"] = rv3d.view_distance
						view["rotation"] = rv3d.view_rotation
						# view["matrix"] = rv3d.view_matrix
						view['view_perspective'] = rv3d.view_perspective

						view['is_perspective'] = rv3d.is_perspective
						view['is_side_view'] = rv3d.is_orthographic_side_view
			# Return none for non 3dviews, otherwise error
			else:
				view["viewLoc"] = None

		# return view if rv3d.view_perspective != 'CAMERA' else None
		return view

	def setView(self,context, workspace, view):
		for screen in workspace.screens:
			for area in screen.areas:
				if area.type == 'VIEW_3D':
					for space in area.spaces:
						if space.type == 'VIEW_3D':
							rv3d = space.region_3d
							qssw = context.scene.qsStoreView
							# rv3d = area.spaces[0].region_3d
							# rv3d.view_location = qssw.viewLoc#float(qssw.viewLoc[0]).strip(", ") #,float(qssw.viewLoc[1]),float(qssw.viewLoc[2]))
							# rv3d.view_distance = qssw.distance#float(qssw.distance)
							# rv3d.view_rotation = qssw.rotation#float(qssw.rotation)
							# rv3d.view_matrix = matrix#float(qssw.rotation)
							
							# If we come from a none 3dview skip it
							# print(view["viewLoc"])
							if view["viewLoc"] != None:
								# from MACHIN3tools
								rv3d.view_location = view["viewLoc"] #float(qssw.viewLoc[0]).strip(", ") #,float(qssw.viewLoc[1]),float(qssw.viewLoc[2]))
								rv3d.view_distance = view["distance"] #float(qssw.distance)
								rv3d.view_rotation = view["rotation"] #float(qssw.rotation)

								# don't set camera views
								if rv3d.view_perspective != 'CAMERA':
									rv3d.view_perspective = view['view_perspective']

									rv3d.is_perspective = view['is_perspective']
									rv3d.is_orthographic_side_view = view['is_side_view']
							else:
								print("## QS > Skipping #DV Matching Workspace")
							return



#######################################################
## 3DVIEW VIEW SETTINGS
class QS_PG_ViewData(PropertyGroup):
    name = StringProperty()
    lens : FloatProperty()
    clip_start : FloatProperty()
    clip_end : FloatProperty()

def QS_store_3dview_data(self, context):
	view3d = context.space_data
	# context = bpy.context
	scene = context.scene
	qs3dvd = scene.qs3DViewData

	qs3dvd.lens = view3d.lens
	qs3dvd.clip_start = view3d.clip_start
	qs3dvd.clip_end = view3d.clip_end
	if scene.qsSync3dView:
		for ws in bpy.data.workspaces:
			for area in bpy.data.workspaces[ws.name].screens[0].areas:
				if area.type == 'VIEW_3D':
					viewd = area.spaces.active
					viewd.lens = qs3dvd.lens
					viewd.clip_start = qs3dvd.clip_start
					viewd.clip_end = qs3dvd.clip_end
		

class QD_OT_Sync_ViewData(Operator):
	"""Syncs all 3DViews view settings"""
	bl_idname = "qs.sync_viewdata"
	bl_label = "Sync Viewports"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		view3d = context.space_data
		for ws in bpy.data.workspaces:
			for area in bpy.data.workspaces[ws.name].screens[0].areas:
				if area.type == 'VIEW_3D':
					viewd = area.spaces.active
					viewd.lens = view3d.lens
					viewd.clip_start = view3d.clip_start
					viewd.clip_end = view3d.clip_end

		return {"FINISHED"}	


class QD_OT_Reset_ViewData(Operator):
	"""Resets all 3DViews view settings"""
	bl_idname = "qs.reset_viewdata"
	bl_label = "Reset Viewports"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		for ws in bpy.data.workspaces:
			for area in bpy.data.workspaces[ws.name].screens[0].areas:
				if area.type == 'VIEW_3D':
					viewd = area.spaces.active
					viewd.lens = 50
					viewd.clip_start = 0.1
					viewd.clip_end = 1000

		return {"FINISHED"}	
					

bpy.types.Scene.qsSync3dView = bpy.props.BoolProperty(
	name = "Sync Viewports", 
	default=False, 
	description="Syncs all 3DViews view settings",
	update=QS_store_3dview_data)


# 
# Function: Opens folder current blend file 
# 
class QS_OT_path_open(bpy.types.Operator):
	"Open a path in a file browser"
	bl_idname = "wm.qs_path_open"
	bl_label = ""

	filepath : StringProperty(name="File Path", maxlen= 1024)

	@classmethod
	def poll(cls, context):
		return os.path.dirname(bpy.data.filepath)

	def execute(self, context):
		filepath = os.path.dirname(bpy.data.filepath)
		
		if not os.path.exists(filepath):
			self.report({'ERROR'}, "File '%s' not found" % filepath)
			return {'CANCELLED'}
		print(filepath)
		if sys.platform == 'win32':
			# subprocess.Popen(['start', filepath], shell= True)
			# https://stackoverflow.com/questions/281888/open-explorer-on-a-file
			subprocess.Popen(r'explorer /open,"'+filepath+'\"')
		elif sys.platform == 'darwin':
			subprocess.Popen(['open', "-R", filepath])

		return {'FINISHED'}


def ui_add_menu(self, context):
	# scene = context.scene
	col = self.layout.column(align=True)
	row = col.row(align=True)
	row.label(text='Sync views')
	row.operator(QD_OT_Sync_ViewData.bl_idname, icon="UV_SYNC_SELECT",text="")
	# row.operator(QD_OT_Sync_ViewData.bl_idname, icon="UV_SYNC_SELECT")
	row.operator(QD_OT_Reset_ViewData.bl_idname, icon="LOOP_BACK", text="")
    
########################################################


#-- ADDON PREFS --#
class QS_PT_AddonPreferences(AddonPreferences):
	""" Preference Settings Addin Panel"""
	bl_idname = __name__

	qsMenus: bpy.props.EnumProperty(name = "QuickSwitch Options", items = [("Workspaces","Workspaces","Workspaces"),("Render_Menu","Render Menu","Render Menu")])

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		ws = context.workspace
		col = layout.column()

		#layout.prop(scene, "qsDefWSmodes")
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
			kmi = get_hotkey_entry_item(km, 'wm.call_menu', 'QS_MT_WorkspaceSwitchMenu', 'name')
			if kmi:
				col.label(text='Quick Switch Menu:')
				col.context_pointer_set("keymap", km)
				rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
			else:
				col.label(text="restore hotkeys from interface tab")


			kmi = get_hotkey_entry_item(km, 'wm.call_menu_pie', 'QS_MT_WorkspaceSwitchPieMenu', 'name')
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
			for i in range(0,len(get_names_workspaces(self, context))):
	#			if km.keymap_items.keys()[i] == 'Switch to Workspace':
				kmi = get_hotkey_entry_item(km, 'qs.workspace_set_layout', 'WorkspaceSwitcher'+str(i), 'layoutname')
				if not kmi == None:
					if kmi:
						col.context_pointer_set("keymap", km)
						rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
					else:
						col.label(text="restore hotkeys from interface tab")
			col.label(text='Set each shortcut in the dropdown menu named "Workspace"')

		if getattr(self,"qsMenus") in ("Render_Menu"):
			wm = bpy.context.window_manager
			kc = wm.keyconfigs.user
			km = kc.keymaps['Screen']
			box=layout.box()
			split = box.split()
			col = split.column()
			col.label(text='Set Render Menu:')
			kmi = get_hotkey_entry_item(km, 'wm.call_menu', 'QS_MT_QuickSwitchEngine', 'name')
			if kmi:
				col.context_pointer_set("keymap", km)
				rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
				col.label(text = "Quick export using last settings")

			else:
				col.label(text = "restore hotkeys from interface tab")



#Classes for register and unregister
classes = [
	QS_workspaceStore,
	QS_defaultWSSmodes,
	QS_Store3DView,
	# QS_StoreView,
	#AddPresetQuickSwitch,
	#QS_PT_presets,
	#QS_OT_AddonUpdater,
	QS_PG_ViewData,
	QD_OT_Sync_ViewData,
	QD_OT_Reset_ViewData,
	QS_PT_AddonPreferences,
	QS_MT_QuickSwitchEngine,
	QS_MT_WorkspaceSwitchPieMenu,
	QS_MT_WorkspaceSwitchMenu,
	QS_OT_SetWorkspace,
	QS_OT_path_open,
]

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.qsWSstore = PointerProperty(type=QS_workspaceStore)
	bpy.types.Scene.qsWSsmode = PointerProperty(type=QS_defaultWSSmodes)
	bpy.types.Scene.qsStoreView = PointerProperty(type=QS_Store3DView)
	bpy.types.Scene.qs3DViewData = PointerProperty(type=QS_PG_ViewData)

	# hotkey setup
	add_hotkey()

	# Check workspace names and interaction mode
	bpy.app.handlers.depsgraph_update_pre.append(on_scene_update)
	# bpy.app.handlers.depsgraph_update_pre.append(on_ws_switch)
	bpy.types.VIEW3D_PT_view3d_properties.prepend(ui_add_menu)



def unregister():
	bpy.app.handlers.depsgraph_update_pre.remove(on_scene_update)
	# bpy.app.handlers.depsgraph_update_pre.remove(on_ws_switch)
	bpy.types.VIEW3D_PT_view3d_properties.remove(ui_add_menu)
	
	# handle the keymap
	for km, kmi in addon_keymaps:
		print("QS: %s - %s" % (km,kmi))
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.qsWSsmode
	del bpy.types.Scene.qsStoreView
	# del bpy.types.Scene.qs3DViewData



if __name__ == "__main__":
	register()
