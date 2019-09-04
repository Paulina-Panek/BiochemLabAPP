import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder


class MainWindow(Screen):
    sequence = ObjectProperty(None)

    def btn(self):
        print("sequence: ", self.sequence.text)   #reading in input for sequence

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App): # <- Main Class
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()