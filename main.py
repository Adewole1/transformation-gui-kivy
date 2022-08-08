from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton, MDTextButton
from kivy.metrics import dp
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import NoTransition, FadeTransition, ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.snackbar import Snackbar, BaseSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget, OneLineIconListItem, TwoLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from kivy.core.window import Window

from math import radians, cos, sin
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


import os

# from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

from transform import Transform

Window.softinput_mode = "pan"


class CustomSnackbar(BaseSnackbar): 
	text = StringProperty(None) 
	icon = StringProperty(None) 
	font_size = NumericProperty("12sp")


class IconListItem(OneLineIconListItem): 
	icon = StringProperty()
	
	
class IconListItem2(TwoLineIconListItem): 
	icon = StringProperty()


class TranslateContent(BoxLayout):
	pass


class RotateContent(BoxLayout):
	pass


class ScaleContent(BoxLayout):
	pass


class ShearContent(BoxLayout):
	pass


class ReflectContent(BoxLayout):
	pass


class CoordTab(MDFloatLayout, MDTabsBase):
	'''Class implenting content for a tab'''


class TransTab(MDFloatLayout, MDTabsBase):
	'''Class implenting content for a tab'''


class Content(MDBoxLayout): 
	'''Custom content.'''


class SummaryScreen(MDScreen):
	data_tables = None
	
	def on_pre_enter(self):
		data = self.manager.get_screen('coord').data_tables
		data2 = self.manager.get_screen('trans').ids.container.children[::-1]
		
		if data:
			self.data_tables = MDDataTable(
				use_pagination=True,
				column_data=data.column_data,
				row_data=data.row_data,
				size_hint=[0.95, 0.78],
				pos_hint={'center_x': 0.5, 'top':0.95},
				background_color_header=[0,0,0,1]
				)
			self.ids.layout.add_widget(self.data_tables)
			
		if len(self.manager.get_screen('trans').ids.container.children) !=0:
			for el in data2:
				self.ids.container.add_widget(
					TwoLineIconListItem(
						text=el.text,
						secondary_text=el.secondary_text,
						#icon=el.icon,
						)
					)
					
		self.ids.D.text = MDApp.get_running_app().d_type
		self.ids.cord.text = 'Edit Coordinates' if self.data_tables else 'Add Coordinates'
		self.ids.trans.text = 'Edit Transformation' if len(self.ids.container.children)>0 else 'Add Transformation'
		self.ids.done1.opacity = 1 if self.data_tables and len(self.ids.container.children)>0 else 0
		self.ids.done1.disabled = False if self.data_tables and len(self.ids.container.children)>0 else True
		self.ids.done2.opacity = 1 if self.data_tables and len(self.ids.container.children)>0 else 0
		self.ids.done2.disabled = False if self.data_tables and len(self.ids.container.children)>0 else True
					
	def on_leave(self):
		#self.ids.layout.clear_widgets()
		self.ids.container.clear_widgets()
	
	def previous_screen(self):
		self.manager.current = 'trans'

	def done(self):
		app = MDApp.get_running_app()
		self.transform(app.d_type, app.coordinates, app.transformed_list)
		#app.transformer.transform(app.d_type, app.coordinates, app.transformed_list)

	def transform(self, d_type, coord, trans):
		t_coord = coord

		for el in trans:
			t_coord = np.dot(t_coord, el)
		if MDApp.get_running_app().theme_cls.theme_style == 'Dark':
			sns.set_style('darkgrid')
		else:
			sns.set_style('whitegrid')
		if d_type == '2D':
			X1 = coord[:, 0]
			X1 = np.append(X1, X1[0])
			Y1 = coord[:, 1]
			Y1 = np.append(Y1, Y1[0])
			X2 = t_coord[:, 0]
			X2 = np.append(X2, X2[0])
			Y2 = t_coord[:, 1]
			Y2 = np.append(Y2, Y2[0])
			plt.plot(X1, Y1, '-')
			plt.plot(X2, Y2, '--')
			plt.legend(['Original Shape', 'Transformed shape'])
			
		else: 
			X1 = coord[:, 0]
			X1 = np.append(X1, X1[0])
			Y1 = coord[:, 1]
			Y1 = np.append(Y1, Y1[0])
			Z1 = coord[:, 2]
			Z1 = np.append(Z1, Z1[0])
			X2 = t_coord[:, 0]
			X2 = np.append(X2, X2[0])
			Y2 = t_coord[:, 1]
			Y2 = np.append(Y2, Y2[0])
			Z2 = t_coord[:, 2]
			Z2 = np.append(Z2, Z2[0])
			axes = plt.axes(projection='3d')
			axes.plot_surface(X1, Y1, Z1)
			axes.plot_surface(X2, Y2, Z2)
		
		self.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class TransScreen(MDScreen):
	
	custom_sheet = None
	dialog = None
	last = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
	def reflect_changed(self, text):
		self.dialog.content_cls.ids.reflect_axis.text=text
		if text=='Line':
			self.dialog.content_cls.ids.line_ref.opacity=1
			self.dialog.content_cls.ids.line_ref.disabled=False
		else:
			self.dialog.content_cls.ids.line_ref.opacity=0
			self.dialog.content_cls.ids.line_ref.disabled=True
		self.axis_direction.dismiss()
		
	def ref_changed(self, text):
		self.dialog.content_cls.ids.line_ref.text=text
		#self.line_ref.dismiss()
		
	def plane_changed(self, text):
		self.dialog.content_cls.ids.reflect_plane.text=text
		self.plane_direction.dismiss()
			
	def axis2_points(self, text):
		self.dialog.content_cls.ids.axis2.text=text
		self.dialog.content_cls.ids.points.opacity=1 if text=='Point' else 0
		self.dialog.content_cls.ids.points.disabled=False if text=='Point' else True
		
		self.axis2.dismiss()

	def direction_changed(self, text):
		self.dialog.content_cls.ids.direction.text=text
		self.direction.dismiss()

	def axis3_changed(self, text):
		self.dialog.content_cls.ids.axis3.text=text
		self.axis3.dismiss()
		
	def shear_changed(self, text):
		hid = self.dialog.content_cls.ids
		hid.shear_direction.text=text
		self.shear_direction.dismiss()
		
	def relative_changed(self, text):
		self.dialog.content_cls.ids.relative.text=text
		self.dialog.content_cls.ids.parameter_l.opacity=1 if text=='Yes' else 0
		self.dialog.content_cls.ids.parameter_l.disabled=False if text=='Yes' else True
		self.relative.dismiss()
		
	def menu(self):
		self.custom_sheet = MDCustomBottomSheet(
			screen=Factory.ContentCustomSheet())
		self.custom_sheet.open()
		
	def transform(self, trans, d_type):
		self.last = trans
		if trans=='Translate':
			if not self.dialog:
				self.dialog = MDDialog(
					title=trans,
					type='custom',
					content_cls=TranslateContent(),
					buttons=[
						MDFlatButton(
							text="CANCEL",
							on_release=self.dialog_close
							),
						MDRaisedButton(
							text="ACCEPT",
							theme_text_color="Custom",
							text_color=[1,1,1,1],
							on_release=self.add_translate
							)
						], )
			self.dialog.open()
		elif trans=='Rotate':
			if not self.dialog:
				self.dialog = MDDialog(
					title=trans,
					type='custom',
					content_cls=RotateContent(),
					buttons=[
						MDFlatButton(
							text="CANCEL",
							on_release=self.dialog_close
							),
						MDRaisedButton(
							text="ACCEPT",
							theme_text_color="Custom",
							text_color=[1,1,1,1],
							on_release=self.add_rotate
							)
						], )
						
				menu_direction = [
					{
						'viewclass': 'OneLineListItem',
						'text': 'Clockwise',
						'height': dp(56),
						'on_release': lambda x='Clockwise': self.direction_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Counter-clockwise',
						'height': dp(40),
						'on_release': lambda x='Counter-clockwise': self.direction_changed(x)
					},
					]
				self.direction = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.direction,
					items=menu_direction,
					position='bottom',
					width_mult=4)
					
				menu_axis3 = [
					{
						'viewclass': 'OneLineListItem',
						'text': 'X',
						'height': dp(56),
						'on_release': lambda x='X': self.axis3_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Y',
						'height': dp(40),
						'on_release': lambda x='Y': self.axis3_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Z',
						'height': dp(40),
						'on_release': lambda x='Z': self.axis3_changed(x)
					},
					]
				self.axis3 = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.axis3,
					items=menu_axis3,
					position='bottom',
					width_mult=4)
					
				menu_axis2= [
					{
						'viewclass': 'OneLineListItem',
						'text': 'Point',
						'height': dp(40),
						'on_release': lambda x='Point': self.axis2_points(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Origin',
						'height': dp(40),
						'on_release': lambda x='Origin': self.axis2_points(x)
					},
					]
				self.axis2 = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.axis2,
					items=menu_axis2,
					position='bottom',
					width_mult=4)
			if MDApp.get_running_app().d_type=='2D':
				self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.axis3)
			else:
				self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.axis2)
				self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.points)
				#self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.points2)
			self.dialog.open()
		elif trans=='Scale':
			if not self.dialog:
				self.dialog = MDDialog(
					title=trans,
					type='custom',
					content_cls=ScaleContent(),
					buttons=[
						MDFlatButton(
							text="CANCEL",
							on_release=self.dialog_close
							),
						MDRaisedButton(
							text="ACCEPT",
							theme_text_color="Custom",
							text_color=[1,1,1,1],
							on_release=self.add_scale
							)
						], )
			self.dialog.open()
			
		elif trans=='Shear':
			if not self.dialog:
				self.dialog = MDDialog(
					title=trans,
					type='custom',
					content_cls=ShearContent(),
					buttons=[
						MDFlatButton(
							text="CANCEL",
							on_release=self.dialog_close
							),
						MDRaisedButton(
							text="ACCEPT",
							theme_text_color="Custom",
							text_color=[1,1,1,1],
							on_release=self.add_shear
							)
						], )
						
				menu_shear = [
					{
						'viewclass': 'OneLineListItem',
						'text': 'X',
						'height': dp(56),
						'on_release': lambda x='X': self.shear_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Y',
						'height': dp(40),
						'on_release': lambda x='Y': self.shear_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Z',
						'height': dp(40) if MDApp.get_running_app().d_type=='3D' else 0,
						'on_release': lambda x='Z': self.shear_changed(x)
					},
					]
				self.shear_direction = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.shear_direction,
					items=menu_shear,
					position='bottom',
					width_mult=4)
					
				menu_relative = [
					{
						'viewclass': 'OneLineListItem',
						'text': 'Yes',
						'height': dp(56),
						'on_release': lambda x='Yes': self.relative_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'No',
						'height': dp(40),
						'on_release': lambda x='No': self.relative_changed(x)
					},
					]
				self.relative = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.relative,
					items=menu_relative,
					position='bottom',
					width_mult=4)
				
			if MDApp.get_running_app().d_type=='2D':
				if 'shear_x' in self.dialog.content_cls.ids.keys():
					self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.shear_x)
				if 'shear_y' in self.dialog.content_cls.ids.keys():
					self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.shear_y)
				if 'shear_z' in self.dialog.content_cls.ids.keys():
					self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.shear_z)
			else:
				if 'parameter_l' in self.dialog.content_cls.ids.keys():
					self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.parameter_l)
				if 'parameter_s' in self.dialog.content_cls.ids.keys():
					self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.parameter_s)
				if 'relative' in self.dialog.content_cls.ids.keys():
					self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.relative)
			self.dialog.open()
			
		elif trans=='Reflect':
			if not self.dialog:
				self.dialog = MDDialog(
					title=trans,
					type='custom',
					content_cls=ReflectContent(),
					buttons=[
						MDFlatButton(
							text="CANCEL",
							on_release=self.dialog_close
							),
						MDRaisedButton(
							text="ACCEPT",
							theme_text_color="Custom",
							text_color=[1,1,1,1],
							on_release=self.add_reflect
							)
						], )
						
				menu_axis = [
					{
						'viewclass': 'OneLineListItem',
						'text': 'X',
						'height': dp(56),
						'on_release': lambda x='X': self.reflect_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Y',
						'height': dp(56),
						'on_release': lambda x='Y': self.reflect_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Origin',
						'height': dp(56),
						'on_release': lambda x='Origin': self.reflect_changed(x)
					},
										{
						'viewclass': 'OneLineListItem',
						'text': 'Line',
						'height': dp(56),
						'on_release': lambda x='Line': self.reflect_changed(x)
					},
					]
				self.axis_direction = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.reflect_axis,
					items=menu_axis,
					position='bottom',
					width_mult=4)
					
				menu_ref = [
					{
						'viewclass': 'OneLineListItem',
						'text': 'X',
						'height': dp(56),
						'on_release': lambda x='X': self.ref_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'Y',
						'height': dp(40),
						'on_release': lambda x='Y': self.ref_changed(x)
					},
					]
				self.line_ref = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.line_ref,
					items=menu_ref,
					position='bottom',
					width_mult=4)
					
				menu_plane = [
					{
						'viewclass': 'OneLineListItem',
						'text': 'XY',
						'height': dp(56),
						'on_release': lambda x='XY': self.plane_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'XZ',
						'height': dp(56),
						'on_release': lambda x='XZ': self.plane_changed(x)
					},
					{
						'viewclass': 'OneLineListItem',
						'text': 'YZ',
						'height': dp(56),
						'on_release': lambda x='YZ': self.plane_changed(x)
					},
					]
				self.plane_direction = MDDropdownMenu(
					caller=self.dialog.content_cls.ids.reflect_plane,
					items=menu_plane,
					position='bottom',
					width_mult=4)
			if MDApp.get_running_app().d_type=='2D':
				self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.reflect_plane)
			else:
				self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.reflect_axis)
				self.dialog.content_cls.remove_widget(self.dialog.content_cls.ids.line_ref)
			self.dialog.open()
					
	def add_reflect(self, instance):
		app = MDApp.get_running_app()
		hid = self.dialog.content_cls.ids
		d_type = app.d_type
		
		if d_type=='2D':
			axis = hid.reflect_axis.text
			if axis=='Line':
				line = hid.line_ref.text
				R = app.transformer.reflect(d_type, axis, line)
				app.transformed_list.append(R)
				self.ids.container.add_widget(
					TwoLineAvatarIconListItem(
					text=self.last,
					secondary_text=f"Axis: {axis}  Line reference: {line}"
					))
				self.dialog.dismiss()
				self.dialog = None
			else:
				R = app.transformer.reflect(d_type, axis)
				app.transformed_list.append(R)
				self.ids.container.add_widget(
					TwoLineAvatarIconListItem(
					text=self.last,
					secondary_text=f"Axis: {axis}"
					))
				self.dialog.dismiss()
				self.dialog = None
		elif d_type=='3D':
			plane = hid.reflect_plane.text
			R = app.transformer.reflect(d_type, plane)
			app.transformed_list.append(R)
			self.ids.container.add_widget(
				TwoLineAvatarIconListItem(
				text=self.last,
				secondary_text=f"Axis: {self.dialog.content_cls.ids.reflect_axis.text}  Plane: {self.dialog.content_cls.ids.reflect_plane.text}"
				))
			self.dialog.dismiss()
			self.dialog = None
			
	def add_shear(self, instance):
		app = MDApp.get_running_app()
		hid = self.dialog.content_cls.ids
		d_type = app.d_type
		axis = hid.shear_direction.text
		if d_type=='2D':
			sh = hid.parameter_s.text
			if sh == '':
				hid.parameter_s.required=True
			else:
				rel = hid.relative.text
				if rel=='Yes':
					rel_para = hid.parameter_l.text
					S = app.transformer.shear(d_type, axis, sh, rel, rel_para)
				else:
					S = app.transformer.shear(d_type, axis, sh, rel)
				app.transformed_list.append(S)
				self.ids.container.add_widget(
						TwoLineAvatarIconListItem(
						text=self.last,
						secondary_text=f"Direction:{self.dialog.content_cls.ids.shear_direction.text}  Shear parameter: {sh}"
						))
				self.dialog.dismiss()
				self.dialog = None
		elif d_type=='3D':
			if axis=='X':
				shear_y = hid.shear_y.text
				shear_z = hid.shear_z.text
				if shear_y!='' and shear_z!='':
					S = app.transformer.shear(d_type, axis, shear_y, shear_z)
					app.transformed_list.append(S)
					self.ids.container.add_widget(
							TwoLineAvatarIconListItem(
							text=self.last,
							secondary_text=f"Direction:{self.dialog.content_cls.ids.shear_direction.text}  Shear_y: {shear_y}  Shear_z: {shear_z}"
							))
					self.dialog.dismiss()
					self.dialog = None
					
				else:
					if shear_y=='':
						hid.shear_y.error=True
					if shear_z=='':
						hid.shear_z.error=True
			elif axis=='Y':
				shear_x = hid.shear_x.text
				shear_z = hid.shear_z.text
				if shear_x!='' and shear_z!='':
					S = app.transformer.shear(d_type, axis, shear_x, shear_z)
					app.transformed_list.append(S)
					self.ids.container.add_widget(
							TwoLineAvatarIconListItem(
							text=self.last,
							secondary_text=f"Direction:{self.dialog.content_cls.ids.shear_direction.text}  Shear_x: {shear_x}  Shear_z: {shear_z}"
							))
					self.dialog.dismiss()
					self.dialog = None
					
				else:
					if shear_x=='':
						hid.shear_x.error=True
					if shear_z=='':
						hid.shear_z.error=True
			elif axis=='Z':
				shear_x = hid.shear_x.text
				shear_y = hid.shear_y.text
				if shear_x!='' and shear_y!='':
					S = app.transformer.shear(d_type, axis, shear_x, shear_y)
					app.transformed_list.append(S)
					self.ids.container.add_widget(
							TwoLineAvatarIconListItem(
							text=self.last,
							secondary_text=f"Direction:{self.dialog.content_cls.ids.shear_direction.text}  Shear_x: {shear_x}  Shear_y: {shear_y}"))
					self.dialog.dismiss()
					self.dialog = None
					
				else:
					if shear_x=='':
						hid.shear_x.error=True
					if shear_y=='':
						hid.shear_y.error=True
		
			
	def add_scale(self, instance):
		app = MDApp.get_running_app()
		hid = self.dialog.content_cls.ids
		Sx = hid.Sx.text
		Sy = hid.Sy.text
		d_type = app.d_type
		if d_type=='2D':
			if Sx!='' and Sy!='':
				S = app.transformer.translate(d_type, Sx, Sy)
				app.transformed_list.append(S)
				self.ids.container.add_widget(
						TwoLineAvatarIconListItem(
						text=self.last,
						secondary_text=f"Sx: {Sx}  Sy: {Sy}"
						))
				self.dialog.dismiss()
				self.dialog = None
			else:
				if Sx=='':
					hid.Sx.error=True
				if Sy=='':
					hid.Sy.error=True
		else:
			Sz = hid.Sz.text
			if Sx!='' and Sy!='' and Sz!='':
				S = app.transformer.translate(d_type, Sx, Sy, Sz)
				app.transformed_list.append(S)
				self.ids.container.add_widget(
						TwoLineAvatarIconListItem(
						text=self.last,
						secondary_text=f"Sx: {Sx}  Sy: {Sy}  Sz: {Sz}"
						))
				self.dialog.dismiss()
				self.dialog = None
			else:
				if Sx=='':
					hid.Sx.error=True
				if Sy=='':
					hid.Sy.error=True
				if Sz=='':
					hid.Sz.error=True
		
			
	def add_rotate(self, instance):
		app = MDApp.get_running_app()
		d_type = app.d_type
		hid = self.dialog.content_cls.ids
		angle = hid.angle.text
		direction = hid.direction.text
		if angle!='':
			if d_type=='2D':
				axis2 = hid.axis2.text
				O = app.transformer.rotate(d_type, angle, direction)
				if axis2=='Point':
					P1 = hid.points1.text
					P2 = hid.points2.text
					T1 = app.transformer.translate(d_type, P1, P2)
					T2 = app.transformer.translate(d_type, -float(P1), -float(P2))
					O = np.dot(T1, O)
					O = np.dot(O, T2)
				app.transformed_list.append(O)
				self.ids.container.add_widget(
						TwoLineAvatarIconListItem(
						text=self.last,
						secondary_text=f"Angle: {angle}  Dir: {direction}  Rotate: {axis2}"
						))
				self.dialog.dismiss()
				self.dialog = None
			else:
				axis3 = hid.axis3.text
				O = app.transformer.rotate(d_type, angle, direction, axis3)
				app.transformed_list.append(O)
				self.ids.container.add_widget(
						TwoLineAvatarIconListItem(
						text=self.last,
						secondary_text=f"Angle: {angle}  Dir: {direction}  Axis: {axis3}"
						))
				self.dialog.dismiss()
				self.dialog = None
		else:
			hid.angle.error=True

	def add_translate(self, instance):
		app = MDApp.get_running_app()
		hid = self.dialog.content_cls.ids
		Tx = hid.Tx.text
		Ty = hid.Ty.text
		d_type = app.d_type
		if d_type=='2D':
			if Tx!='' and Ty!='':
				T = app.transformer.translate(d_type, Tx, Ty)
				app.transformed_list.append(T)
				self.ids.container.add_widget(
						TwoLineAvatarIconListItem(
						text=self.last,
						secondary_text=f"Tx: {Tx}  Ty: {Ty}"
						))
				self.dialog.dismiss()
				self.dialog = None
			else:
				if Tx=='':
					hid.Tx.error=True
				if Ty=='':
					hid.Ty.error=True
		else:
			Tz = hid.Tz.text
			if Tx!='' and Ty!='' and Tz!='':
				T = app.transformer.translate(d_type, Tx, Ty, Tz)
				app.transformed_list.append(T)
				self.ids.container.add_widget(
						TwoLineAvatarIconListItem(
						text=self.last,
						secondary_text=f"Tx: {Tx}  Ty: {Ty}  Tz: {Tz}"
						))
				self.dialog.dismiss()
				self.dialog = None
			else:
				if Tx=='':
					hid.Tx.error=True
				if Ty=='':
					hid.Ty.error=True
				if Tz=='':
					hid.Tz.error=True
	def remove(self, instance):
		self.ids.container.remove_widget(instance )
		
	def reset(self):
		if len(self.ids.container.children)>0:
			self.dialog = MDDialog(
				title="Clear data?", 
				text="This will clear all [b]data[/b] in transformation list",
				buttons=[
					MDFlatButton(
						text="CANCEL",
						on_release=self.dialog_close
						),
					MDRaisedButton(
						text="ACCEPT",
						theme_text_color="Custom",
						text_color=[1,1,1,1],
						on_release=self.clear
						)
					], 
				)
			self.dialog.open()
		else:
			CustomSnackbar(
				text='Nothing to clear.',
				icon = 'information',
				font_size=dp(12),
				size_hint= [0.9, 0.01],
				pos_hint= {'center_x':0.5, 'center_y':0.1},
				radius= [8,8,8,8],
				).open()
				
	def dialog_close(self, instance):
		self.dialog.dismiss()
		self.dialog = None
				
	def clear(self, instance):
		self.ids.container.clear_widgets()
		CustomSnackbar(
				text='Table data cleared!.',
				icon = 'information',
				font_size=dp(12),
				size_hint= [0.9, 0.01],
				pos_hint= {'center_x':0.5, 'center_y':0.1},
				radius= [8,8,8,8],
				).open()
		self.dialog.dismiss()
		self.dialog = None
		
	def done(self):
		self.manager.current = 'summary'


class CordScreen(MDScreen):
	custom_sheet = None
	data_tables = None
	dialog = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		menu_items = [
			{
				'viewclass': 'IconListItem',
				'icon': '',
				'text': '2D',
				'height': dp(56),
				'on_release': lambda x='2D': self.changed(x),
			},
			{
				'viewclass': 'IconListItem',
				'icon': '',
				'text': '3D',
				'height': dp(56),
				'on_release': lambda x='3D': self.changed(x)
			},
			]
		self.menu_type = MDDropdownMenu(
			caller=self.ids.mode2,
			items=menu_items,
			position='bottom',
			width_mult=4)
			
			
	def changed(self, text):
		self.ids.mode2.text = text
		self.ids.mode3.size_hint = [0.3625, 0.07] if text=='2D' else [0.2, 0.07]
		self.ids.mode4.size_hint = [0.3625, 0.07] if text=='2D' else [0.2, 0.07]
		self.ids.left4.pos_hint = {'x': 0.5125} if text=='2D' else {'x': 0.345}
		self.ids.left5.opacity=0 if text=='2D' else 1
		self.ids.mode5.opacity=0 if text=='2D' else 1
		self.ids.mode5.disabled=True if text=='2D' else False
		self.ids.back5.opacity=0 if text=='2D' else 1
		self.ids.icon5.opacity=0 if text=='2D' else 1
		self.menu_type.dismiss()
		if self.data_tables:
			self.ids.layout.remove_widget(self.data_tables)
			self.data_tables = None
		MDApp.get_running_app().manager.get_screen('trans').ids.container.clear_widgets()
	
	def menu(self):
		self.custom_sheet = MDCustomBottomSheet(
			screen=Factory.ContentCustomSheet())
		self.custom_sheet.open()
		
	def add(self, *args):
		if self.data_tables:
			last_num_row = int(self.data_tables.row_data[-1][0])
			if self.ids.mode2.text=='2D' and args[0]!='' and args[1]!='':
				self.data_tables.add_row((last_num_row + 1, float(args[0]), float(args[1])))
			elif self.ids.mode2.text=='3D' and args[0]!='' and args[1]!='' and args[2]!='':
				self.data_tables.add_row((last_num_row + 1, float(args[0]), float(args[1]), float(args[2])))
		else:
			if self.ids.mode2.text=='2D' and args[0]!='' and args[1]!='':
				self.data_tables = MDDataTable(
					use_pagination=True,
					column_data=[('No.',dp(15)), ('X',dp(28)), ('Y', dp(28)),],
					row_data=[(1, float(args[0]), float(args[1])),],
					size_hint=(0.95, 0.38),
					pos_hint={'center_x': 0.5, 'top':0.48},)
				self.ids.layout.add_widget(self.data_tables)
			elif self.ids.mode2.text=='3D' and args[0]!='' and args[1]!='' and args[1]!='':
				self.data_tables = MDDataTable(
					use_pagination=True,
					column_data=[('No.',dp(10)), ('X',dp(20)), ('Y', dp(20)),('Z', dp(20)),],
					row_data=[(1, float(args[0]), float(args[1]), float(args[2])),],
					size_hint=(0.95, 0.38),
					pos_hint={'center_x': 0.5, 'top':0.48},)
				self.ids.layout.add_widget(self.data_tables)
		self.ids.mode3.text=''
		self.ids.mode4.text=''
		self.ids.mode5.text=''
			
	def reset(self):
		if self.data_tables:
			self.dialog = MDDialog(
				title="Clear data?", 
				text="This will clear all table data and delete the table columns.",
				buttons=[
					MDFlatButton(
						text="CANCEL",
						on_release=self.dialog_close
						),
					MDRaisedButton(
						text="ACCEPT",
						theme_text_color="Custom",
						text_color=[1,1,1,1],
						on_release=self.clear
						)
					], 
				)
			self.dialog.open()
		else:
			CustomSnackbar(
				text='Nothing to clear.',
				icon = 'information',
				font_size=dp(12),
				size_hint= [0.9, 0.01],
				pos_hint= {'center_x':0.5, 'center_y':0.1},
				radius= [8,8,8,8],
				).open()
				
	def dialog_close(self, instance):
		self.dialog.dismiss()
				
	def clear(self, instance):
		self.ids.layout.remove_widget(self.data_tables)
		self.data_tables = None
		CustomSnackbar(
				text='Table data cleared!.',
				icon = 'information',
				font_size=dp(12),
				size_hint= [0.9, 0.01],
				pos_hint= {'center_x':0.5, 'center_y':0.1},
				radius= [8,8,8,8],
				).open()
		self.dialog.dismiss()
		self.ids.mode3.text=''
		self.ids.mode4.text=''
		self.ids.mode5.text=''
				
	def check(self):
		if self.data_tables:
			coordinates = [list(num[1:])+[1.0] for num in self.data_tables.row_data]
			coordinates = np.array(coordinates)
			MDApp.get_running_app().coordinates = coordinates
		self.manager.current = 'trans'


class TransformApp(MDApp):
	manager = None
	transformation_list = {}
	transformed_list = []
	coordinates = None
	d_type = '3D'
	transformer = Transform()
	icons = {
		'Rotate': 'rotate-orbit',
		'Translate': 'transition',
		'Reflect': 'reflect-horizontal',
		'Shear': 'skew-more',
		'Scale': 'checkbox-intermediate'
	}
	
	def build(self):
		self.theme_cls.material_style = 'M3'
		self.theme_cls.theme_style = 'Dark'
		self.theme_cls.primary_palette = "DeepOrange"
		self.theme_cls.primary_hue = "700"
		#self.theme_cls.accent_palette = "Teal"
		self.manager = ScreenManager(transition=FadeTransition())
		self.manager.add_widget(CordScreen(name='coord'))
		self.manager.add_widget(TransScreen(name='trans'))
		self.manager.add_widget(SummaryScreen(name='summary'))
		#self.manager.current = 'summary'
		return self.manager
		
	def switch(self, switch, value):
		if value:
			self.theme_cls.theme_style = 'Dark'
		else: 
			self.theme_cls.theme_style = 'Light'


if __name__ == '__main__':
	TransformApp().run()