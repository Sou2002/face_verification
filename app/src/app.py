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
        pass


if __name__ == '__main__':
    CamApp().run()