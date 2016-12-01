#!/usr/bin/python

# Python Libraries
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider

# Our Libraries
import ImageProcessor as ip

# Static variables
imageProcessor = ip.ImageProcessor()
chosenImage = Image(source='images/hand.jpg', pos=(500, 200), size=(200, 200))
drawingImage = Image(source='drawing.png', pos=(500, 200), size=(200, 200))

# Create the screen manager
sm = ScreenManager()

# Global variables
chosenFile = ''

# Constants
MAIN_SCREEN_ID = 'main_screen'
FILE_CHOOSER_SCREEN_ID = 'filechooser_screen'
IMAGE_SCREEN_ID = "image_screen"

# Settings
Config.set('graphics', 'width', '1360')
Config.set('graphics', 'height', '1024')


# Float Widget
class FloatWidget(FloatLayout):
    pass


# Float Widget
class BoxWidget(BoxLayout):
    pass


# Main app
class MainApp(App):
    # --- Define the both Layouts ---
    mainScreenLayout = BoxWidget(orientation='vertical', size=(1360, 640))
    fileChooserScreenLayout = FloatWidget(size=(1360, 640))
    imageScreenLayout = BoxWidget(orientation='horizontal', size=(1360, 640))

    # ------------

    # Build app
    def build(self):
        # --- Define the screens ---
        mainScreen = MainScreen(name=MAIN_SCREEN_ID)
        fileChooserScreen = FileChooserScreen(name=FILE_CHOOSER_SCREEN_ID)
        imageScreen = ImageScreen(name=IMAGE_SCREEN_ID)
        # ------------

        # --- Construct main Screen ---
        self.constructMainScreen(self.mainScreenLayout)
        # ------------

        # --- Construct file chooser Screen ---
        self.constructFileChooserScreen(self.fileChooserScreenLayout)
        # ------------

        # --- Construct image Screen ---
        self.constructImageScreen(self.imageScreenLayout)
        # ------------

        # --- Add layouts to screens ---
        mainScreen.add_widget(self.mainScreenLayout)
        fileChooserScreen.add_widget(self.fileChooserScreenLayout)
        imageScreen.add_widget(self.imageScreenLayout)

        # ------------

        # --- Add screens to screen manager ---
        sm.add_widget(mainScreen)
        sm.add_widget(fileChooserScreen)
        sm.add_widget(imageScreen)
        # ------------

        return sm

    # --- Constructs the main Screen
    def constructMainScreen(self, mainScreenLayout):
        changeToFileChooserButton = Button(text="Choose File",
                                           size_hint=(.5, 1))
        changeToFileChooserButton.bind(on_press=MainApp.changeToFileChooserScreen)
        mainScreenLayout.add_widget(changeToFileChooserButton)

        changeToImageScreenButton = Button(text="Show images",
                                           size_hint=(.5, 1))
        changeToImageScreenButton.bind(on_press=MainApp.changeToImageScreen)
        mainScreenLayout.add_widget(changeToImageScreenButton)

    # --- Constructs the file Chooser Screen Layout
    def constructFileChooserScreen(self, fileChooserScreenLayout):
        changeToMainButton = Button(text="Go back to main",
                                    size_hint=(.2, .1),
                                    pos_hint={'center_x': .5, 'center_y': 0.95})
        changeToMainButton.bind(on_press=MainApp.changeToMainScreen)
        fileChooserScreenLayout.add_widget(changeToMainButton)
        fileChooserWidget = FileChooserWidget()
        fileChooserScreenLayout.add_widget(fileChooserWidget)

    # --- Constructs the file Chooser Screen Layout
    def constructImageScreen(self, imageScreenLayout):
        buttonLayout = BoxLayout(orientation='vertical', size_hint=(.2, .2), pos_hint={'center_x': 0, 'center_y': 0.9})
        changeToMainButton = Button(text="Go back to main")
        changeToMainButton.bind(on_press=MainApp.changeToMainScreen)

        blurSlider = Slider(min=5,
                            max=155,
                            value=45,
                            step=10)
        blurSlider.bind(value=MainApp.onSliderValueChange)

        buttonLayout.add_widget(changeToMainButton)
        buttonLayout.add_widget(blurSlider)
        imageScreenLayout.add_widget(buttonLayout)
        imageScreenLayout.add_widget(chosenImage)
        imageScreenLayout.add_widget(drawingImage)

    # --- Change to file chooser screen
    def changeToFileChooserScreen(root):
        sm.current = FILE_CHOOSER_SCREEN_ID
        sm.transition.direction = 'left'

    # --- Change to image screen
    def changeToImageScreen(root):
        sm.current = IMAGE_SCREEN_ID
        sm.transition.direction = 'up'

    # --- Change to main screen
    def changeToMainScreen(root):
        sm.current = MAIN_SCREEN_ID
        sm.transition.direction = 'right'

    # --- Setting the slider value
    def onSliderValueChange(instance, value):
        imageProcessor.blurringLevel = int(value)
        renderCallback()


# --- Render callback
def renderCallback():
    ip.analyze(imageProcessor)
    MainApp.imageScreenLayout.remove_widget(drawingImage)
    drawingImage.reload()
    MainApp.imageScreenLayout.add_widget(drawingImage)
    print 'done'


# Declare screens
class FileChooserScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class ImageScreen(Screen):
    pass


Builder.load_string("""
<FileChooserWidget>:
    id: file_chooser_widget
    FileChooserIconView:
        id: filechooser
        pos_hint: {'center_y': .4}
        on_selection: file_chooser_widget.selected(filechooser.path, filechooser.selection)
""")


class FileChooserWidget(FloatLayout):
    def selected(self, path, filename):
        print filename
        if len(filename) > 0:
            chosenFile = os.path.join(path, filename[0])
            imageProcessor.fileName = chosenFile
            if chosenImage is not None:
                chosenImage.source = chosenFile
                chosenImage.reload()
            renderCallback()
            sm.current = MAIN_SCREEN_ID
            sm.transition.direction = 'right'


# Run app
fi = MainApp()
fi.run()
