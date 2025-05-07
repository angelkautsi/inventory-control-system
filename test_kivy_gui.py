from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(selfself):
        return Label(text="kivy is working")

TestApp().run()