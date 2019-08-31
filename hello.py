import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        return MyGrid()

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1 # columns in main layout

        self.inside = GridLayout()
        self.inside.cols = 2 #cols in new grid, below new layout

        self.inside.add_widget(Label(text="Enter the DNA sequence:", font_size="20sp"))
        self.DNA = TextInput(font_size="20sp")
        self.inside.add_widget(self.DNA)

        self.add_widget(self.inside)
        self.submit = Button(text="Submit", font_size="25sp")
        self.add_widget(self.submit)

if __name__ == "__main__":
    MyApp().run()
