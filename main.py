import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MyGrid(Widget):
    sequence = ObjectProperty(None)

    def btn(self):
        print("sequence: ", self.sequence.text)

class MyApp(App): # <- Main Class
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()