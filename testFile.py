import kivy.core.text
import cv2

from kivy.app import App
from kivy.base import EventLoop
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from threading import Thread
import linecache
from collections import deque
import sys,re
from os import path
from random import randint
from os.path import join
# import kivy.utils.get_color_from_hex as hex
from kivy.utils import get_color_from_hex
from kivy.config import  Config

import datetime
#GenderEmotion
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 100)
Config.set('graphics', 'top', 100)

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder

global sm
sm = ScreenManager()

Builder.load_string('''
<UIMain>:
    BoxLayout:
        id: uimain
        orientation: "vertical"
        BoxLayout:
            id: banner
            size_hint:1, .1
            orientation: "horizontal"
            # Image:
            #     id: deloitte_logo
            #     source: 'images/deloitte-logo-site-image' #deloitte-brand-logo-128x128.png'
            Image:
                source: 'images/deloitte-logo-site-image.png' #deloitte-brand-logo-128x128.png'
                allow_stretch: True
                keep_ratio: False
                size_hint: 0.1,1

                # width: self.parent.width
                # height: self.parent.width/self.image_ratio
            Label:
                id: banner_label
                text: '[color=FFFFFF]'+'Deloitte Beam v0.0.1'+'[/color]'
                markup: True
                color: 96,125,139,1
                #:import hex kivy.utils.get_color_from_hex
                canvas.before:
                    Color:
                        rgba: hex('#607D8B')
                    Rectangle:
                        pos: self.pos
                        size: self.size



        BoxLayout:
            id: box_one_vertical
            BoxLayout:
                id:box_one_sub_box
                orientation: "horizontal"

                BoxLayout:
                    id: box_one_sub_box_left
                    # Camera:
                    #     id:cam

                    KivyCamera:
                        id: qrcam
                        # width:self.parent.width
                        # height: self.parent.height


                BoxLayout:
                    id: box_one_sub_box_right
                    orientation: "vertical"

                    # BoxLayout:
                    #     size_hint: 1,0.2
                    #     Label:
                    #         text:'Frames Processed'
                    #     Label:
                    #         id:num_frames_processed
                    #         text:'0'
                    BoxLayout:
                        padding: 10,10,10,10
                        size_hint: 1,0.1
                        Spinner:
                            text:'Gender/Emotion'
                            values: {'Gender/Emotion[Default]','Heartrate Monitor[upcoming]','Eye Blink Rate[upcoming]','Driver Alertness[upcoming]'}
                    BoxLayout:
                        size_hint:1,0.5
                        id:img_box
                        orientation:"horizontal"

                        BoxLayout:
                            id: emotion_box
                            padding:10,10,10,10
                            orientation:"vertical"
                            Label:
                                id: lbl_emotion
                                size_hint: 1,0.1
                                text:'Hello, World'

                            Carousel:
                                id: carousel_emotion
                                Label:
                                    Image:
                                        id:img_happy
                                        center:self.parent.center
                                        source: 'images/emotion/happy/4/happy_4_128.png'
                                Label:
                                    Image:
                                        id:img_neutral
                                        center:self.parent.center
                                        source: 'images/emotion/neutral/1/neutral_1_128.png'
                                Label:
                                    Image:
                                        id:img_angry
                                        center:self.parent.center
                                        source: 'images/emotion/angry/1/angry_1_128.png'
                                Label:
                                    Image:
                                        id:img_thinking
                                        center:self.parent.center
                                        source: 'images/emotion/thinking/2/thinking_2_128.png'


                        BoxLayout:
                            id: gender_box
                            padding:10,10,10,10
                            orientation:"vertical"
                            Label:
                                id: lbl_gender
                                size_hint: 1,0.1
                                text: 'Hello,World'
                            Carousel:
                                id:carousel_gender
                                Label:
                                    orientation:"vertical"
                                    Image:
                                        id:img_male
                                        center:self.parent.center
                                        source: 'images/gender/male/active/male_active_128.png'
                                        allow_stretch: True
                                        keep_ratio: False


                                Label:
                                    #:import hex kivy.utils.get_color_from_hex
                                    Image:
                                        id:img_female
                                        center:self.parent.center
                                        source: 'images/gender/female/active/female_active_128.png'
                                        allow_stretch: True
                                        keep_ratio: False
                                Label:
                                    Image:
                                        id:img_undecided
                                        center:self.parent.center
                                        source: 'images/gender/undecided/active/undecided_active_128.png'
                                        allow_stretch: True
                                        keep_ratio: False



                    BoxLayout:
                        orientation: "horizontal"
                        size_hint:1,0.3
                        padding:10,10,10,10
                        Label:
                            size_hint: 0.2,1
                            text: 'Threshold'
                        Slider:
                            id: accuracy_slider
                            size_hint: 0.7,1
                            step:10
                            min:0
                            max:100
                            value:60
                            value_track: True
                            value_track_color: hex('#CDDC39')
                            on_value: root.update_threshold(self.value)

                        Label:
                            size_hint: 0.1,1
                            text: '{}'.format(accuracy_slider.value)


        BoxLayout:
            id: buttons_box
            orientation: "horizontal"
            size_hint:1,0.1
            padding:10,0,10,10
            # Spinner:
            #     text:'Gender/Emotion'
            #     size_hint: 0.3,1
            #     values: {'Gender/Emotion[Default]','Heartrate Monitor[upcoming]','Eye Blink Rate[upcoming]','Driver Alertness[upcoming]'}
            Button:
                id: butt_start
                size_hint: 0.3,1
                text: "Start"
                on_press: root.dostart()
            Button:
                id: butt_gender
                text: "Detect"
                size_hint: 0.3,1
                #on_press: root.captureFrames()
                on_press: root.detectgender()
            Button:
                id: butt_exit
                text: "Stop"
                size_hint: 0.3,1
                on_press: root.doexit()

        BoxLayout:
            id:status_box
            size_hint:1,0.4
            padding:10,0,10,5
            ScrollView:
                id:runstatlabelscroll
                effect_cls:'ScrollEffect'

                Label:
                    id:runstatlabel
                    halign:'left'
                    valign:'top'
                    padding_x:3
                    padding_y:3
                    text:'Deloitte Beam \\nBeam me up :D\\nversion: 0.0.1\\nDate of Publication: 13 September 2017\\n © Copyrights with Deloitte USI. All rights reserved.'
                    markup: True
                    size_hint:None,None
                    canvas.before:
                        Color:
                            #rgba:0.6,0.16,0.16,1
                            rgba:0,0,0,1
                        Rectangle:
                            pos:self.pos
                            size:self.size
''')
global frameList
global uiThread
global uiActive
global genderDetectThread
global genderDetectActive
global genderEmotionObj
global captureActive
global prediction_threshold

frameList=deque()
uiThread=Thread()
uiActive = False
genderDetectThread = Thread()
genderDetectActive = False
captureActive = False
prediction_threshold=0.6
errormsg='ERROR  '
logmsg='LOG    '
warnmsg='WARNING'

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    # logdisplay('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj),errormsg)

    return





class KivyCamera(Image):

    global frameList
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

            if(len(frameList)<1):# and captureActive):
                frameList.append(frame)
                # self.framesDetected+=1
                # if(self.framesDetected==10):
                #     captureActive=False
                #     # self.framesDetected=0

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




class UIMain(Screen):
    global genderDetectThread
    global hrdetectThread
    ge_tf = object
    d_images_emotion={}
    lbl_emotion =''
    lbl_gender =''
    car_emotion=object
    car_gender=object
    runstatlabel=object
    runstatlabelscroll = object
    idx_happy=0
    idx_neutral=1
    idx_angry=2
    idx_thinking=3

    idx_male = 0
    idx_female=1
    idx_undecided=2
    def __init__(self,**kwargs):
        super(UIMain, self).__init__(**kwargs)
        self.lbl_emotion = self.ids['lbl_emotion'] #['lbl_emotion']
        self.lbl_gender = self.ids['lbl_gender'] #['lbl_gender']
        self.car_emotion=self.ids['carousel_emotion']
        self.car_emotion.index=self.idx_thinking
        self.car_gender = self.ids['carousel_gender']
        self.car_gender.index=self.idx_undecided
        self.runstatlabel = self.ids['runstatlabel']
        self.runstatlabelscroll = self.ids['runstatlabelscroll']
        self.runstatlabel.bind(texture_size=self.runstatlabel.setter('size'))
        # self.dostart()
        #self.loadImages()
        # self.ge_tf = GenderEmotion()

    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

        self.logdisplay('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj),errormsg)

        return
    def getRand(self,max):
        return str(randint(1,max))

    def update_threshold(self,val):
        global prediction_threshold
        prediction_threshold=val/100


    def dostart(self, *largs):
        global capture
        #global genderDetectThread
        #self.update_emotion('Emotion')
        #self.update_gender('Gender')
        capture = cv2.VideoCapture(0)
        self.ids.qrcam.start(capture)
        #genderDetectThread = True


    def doexit(self):
        #global genderDetectThread
        global capture
        global frameList
        #setInitSetup(False)
        if capture != None:
            capture.release()
            capture = None

        self.ids.qrcam.stop()
        genderDetectThread = False
        frameList=deque()
        self.logdisplay('All running threads are being killed..',warnmsg)




    def captureFrames(self):
        global captureActive
        captureActive = True


    def logdisplay(self, strin, msgtype):
        if msgtype == errormsg:
            colorstart = '[color=FF0000]'
            colorend = '[/color]'
        elif msgtype == warnmsg:
            colorstart = '[color=629632]'
            colorend = '[/color]'
        else:
            colorstart = '[color=40E0D0]'
            colorend = '[/color]'

        nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        displaystr = '\n' + colorstart + nowtime + '    ' + msgtype + '    ' + str(strin) + colorend
        # print displaystr
        self.runstatlabel.text = self.runstatlabel.text + displaystr
        self.runstatlabelscroll.scroll_x = 0
        self.runstatlabelscroll.scroll_y = 0
        self.runstatlabelscroll.effect_x.value = self.runstatlabelscroll.effect_x.max
        self.runstatlabelscroll.effect_y.value = self.runstatlabelscroll.effect_y.max


#create the screen manager

sm.add_widget(UIMain(name='mainWindow'))


class BeamApp(App):
    icon = 'images\\BeamIcon.png'
    title = 'Beam'
    file_path = ''
    file_name = ''

    def build(self):
        config = self.config
        Window.clearcolor = kivy.utils.get_color_from_hex("#455A64")#(.4,.4,.4,1)
        return sm

    def on_stop(self):
        global capture
        if capture:
            capture.release()
            capture = None



if __name__=='__main__':
    BeamApp().run()

