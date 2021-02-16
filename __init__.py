# NodePie addon for Blender 2.80+ to create custom nested pie menus for nodes in the node editor
# Managed by: Binit (aka Yeetus)
# Contact me via twitter(@yeetusblenditus), email(binitnew@gmail.com) or my discord server (https://discord.gg/G8ajxwQuYT)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import bpy
import bpy.utils.previews
import os
import json
from bpy.props import StringProperty, IntProperty, CollectionProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, Menu, AddonPreferences
from .NodePie_lists import node_names, node_dir, icon_list

bl_info = {
	"name" : "NodePie",
	"author" : "Binit (Yeetus)",
	"description" : "Pie menu creator for nodes!",
	"blender" : (2, 80, 0),
	"version" : (1, 0, 0),
	"location" : "Node editor > N-Panel, Shift+Q in NodeEditor",
	"warning" : "",
	"category" : "Interface"
}

is_init = False # state of if props are initialized 
json_dir = os.path.join(os.path.dirname(__file__), "NodePie_Preset.json")


def InitProps(): # populate the pie operators list with the list of nodes the first time its called.
	global is_init

	if is_init == False:
		for i in node_names:
			new = bpy.context.scene.pie_ops.add()
			new.name = i
		is_init = True
		return None
	else:
		return None

def EditProp(self, context): # function to rename the prop from pie_ops collection if edited in the list
	context.scene.pie_ops[context.scene.list_index - len(context.scene.menu_list)].name = self.name
	return None

def CreatePies(index): # function to dynamically create the pie menus as according the the pie menu list
	
	# create pie menu for each time it is called in the NewPiemenu operator
	#i = len(bpy.context.scene.menu_list) - 1

	idname = "node.pie_menu_%d" % index
		
	def func(self, context):
		layout = self.layout
		pie = layout.menu_pie()

		for operator_index in range(8):
			name = context.scene.pie_elements[(self.iterator * 8) + operator_index].name
			title = context.scene.pie_elements[(self.iterator * 8) + operator_index].title

			if name in bpy.context.scene.menu_list:
				index = int(bpy.context.scene.menu_list[name].path_from_id()[10:-1])
				pie.operator('wm.call_menu_pie', text = title, icon_value=pcoll[icon_list[operator_index]].icon_id).name = f'MENU_MT_dynPie_{index}'
			else:
				ID = node_dir[bpy.context.scene.pie_elements[(self.iterator * 8) + operator_index].name]
				op = pie.operator('nodepie.insert_node', text = title , icon_value=pcoll[icon_list[operator_index]].icon_id)
				op.node_id = ID
				op.node_name = name
				
	DynamicPiemenus = type(f"MENU_MT_dynPie_{index}", (Menu, ), 
	{"bl.idname": idname, 
	"bl_label": bpy.context.scene.menu_list[index].name, 
	"iterator" : index, 
	"draw": func}, )
				
	bpy.utils.register_class(DynamicPiemenus)    

class MenuList(PropertyGroup):
	"""List of all the primary pie menu and sub pie menus."""
	name: bpy.props.StringProperty(default="DefaultPieMenu", update = EditProp)
		
class PieOperators(PropertyGroup):
	"""List of all nodes and pie menus to be picked from for each pie menu operator."""
	name: StringProperty()
	
class PieElements(PropertyGroup):
	"""List of all the elements of all pie menus."""
	name: StringProperty()
	title: StringProperty()

class InsertNode(Operator):
	'''Insert given node into the editor'''
	bl_idname = "nodepie.insert_node"
	bl_label = "Insert Node"

	node_id = bpy.props.StringProperty()
	node_name = bpy.props.StringProperty()
	
	def execute(self, context):
		
		tree = context.space_data.edit_tree
		
		for node in tree.nodes:
			node.select = False
		
		node_words = self.node_name.split()
		
		# kinda hacky way to set operation/blend_type for particular nodes (actually, everything here is kinda hacky if you think about it but well, it works! good enough, I'll take it.)
		if len(node_words) > 2 and node_words[-2:] == ['Vector', 'Math']:
			node = tree.nodes.new('ShaderNodeVectorMath')
			node.operation = self.node_id
			
		elif len(node_words) > 1 and node_words[-1] == 'Math' and node_words[-2] != 'Vector':
			node = tree.nodes.new('ShaderNodeMath')
			node.operation = self.node_id
			
		elif node_words[-1] == 'Color':
			node = tree.nodes.new('ShaderNodeMixRGB')
			node.blend_type = self.node_id
		else:
			node = tree.nodes.new(self.node_id)
		
		node.select= True
		tree.nodes.active = node
		node.location = context.space_data.cursor_location
		
		return {'FINISHED'} 

class NodePieList(UIList):
	"""UI List of all pie menus."""

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.label(text=item.name, icon = 'NODE')

		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			layout.label(text="test", icon = 'NODE')

class NewPiemenu(Operator):
	"""Add a new pie menu to the list."""
	bl_idname = "nodepie.new_piemenu"
	bl_label = "Add a new Pie Menu"

	def execute(self, context):

		InitProps() # initialize the pie_ops list

		name = 'DefaultPie' if len(context.scene.menu_list) == 0 else f'SubPie{len(context.scene.menu_list)}'
		newItem = context.scene.menu_list.add()
		newItem.name = name
		
		for menu_index in range(8):
			newCustomItem = bpy.context.scene.pie_elements.add()
			newCustomItem.name = "Texture Coordinate"

		newPieMenu = bpy.context.scene.pie_ops.add()
		newPieMenu.name = name
		
		CreatePies(index = len(bpy.context.scene.menu_list)-1)
		
		return{'FINISHED'} 	

class RemovePiemenu(Operator):
	"""Remove the selected Pie Menu."""
	bl_idname = "nodepie.remove_piemenu"
	bl_label = "Remove selected Pie Menu"

	@classmethod
	def poll(cls, context):
		return context.scene.menu_list

	def execute(self, context):
		menu_list = context.scene.menu_list
		index = context.scene.list_index
		
		context.scene.pie_ops.remove(len(context.scene.pie_ops)+(index-len(menu_list)))
		
		menu_list.remove(index)
		context.scene.list_index = min(max(0, index - 1), len(menu_list) - 1)
		
		for i in range(8):
			context.scene.pie_elements.remove((8*index)+i)	

		return {'FINISHED'}

class SaveToJson(Operator):
	"""Export preset as a json file"""
	bl_idname = "nodepie.save_to_json"
	bl_label = "Save Preset"

	def execute(self, context):

		menu_dir = [prop.items() for prop in context.scene.menu_list]
		menu_data = json.dumps(menu_dir)

		pieops_dir = [prop.items() for prop in context.scene.pie_ops]
		pieops_data = json.dumps(pieops_dir)

		elems_dir = [prop.items() for prop in context.scene.pie_elements]
		elems_data = json.dumps(elems_dir)

		with open(json_dir, 'w') as outfile:
			outfile.write(menu_data+'\n')
			outfile.write(pieops_data+'\n')
			outfile.write(elems_data+'\n')

		return {'FINISHED'}

class LoadFromJson(Operator):
	"""Import preset from json file"""
	bl_idname = "nodepie.load_from_json"
	bl_label = "Load Preset"

	def execute(self, context):

		json_data = []

		with open(json_dir, 'r') as infile:
			for line in infile:
				json_line = json.loads(line)
				json_data.append(json_line)

		# clear the collection properties before populating them from the json data
		context.scene.menu_list.clear()
		context.scene.pie_ops.clear()
		context.scene.pie_elements.clear()

		for prop_list in json_data[0]:
			prop = context.scene.menu_list.add()
			for key, value in prop_list:
				prop[key] = value

		for prop_list in json_data[1]:
			prop = context.scene.pie_ops.add()
			for key, value in prop_list:
				prop[key] = value

		for prop_list in json_data[2]:
			prop = context.scene.pie_elements.add()
			if len(prop_list) == 2:
				prop.name = prop_list[0][1]
				prop.title = prop_list[1][1]
			else:
				prop.name = prop_list[0][1]
				prop.title = ''

		return {'FINISHED'}

class NodePiePanel(Panel):
	"""Demo panel for UI list Tut"""
	bl_label = "NodePie" 
	bl_idname = "nodepie_panel" 
	bl_space_type = 'NODE_EDITOR' 
	bl_region_type = 'UI'
	bl_category = 'NodePie'
	bl_context = "scene"

	def draw(self, context): 
		layout = self.layout 
		scene = context.scene
		  
		row = layout.row() 
		row.template_list("NodePieList", "The_List", scene, "menu_list", scene, "list_index")
		
		col = row.column(align=True)
		col.operator('nodepie.new_piemenu', icon='ADD', text='')
		col.operator('nodepie.remove_piemenu', icon='REMOVE', text = '')

		if scene.list_index >= 0 and scene.menu_list: 
			item = scene.menu_list[scene.list_index] 

			row = layout.row(align=True)
			row.prop(item, "name")
		
		row = layout.row()
		row.label(icon= 'SEQ_CHROMA_SCOPE')
		row.label(text= "Title")
		row.label(text= "Operator Node/Menu")
		
		if len(context.scene.menu_list) != 0:
			for menu_index in range(8):
				row = layout.row(align=True)
				row.label(icon_value=pcoll[icon_list[menu_index]].icon_id)
				row.prop(scene.pie_elements[(context.scene.list_index*8)+menu_index], "title", text = '')
				row.prop_search(scene.pie_elements[(context.scene.list_index*8)+menu_index], "name", context.scene, "pie_ops", text='')

		row = layout.row()
		row = layout.row()
		row.scale_y = 2.5
		row.operator('nodepie.save_to_json', icon = 'FILE_TICK', text = 'Save Preset')
		row.operator('nodepie.load_from_json', icon = 'FILE', text = 'Load Preset')

class LoadNodePie(Operator):
	"""Initialize pie menus"""
	bl_idname = 'nodepie.load_menu'
	bl_label = 'Initialize NodePie'

	def execute(self, context):

		global is_init
		if is_init == False:
			bpy.ops.nodepie.load_from_json()

			for i in range(len(context.scene.menu_list)):
				CreatePies(i)

			is_init = True
			
		bpy.ops.wm.call_menu_pie(name="MENU_MT_dynPie_0")

		return {'FINISHED'}


addon_keymaps = [] # variable to hold keymaps
pcoll = None # custom icon collection variable

classes = (MenuList, PieElements, NodePieList, NewPiemenu, RemovePiemenu, 
	NodePiePanel, PieOperators, InsertNode, SaveToJson, LoadFromJson, LoadNodePie) 

def register():

	for CLS in classes:
		bpy.utils.register_class(CLS)

	bpy.types.Scene.pie_ops = CollectionProperty(type = PieOperators)
	bpy.types.Scene.menu_list = CollectionProperty(type = MenuList) 
	bpy.types.Scene.list_index = IntProperty(name = "NodePie Menu", default = 0)
	bpy.types.Scene.pie_elements = CollectionProperty(type = PieElements)

	# register shortcut keys
	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	if kc:
		km = kc.keymaps.new(name='Node Editor',space_type='NODE_EDITOR')
		kmi = km.keymap_items.new(LoadNodePie.bl_idname,type='Q',value='PRESS',shift=True)
		#kmi.properties.name = 'MENU_MT_dynPie_0'
		addon_keymaps.append((km,kmi))

	global pcoll 
	pcoll = bpy.utils.previews.new()

	my_icons_dir = os.path.join(os.path.dirname(__file__), "icons") # get the directiory from where the custom icons are to be loaded

	# load a preview thumbnail of a file and store in the previews collection
	for i in range(8):
		pcoll.load(icon_list[i], os.path.join(my_icons_dir, f'{icon_list[i]}.png'), 'IMAGE')
	
	global is_init
	is_init = False	

def unregister():

	for CLS in classes:
		bpy.utils.unregister_class(CLS)

	#del bpy.types.Scene.menu_list
	#del bpy.types.Scene.list_index
	#del bpy.types.Scene.pie_elements
	#del bpy.types.Scene.pie_ops

	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()

	global pcoll
	bpy.utils.previews.remove(pcoll)