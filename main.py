#!/usr/bin/python

# Python Libraries
import os
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.config import Config

# Our Libraries
import ImageProcessor as ip

# Static variables
imageProcessor = ip.ImageProcessor()

# Settings
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '640')

# Root Widget
class RootWidget(FloatLayout):
    pass

# Main app
class MainApp(App):

    # Build app
    def build(self):
        root = RootWidget(size=(1024, 640))
        btn1 = Button(text="Load image",
                      size_hint=(.1, .1),
                      pos=(10, 540))
        btn1.bind(on_press=MainApp.addImageCallback)
        root.add_widget(btn1, root)

        Clock.schedule_interval(renderCallback, 0.1)

        return root

    # Add image call back - button action
    def addImageCallback(root):
        # here will be extracted the filename 
        root.add_widget(AsyncImage(source='drawing.png',
                                   pos=(500, 200),
                                   size=(200, 200)))

# Render callback
def renderCallback(dt):
    ip.analyze(imageProcessor)

# Run app
fi = MainApp()
fi.run()
