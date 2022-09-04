from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from tkinter import END
import tensorflow as tf
from tensorflow.keras import backend as K

import cv2
import numpy as np

tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)

#   METHODS

class Backend:
    '''
    Class to define methods used by UI
    '''

    def read_jpg_file(self, path):
        ''' Method for read image jpeg'''
        img = cv2.imread(path)
        img_array = np.asarray(img)
        img2show = Image.fromarray(img_array)
        img2 = img_array.astype(float)
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
        img2 = np.uint8(img2)
        return img2, img2show

    def read_dicom_file(self, path):
        img = dicom.read_file(path)
        img_array = img.pixel_array
        img2show = Image.fromarray(img_array)
        img2 = img_array.astype(float)
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
        img2 = np.uint8(img2)
        img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
        return img_RGB, img2show

    def model_fun(self):
        ''' method to load trained model'''
        model_cnn = tf.keras.models.load_model("backend/WilhemNet_86.h5")
        return model_cnn

    def predict(self, array):
        #   1. call function to pre-process image: it returns image in batch format
        batch_array_img = self.preprocess(array)
        #   2. call function to load model and predict: it returns predicted class and probability
        model = self.model_fun()
        # model_cnn = tf.keras.models.load_model('conv_MLP_84.h5')
        prediction = np.argmax(model.predict(batch_array_img))
        proba = np.max(model.predict(batch_array_img)) * 100
        label = ""
        if prediction == 0:
            label = "bacteriana"
        if prediction == 1:
            label = "normal"
        if prediction == 2:
            label = "viral"
        #   3. call function to generate Grad-CAM: it returns an image with a superimposed heatmap
        heatmap = self.grad_cam(array)
        return (label, proba, heatmap)

    def preprocess(self, array):
        array = cv2.resize(array, (512, 512))
        array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        array = clahe.apply(array)
        array = array / 255
        array = np.expand_dims(array, axis=-1)
        array = np.expand_dims(array, axis=0)
        return array

    def grad_cam(self, array):
        img = self.preprocess(array)
        model = self.model_fun()
        preds = model.predict(img)
        argmax = np.argmax(preds[0])
        output = model.output[:, argmax]
        last_conv_layer = model.get_layer("conv10_thisone")
        grads = K.gradients(output, last_conv_layer.output)[0]
        pooled_grads = K.mean(grads, axis=(0, 1, 2))
        iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
        pooled_grads_value, conv_layer_output_value = iterate(img)
        for filters in range(64):
            conv_layer_output_value[:, :, filters] *= pooled_grads_value[filters]
        # creating the heatmap
        heatmap = np.mean(conv_layer_output_value, axis=-1)
        heatmap = np.maximum(heatmap, 0)  # ReLU
        heatmap /= np.max(heatmap)  # normalize
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[2]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        img2 = cv2.resize(array, (512, 512))
        hif = 0.8
        transparency = heatmap * hif
        transparency = transparency.astype(np.uint8)
        superimposed_img = cv2.add(transparency, img2)
        superimposed_img = superimposed_img.astype(np.uint8)
        return superimposed_img[:, :, ::-1]
