#!/usr/bin/python

# Python Libraries
import os
import pickle
import multiprocessing
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox

# Our Libraries
import ImageProcessor as ip
import HandTracking as ht

# Static variables
imageProcessor = ip.ImageProcessor()
chosenImage = Image(source='images/hand.jpg', pos=(500, 200), size=(200, 200))
drawingImage = Image(source='drawing.png', pos=(500, 200), size=(200, 200))
widthCropSlider = Slider(min=10, max=(chosenImage._coreimage._size[0] / 100 * 90),
                         value=(chosenImage._coreimage._size[0] / 100 * 90), steps=1)
heightCropSlider = Slider(min=10, max=(chosenImage._coreimage._size[1] / 100 * 90),
                          value=(chosenImage._coreimage._size[1] / 100 * 90), steps=1)
xCropSlider = Slider(min=0, max=(chosenImage._coreimage._size[0]), value=0, steps=1)
yCropSlider = Slider(min=0, max=(chosenImage._coreimage._size[1]), value=0, steps=1)
amountOfFingersLabel = Label(text='')
Settings = pickle.load(open(".config", "r"))

# Create the screen manager
sm = ScreenManager()

# Global variables
chosenFile = ''

# Constants
MAIN_SCREEN_ID = 'main_screen'
FILE_CHOOSER_SCREEN_ID = 'filechooser_screen'
IMAGE_SCREEN_ID = "image_screen"
VIDEO_SCREEN_ID = "video_screen"

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
    videoScreenLayout = BoxWidget(orientation='horizontal', size=(1360, 640))

    # ------------

    # Build app
    def build(self):
        # --- Define the screens ---
        mainScreen = MainScreen(name=MAIN_SCREEN_ID)
        fileChooserScreen = FileChooserScreen(name=FILE_CHOOSER_SCREEN_ID)
        imageScreen = ImageScreen(name=IMAGE_SCREEN_ID)
        videoScreen = VideoScreen(name=VIDEO_SCREEN_ID)
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

        # --- Construct video Screen ---
        self.constructVideoScreen(self.videoScreenLayout)
        # ------------

        # --- Add layouts to screens ---
        mainScreen.add_widget(self.mainScreenLayout)
        fileChooserScreen.add_widget(self.fileChooserScreenLayout)
        imageScreen.add_widget(self.imageScreenLayout)
        videoScreen.add_widget(self.videoScreenLayout)

        # ------------

        # --- Add screens to screen manager ---
        sm.add_widget(mainScreen)
        sm.add_widget(fileChooserScreen)
        sm.add_widget(imageScreen)
        sm.add_widget(videoScreen)
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

        changeToVideoScreenButton = Button(text="Show Video",
                                           size_hint=(.5, 1))
        changeToVideoScreenButton.bind(on_press=MainApp.changeToVideoScreen)
        mainScreenLayout.add_widget(changeToVideoScreenButton)

    # --- Constructs the file Chooser Screen Layout
    def constructFileChooserScreen(self, fileChooserScreenLayout):
        changeToMainButton = Button(text="Go back to main",
                                    size_hint=(.2, .1),
                                    pos_hint={'center_x': .5, 'center_y': 0.95})
        changeToMainButton.bind(on_press=MainApp.changeToMainScreenFromFileChooser)
        fileChooserScreenLayout.add_widget(changeToMainButton)
        fileChooserWidget = FileChooserWidget()
        fileChooserScreenLayout.add_widget(fileChooserWidget)

    # --- Constructs the file Chooser Screen Layout
    def constructImageScreen(self, imageScreenLayout):
        buttonLayout = BoxLayout(orientation='vertical', size_hint=(.4, .6),
                                 pos_hint={'center_x': 0.1, 'center_y': 0.7})
        changeToMainButton = Button(text="Go back to main")
        changeToMainButton.bind(on_press=MainApp.changeToMainScreenFromImage)
        blurSliderLabel = Label(text='blur slider')
        blurSlider = Slider(min=5,
                            max=155,
                            value=45,
                            step=10)
        blurSlider.bind(value=MainApp.onBlurSliderValueChange)

        xCropStartPositionLabel = Label(text='X: crop start position')
        xCropSlider.bind(value=MainApp.onXCropSliderValueChange)

        yCropStartPositionLabel = Label(text='Y: crop start position')
        yCropSlider.bind(value=MainApp.onYCropSliderValueChange)

        widthCropLabel = Label(text='Width crop length')
        widthCropSlider.bind(value=MainApp.onWidthCropSliderValueChange)

        heightCropLabel = Label(text='Height crop length')
        heightCropSlider.bind(value=MainApp.onHeightCropSliderValueChange)

        buttonLayout.add_widget(changeToMainButton)
        buttonLayout.add_widget(blurSliderLabel)
        buttonLayout.add_widget(blurSlider)

        buttonLayout.add_widget(xCropStartPositionLabel)
        buttonLayout.add_widget(xCropSlider)

        buttonLayout.add_widget(yCropStartPositionLabel)
        buttonLayout.add_widget(yCropSlider)

        buttonLayout.add_widget(widthCropLabel)
        buttonLayout.add_widget(widthCropSlider)

        buttonLayout.add_widget(heightCropLabel)
        buttonLayout.add_widget(heightCropSlider)

        buttonLayout.add_widget(amountOfFingersLabel)

        imageScreenLayout.add_widget(buttonLayout)
        ip.analyze(imageProcessor)
        chosenImage.reload()
        drawingImage.reload()
        imageScreenLayout.add_widget(chosenImage)
        imageScreenLayout.add_widget(drawingImage)

    # --- Constructs the Video Screen Layout
    def constructVideoScreen(self, videoScreenLayout):
        changeToMainButton = Button(text="Go back to main",
                                    size_hint=(.2, .1),
                                    pos_hint={'center_x': .5, 'center_y': 0.7})
        changeToMainButton.bind(on_press=MainApp.changeToMainScreenFromVideo)

        firstButtonLayout = BoxLayout(orientation='vertical', size_hint=(.4, .6),
                                      pos_hint={'center_x': 0.1, 'center_y': 0.6})

        secondButtonLayout = BoxLayout(orientation='vertical', size_hint=(.4, .6),
                                       pos_hint={'center_x': 0.1, 'center_y': 0.6})

        blurSliderLabel = Label(text='blur slider')
        blurSlider = Slider(min=0,
                            max=255,
                            value=Settings["blur"],
                            step=1)
        blurSlider.bind(value=MainApp.onVideoBlurSliderValueChange)

        firstButtonLayout.add_widget(changeToMainButton)

        firstButtonLayout.add_widget(blurSliderLabel)
        firstButtonLayout.add_widget(blurSlider)

        erodeSliderLabel = Label(text='erode slider')
        erodeSlider = Slider(min=0,
                             max=255,
                             value=0,
                             step=1)
        erodeSlider.bind(value=MainApp.onVideoErodeSliderValueChange)

        firstButtonLayout.add_widget(erodeSliderLabel)
        firstButtonLayout.add_widget(erodeSlider)

        dilateSliderLabel = Label(text='dilate slider')
        dilateSlider = Slider(min=0,
                              max=255,
                              value=0,
                              step=1)
        dilateSlider.bind(value=MainApp.onVideoDilateSliderValueChange)

        firstButtonLayout.add_widget(dilateSliderLabel)
        firstButtonLayout.add_widget(dilateSlider)

        spinner = Spinner(
            # default value shown
            text='Choose color',
            # available values
            values=('Skin', 'Red', 'Orange', 'Black'),
            # just for positioning in our example
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5})

        def changeHSVToGivenText(spinner, text):
            if text == "Skin":
                writeHSVToSettings(20, 255, 255, 0, 48, 80)
            if text == "Red":
                writeHSVToSettings(10, 255, 255, 0, 50, 50)
            if text == "Orange":
                writeHSVToSettings(15, 255, 255, 5, 50, 50)
            if text == "Black":
                writeHSVToSettings(180, 255, 35, 0, 0, 0)

        def writeHSVToSettings(u, ups, upv, l, ds, dv):
            Settings["upper"] = u
            pickle.dump(Settings, open(".config", "w"))
            Settings["filterUpS"] = ups
            pickle.dump(Settings, open(".config", "w"))
            Settings["filterUpV"] = upv
            pickle.dump(Settings, open(".config", "w"))
            Settings["lower"] = l
            pickle.dump(Settings, open(".config", "w"))
            Settings["filterDownS"] = ds
            pickle.dump(Settings, open(".config", "w"))
            Settings["filterDownV"] = dv
            pickle.dump(Settings, open(".config", "w"))

        spinner.bind(text=changeHSVToGivenText)

        firstButtonLayout.add_widget(spinner)

        checkBoxLabel = Label(text='upper hue slider')
        checkBox = CheckBox()
        checkBox.bind(active=MainApp.onVideoMouseSwitchValueChange)

        firstButtonLayout.add_widget(checkBoxLabel)
        firstButtonLayout.add_widget(checkBox)


        upperHueSliderLabel = Label(text='upper hue slider')
        upperHueSlider = Slider(min=0,
                                max=255,
                                value=Settings["upper"],
                                step=1)
        upperHueSlider.bind(value=MainApp.onVideoUpperHueChange)
        secondButtonLayout.add_widget(upperHueSliderLabel)
        secondButtonLayout.add_widget(upperHueSlider)

        upperSaturationSliderLabel = Label(text='upper saturation slider')
        upperSaturationSlider = Slider(min=0,
                                       max=255,
                                       value=Settings["filterUpS"],
                                       step=1)
        upperSaturationSlider.bind(value=MainApp.onVideoUpperSaturationChange)
        secondButtonLayout.add_widget(upperSaturationSliderLabel)
        secondButtonLayout.add_widget(upperSaturationSlider)

        upperValueSliderLabel = Label(text='upper value slider')
        upperValueSlider = Slider(min=0,
                                  max=255,
                                  value=Settings["filterUpV"],
                                  step=1)
        upperValueSlider.bind(value=MainApp.onVideoUpperValueChange)
        secondButtonLayout.add_widget(upperValueSliderLabel)
        secondButtonLayout.add_widget(upperValueSlider)

        downHueSliderLabel = Label(text='down hue slider')
        downHueSlider = Slider(min=0,
                               max=255,
                               value=Settings["lower"],
                               step=1)
        downHueSlider.bind(value=MainApp.onVideoDownHueChange)
        secondButtonLayout.add_widget(downHueSliderLabel)
        secondButtonLayout.add_widget(downHueSlider)

        downSaturationSliderLabel = Label(text='down saturation slider')
        downSaturationSlider = Slider(min=0,
                                      max=255,
                                      value=Settings["filterDownS"],
                                      step=1)
        downSaturationSlider.bind(value=MainApp.onVideoDownSaturationChange)
        secondButtonLayout.add_widget(downSaturationSliderLabel)
        secondButtonLayout.add_widget(downSaturationSlider)

        downValueSliderLabel = Label(text='down value slider')
        downValueSlider = Slider(min=0,
                                 max=255,
                                 value=Settings["filterDownV"],
                                 step=1)
        downValueSlider.bind(value=MainApp.onVideoDownValueChange)
        secondButtonLayout.add_widget(downValueSliderLabel)
        secondButtonLayout.add_widget(downValueSlider)


        videoScreenLayout.add_widget(firstButtonLayout)
        videoScreenLayout.add_widget(secondButtonLayout)

    # --- Change to file chooser screen
    def changeToFileChooserScreen(root):
        sm.current = FILE_CHOOSER_SCREEN_ID
        sm.transition.direction = 'left'

    # --- Change to image screen
    def changeToImageScreen(root):
        sm.current = IMAGE_SCREEN_ID
        sm.transition.direction = 'up'

    # --- Change to image screen
    def changeToVideoScreen(root):
        sm.current = VIDEO_SCREEN_ID
        sm.transition.direction = 'right'
        os.system("python HandTracking.py &")

    # --- Change to main screen from viedeo
    def changeToMainScreenFromVideo(root):
        sm.current = MAIN_SCREEN_ID
        sm.transition.direction = 'left'
        os.system("pkill -9 -f HandTracking.py")

    # --- Change to main screen from file chooser
    def changeToMainScreenFromFileChooser(root):
        sm.current = MAIN_SCREEN_ID
        sm.transition.direction = 'right'

    # --- Change to main screen from file chooser
    def changeToMainScreenFromImage(root):
        sm.current = MAIN_SCREEN_ID
        sm.transition.direction = 'down'

    # --- Setting the blur slider value
    def onBlurSliderValueChange(instance, value):
        imageProcessor.blurringLevel = int(value)
        renderCallback()

    # --- Setting the video blur slider value
    def onVideoBlurSliderValueChange(instance, value):
        Settings["blur"] = int(value) + 1
        pickle.dump(Settings, open(".config", "w"))

    def onVideoUpperSaturationChange(self, value):
        Settings["filterUpS"] = value
        pickle.dump(Settings, open(".config", "w"))

    # ----------------------------------------------------------------------
    def onVideoDownSaturationChange(self, value):
        Settings["filterDownS"] = value
        pickle.dump(Settings, open(".config", "w"))

    # ----------------------------------------------------------------------
    def onVideoUpperValueChange(self, value):
        Settings["filterUpV"] = value
        pickle.dump(Settings, open(".config", "w"))

    # ----------------------------------------------------------------------
    def onVideoDownValueChange(self, value):
        Settings["filterDownV"] = value
        pickle.dump(Settings, open(".config", "w"))

    # ----------------------------------------------------------------------
    def onVideoUpperHueChange(self, value):
        Settings["upper"] = value
        pickle.dump(Settings, open(".config", "w"))

    # ----------------------------------------------------------------------
    def onVideoDownHueChange(self, value):
        Settings["lower"] = value
        pickle.dump(Settings, open(".config", "w"))

    # ----------------------------------------------------------------------
    def onVideoErodeSliderValueChange(instance, value):
        Settings["erode"] = int(value) + 1
        pickle.dump(Settings, open(".config", "w"))

    # ----------------------------------------------------------------------
    def onVideoDilateSliderValueChange(instance, value):
        Settings["diilate"] = int(value) + 1
        pickle.dump(Settings, open(".config", "w"))

    def onVideoMouseSwitchValueChange(instance, value):
        Settings["mouseOff"] = bool(value)
        pickle.dump(Settings, open(".config", "w"))

    # --- Setting the x crop slider value
    def onXCropSliderValueChange(instance, value):
        imageProcessor._croopingX = int(value)
        widthCropSlider.max = (chosenImage._coreimage._size[0]) - int(value)
        renderCallback()

    # --- Setting the y crop slider value
    def onYCropSliderValueChange(instance, value):
        imageProcessor._croopingY = int(value)
        heightCropSlider.max = (chosenImage._coreimage._size[1]) - int(value)
        renderCallback()

    # --- Setting the width crop slider value- int(value)
    def onWidthCropSliderValueChange(instance, value):
        imageProcessor._croopingWidth = int(value)
        renderCallback()

    # --- Setting the height crop slider value
    def onHeightCropSliderValueChange(instance, value):
        imageProcessor._croopingHeight = int(value)
        renderCallback()


# --- Render callback
def renderCallback():
    ip.analyze(imageProcessor)
    amountOfFingersLabel.text = str(imageProcessor.numberOfFingers)
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


class VideoScreen(Screen):
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
p = multiprocessing.Process(target=fi.run())
p.start()
