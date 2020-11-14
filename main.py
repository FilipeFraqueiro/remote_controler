from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import *

import socket
import time


class KeyBoardScreen(Screen):
	def __init__(self, **kwargs):
		super(KeyBoardScreen, self).__init__(**kwargs)

		self.vkb = VKeyboard()
		self.vkb.font_size = 70
		self.vkb.margin_hint =  [0, 0, 0, 0]
		self.vkb.rotate = False
		self.vkb.do_scale = False
		self.vkb.do_translation = False
		self.vkb.size = (Window.size[0], Window.size[1]-100)
		self.vkb.bind(on_key_up = self.on_key_down)

		self.bl = BoxLayout(orientation = "vertical")

		bl_1 = BoxLayout(orientation = "horizontal", size_hint_y = None, height = 100)
		
		self.ti_ip = TextInput(text = "192.168.1.10", multiline = False)
		self.ti_ip.bind(on_text_validate = self.ip_enter)
		bl_1.add_widget(self.ti_ip)
		
		self.bt_connnect = Button(text = "Connect")
		self.bt_connnect.bind(on_release = self.connect)
		bl_1.add_widget(self.bt_connnect)

		bt_mouse = Button(text = "Mouse")
		bt_mouse.bind(on_release = self.mouse)
		bl_1.add_widget(bt_mouse)

		self.bl.add_widget(bl_1)
		self.bl.add_widget(self.vkb)

		self.add_widget(self.bl)
	# 1
	# 2
	# 3
	def ip_enter(self, instance):
		App.get_running_app().mouse_screen.ti_ip.text = self.ti_ip.text
	# 1
	# 2
	# 3
	def connect(self, instance):
		App.get_running_app().connect(self.ti_ip.text)
	# 1
	# 2
	# 3
	def mouse(self, instance):
		self.manager.current = 'mouse_screen'
	# 1
	# 2
	# 3
	def on_key_down(self, *key):
		# print(key)
		# print(key[1])
		try:
			data = key[1].encode() 
			App.get_running_app().s.send(data)
			
		except:
			App.get_running_app().is_connected = False
				
			Popup(title = "Error!", size_hint = (None, None), size = (600, 300), content = Label(text = "Server Disconnected!")).open()
			
			App.get_running_app().keyboard_screen.bt_connnect.text = "Connect"
			
			App.get_running_app().mouse_screen.bt_connnect.text = "Connect"
			
			# print("Not connected!")
# 1
# 2
# 3
# 4
# 5
class MouseBoardScreen(Screen):
	def __init__(self, **kwargs):
		super(MouseBoardScreen, self).__init__(**kwargs)

		self.bl = BoxLayout(orientation = "vertical")

		bl_1 = BoxLayout(orientation = "horizontal", size_hint_y = None, height = 100)
		
		self.ti_ip = TextInput(text = "192.168.1.10", multiline = False)
		self.ti_ip.bind(on_text_validate = self.ip_enter)
		bl_1.add_widget(self.ti_ip)

		self.bt_connnect = Button(text = "Connect")
		self.bt_connnect.bind(on_release = self.connect)
		
		bl_1.add_widget(self.bt_connnect)

		bt_keyboard = Button(text = "Keyboard")
		bt_keyboard.bind(on_release = self.keyboard)
		bl_1.add_widget(bt_keyboard)

		mouse_area = MyPaintWidget()
		mouse_area.bind(minimum_height = mouse_area.setter('height'))
		mouse_area.bind(minimum_width = mouse_area.setter('width'))
		
		self.bl.add_widget(bl_1)
		self.bl.add_widget(mouse_area)

		self.add_widget(self.bl)
	# 1
	# 2
	# 3
	def ip_enter(self, instance):
		App.get_running_app().keyboard_screen.ti_ip.text = self.ti_ip.text
	# 1
	# 2
	# 3
	def connect(self, instance):
		App.get_running_app().connect(self.ti_ip.text)
	# 1
	# 2
	# 3
	def keyboard(self, instance):
		self.manager.current = 'keyboard_screen'
# 1
# 2
# 3
# 4
# 5
class MyPaintWidget(BoxLayout):
	def on_touch_up(self, touch):
		if touch.pos[0] < self.size[0] and touch.pos[1] < self.size[1]:
			# print(touch.pos)
			try:
				data = "touch"
				data = data.encode() 
				App.get_running_app().s.send(data)
				
			except:
				App.get_running_app().is_connected = False
				
				Popup(title = "Error!", size_hint = (None, None), size = (600, 300), content = Label(text = "Server Disconnected!")).open()
			
				App.get_running_app().keyboard_screen.bt_connnect.text = "Connect"
			
				App.get_running_app().mouse_screen.bt_connnect.text = "Connect"
				
				# print("Not connected!")
	# 1
	# 2
	# 3
	def on_touch_move(self, touch):
		if touch.pos[0] < self.size[0] and touch.pos[1] < self.size[1]:
			# sleep to avoid chocking
			time.sleep(0.1)
			
			try:
				data = str(round(touch.dx, 3)) + "," + str(round(touch.dy, 3)) + " move\n"
				
				data = data.encode() 
				
				App.get_running_app().s.send(data)
				
			except:
				App.get_running_app().is_connected = False

				Popup(title = "Error!", size_hint = (None, None), size = (600, 300), content = Label(text = "Server Disconnected!")).open()
			
				App.get_running_app().keyboard_screen.bt_connnect.text = "Connect"
			
				App.get_running_app().mouse_screen.bt_connnect.text = "Connect"
				
				# print("Not connected!")
# 1
# 2
# 3
# 4
# 5
class MainScreenApp(App):
	def build(self):
		Window.rotation = -90

		self.is_connected = False

		self.sm = ScreenManager()
		self.sm.transition.direction = 'left'

		self.keyboard_screen = KeyBoardScreen(name = 'keyboard_screen')
		self.sm.add_widget(self.keyboard_screen)

		self.mouse_screen = MouseBoardScreen(name = 'mouse_screen')
		self.sm.add_widget(self.mouse_screen)

		self.sm.current = 'keyboard_screen'
		
		return self.sm
	# 1
	# 2
	# 3
	def connect(self, ip):
		# ip = "192.168.1.253"
		
		port = 44444
		
		address = (ip, port)
		
		if self.is_connected == False:
			try:	
				self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				
				self.s.settimeout(2)
				
				self.s.connect(address)
				
				self.is_connected = True
				
				self.keyboard_screen.bt_connnect.text = "Disconnect"
				
				self.mouse_screen.bt_connnect.text = "Disconnect"
			
			except:
				self.is_connected = False
				
				Popup(title = "Error!", size_hint = (None, None), size = (600, 300), content = Label(text = "Failed to connect to server!")).open()
				
				# print("cant connect")
				
		elif self.is_connected == True:
			self.is_connected = False
			
			self.keyboard_screen.bt_connnect.text = "Connect"
			
			self.mouse_screen.bt_connnect.text = "Connect"
			
			self.s.close()
# 1
# 2
# 3
# 4
# 5
if __name__ == "__main__":
	MainScreenApp().run()