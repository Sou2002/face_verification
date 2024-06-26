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
        self.button = Button(text = "Verify", on_press = self.verify, size_hint = (1, 0.1))
        self.verification_label = Label(text = "Verification Uninitiated", size_hint = (1, 0.1))

        # Adding items to box layout
        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.web_cam)
        layout.add_widget(self.button)
        layout.add_widget(self.verification_label)

        # Loading Model
        self.model = siamese_model = tf.keras.models.load_model('../model/siamesemodel.keras', custom_objects = {'Dist': Dist})

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
    def preprocess(self, file_path):
        # Read in image from file path
        byte_img = tf.io.read_file(file_path)

        # Load in the image
        img = tf.io.decode_jpeg(byte_img) 
        
        # Resizing
        img = tf.image.resize(img, (105, 105))
        
        # Scaling
        img = img / 255.0
        
        return img
    
    # To verify the image
    def verify(self, *args):
        # Thresholds
        detection_threshold = 0.5
        verification_threshold = 0.5

        # Capturing input image from webcam
        SAVE_PATH = os.path.join('application_data', 'input_image', 'input_image.jpg')
        success, frame = self.capture.read()
        frame = frame[130:130+250, 150:150+250, :]
        cv2.imwrite(SAVE_PATH, frame)

        # Build results array
        results = []
        for image in os.listdir(os.path.join('application_data', 'verification_images')):
            input_img = self.preprocess(os.path.join('application_data', 'input_image', 'input_image.jpg'))
            validation_img = self.preprocess(os.path.join('application_data', 'verification_images', image))
            
            # Make Predictions 
            result = self.model.predict(list(np.expand_dims([input_img, validation_img], axis=1)), verbose = 0)
            results.append(result)
        
        # Detection Threshold: Metric above which a prediciton is considered positive 
        detection = np.sum(np.array(results) > detection_threshold)
        
        # Verification Threshold: Proportion of positive predictions / total positive samples 
        verification = detection / len(os.listdir(os.path.join('application_data', 'verification_images')))
        verified = verification > verification_threshold

        # Setting verification label
        self.verification_label.text = "Verified" if verified == True else "Unverfied"
        
        # return results, verified

if __name__ == '__main__':
    CamApp().run()