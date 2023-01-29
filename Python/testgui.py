import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

Window.clearcolor = (0, 0.6, 0.1, 1.0)
Window.size = (600, 400)

class MyApp(App):
    def build(self):
        return Label(text="tech with tim")


if __name__ == "__main__":
    MyApp().run()