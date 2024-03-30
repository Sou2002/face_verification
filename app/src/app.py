# kivy dependecies
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# kivy ux components
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label

# others kivy
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger

# others
import cv2
import tensorflow as tf
from layers import Dist
import os
import numpy as np

# AppLayout
class CamApp(App):
    def build(self):
        # Main Layout Components
        self.web_cam = Image(size_hint = (1, 0.8))
        self.button = Button(text = "Verify", size_hint = (1, 0.1))
        self.verification_label = Label(text = "Verification Uninitiated", size_hint = (1, 0.1))

        # Adding items to box layout
        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.web_cam)
        layout.add_widget(self.button)
        layout.add_widget(self.verification_label)

        # Setup webcam
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout
    
    # Update webcam feed continuously
    def update(self, *args):
        success, frame = self.capture.read()
        frame = frame[130:130+250, 150:150+250, :]

        # Flip horizontally and converting image to texture
        buf = cv2.flip(frame, 0).tostring()
        img_texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt = 'bgr')
        img_texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.web_cam.texture = img_texture

    # Need to preprocess the image before passing to the model
    def preprocess(file_path):
        # Read in image from file path
        byte_img = tf.io.read_file(file_path)

        # Load in the image
        img = tf.io.decode_jpeg(byte_img) 
        
        # Resizing
        img = tf.image.resize(img, (105, 105))
        
        # Scaling
        img = img / 255.0
        
        return img

if __name__ == '__main__':
    CamApp().run()