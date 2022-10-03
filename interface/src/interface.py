# import the necessary packages
from tkinter import Tk, Button, Label, filedialog, BOTTOM
import tkinter as ttk
import base64
from tkinter.messagebox import WARNING, askokcancel
from turtle import clear

import grpc
from PIL import Image
from PIL import ImageTk
import numpy as np

import backend_pb2
import backend_pb2_grpc

def select_image():
    # grab a reference to the image panels
    global panelA, backend_client
    # open a file chooser dialog and allow the user to select an input
    # image
    path = filedialog.askopenfilename(title="Select image",
            filetypes=(
                ("JPEG", "*.jpeg"),
                ("DICOM", "*.dcm"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
            ))

    # ensure a file path was selected
    if len(path) > 0:

        path_message = backend_pb2.img_path(path=path)
        response = backend_client.load_image(path_message)

        img_content = response.img_content
        img_w = response.width
        img_h = response.height

        b64decoded = base64.b64decode(img_content)
        image = np.frombuffer(b64decoded, dtype=np.uint8).reshape(img_h, img_w, -1)

        # convert the images to PIL format...
        image = Image.fromarray(image)
        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)

        # if the panels are None, initialize them
        if panelA is None:
            # the first panel will store our original image
            panelA = Label(image=image).grid(column=0, row=2, columnspan=4, pady=10)
            panelA.image = image            
        else:
            # update the pannels
            panelA.configure(image=image)
            panelA.image = image

def make_prediction():
    # grab a reference to the image panels
    global panelA, backend_client

    # open a file chooser dialog and allow the user to select an input
    # image
    path = filedialog.askopenfilename(title="Select image",
            filetypes=(
                ("JPEG", "*.jpeg"),
                ("DICOM", "*.dcm"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
            ))

    # ensure a file path was selected
    if len(path) > 0:

        path_message = backend_pb2.img_path(path=path)
        response = backend_client.load_image(path_message)

        img_content = response.img_content
        img_w = response.width
        img_h = response.height
    
    image_data = backend_pb2.image_data(b64image=img_content, width=img_w, height=img_h)
    data = backend_client.predict_data(image_data)
    
    result_prediction = "Resultado de la evaluación de la imagen\n Presenta un tipo de neumonia {}, \n con una probabilidad de {:.2f}%".format(data.label, data.prediction)

    if panelA is None:
        panelA = Label(frm, text=result_prediction).grid(column=0, row=2, columnspan=4, pady=10)        
    else:
            # update the pannels
        panelA.configure(text=result_prediction)
        #panelA.image = result_prediction


# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Herramienta para la detección rápida de neumonía")
root.resizable(0, 0)
frm = ttk.Frame(root, padx=10, pady=10)
frm.grid()

panelA = None

# Backend client definition
maxMsgLength = 1024 * 1024 * 1024
options = [('grpc.max_message_length', maxMsgLength),
                                         ('grpc.max_send_message_length', maxMsgLength),
                                         ('grpc.max_receive_message_length', maxMsgLength)]
channel = grpc.insecure_channel("backend:50051", options = options)
backend_client = backend_pb2_grpc.BackendStub(channel=channel)

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(frm, text="Select an image", command=select_image).grid(column=0, row=1)

prediction = Button(frm, text='Make a prediction', command=make_prediction).grid(column=2, row=1, padx=10)

exit_app = Button(frm, text='Exit', command=root.destroy).grid(column=3, row=1)

# kick off the GUI
root.mainloop()
