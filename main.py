#!/usr/bin/python

# Python Libraries
import os
import cv2
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
from kivy.clock import Clock
from kivy.graphics.texture import Texture

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
                                    pos_hint={'center_x': .5, 'center_y': 0.95})
        changeToMainButton.bind(on_press=MainApp.changeToMainScreenFromVideo)
        videoScreenLayout.add_widget(changeToMainButton)

        self.img1 = Image(source='images/1.jpg')
        videoScreenLayout.add_widget(self.img1)
        # opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        #self.capture = cv2.VideoCapture("test.mp4")
        self.handTrackingSystem = ht.HandTracking()

        ret, frame = self.capture.read()
        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        result = self.handTrackingSystem.imageProcessing(frame)
        self.handTrackingSystem.actionMouse()
        self.handTrackingSystem.updateMousePosition()
        try:
            buf = result.tostring()
        except:
            buf = frame.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1
        # def CreateImage(self, (height, width), bits=np.uint8, channels=3, color=(0, 0, 0)): # (cv.GetSize(frame), 8, 3)
        #     """Create new image(numpy array) filled with certain color in RGB"""
        #     # Create black blank image
        #     if bits == 8:
        #         bits = np.uint8
        #     elif bits == 32:
        #         bits = np.float32
        #     elif bits == 64:
        #         bits = np.float64
        #     image = np.zeros((height, width, channels), bits)
        #     if color != (0, 0, 0):
        #         # Fill image with color
        #         image[:] = color
        #     return image


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

    # --- Change to main screen from viedeo
    def changeToMainScreenFromVideo(root):
        sm.current = MAIN_SCREEN_ID
        sm.transition.direction = 'left'

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
fi.run()
