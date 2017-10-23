
import cv2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture

class KivyCamera(Image):

    stopFlag = False
    global captureActive

    framesDetected=0

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=30):
        self.capture = capture
        self.stopFlag = False
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        global captureActive
        self.capture = None
        self.stopFlag = True
        #Clock.schedule_interval(self.update, 0.0)
        w,h=self.parent.width,self.parent.height
        self.texture = texture = Texture.create(size=(w, h))
        #texture.flip_vertical()
        #texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
        self.canvas.ask_update()
        captureActive=False
#        Clock.unschedule_interval(self.update)


    def update(self, dt):
        global captureActive
        if not self.stopFlag:
            return_value, frame = self.capture.read()

            if return_value:
                texture = self.texture
                w, h = frame.shape[1], frame.shape[0]
                #print (w,h)
                if not texture or texture.width != w or texture.height != h:
                    self.texture = texture = Texture.create(size=(w, h))
                    texture.flip_vertical()
                texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
                self.canvas.ask_update()
            else:
                self.capture=None

class MyDashboard(BoxLayout):
    pass

class MyDashboard(Screen):
    def __init__(self,**kwargs):
        super(MyDashboard, self).__init__(**kwargs)

    def dostart(self, *largs):
        global capture
        capture = cv2.VideoCapture(0)
        self.ids.qrcam.start(capture)


    def doexit(self):

        global capture
        if capture != None:
            capture.release()
            capture = None

        self.ids.qrcam.stop()


class DashboardApp(App):

    def build(self):
        return MyDashboard()

if __name__=="__main__":
    DashboardApp().run()


