"""
Methods used to build UI.
"""
from tkinter import END, StringVar, Text, Tk, filedialog, font, ttk
from tkinter.messagebox import WARNING, askokcancel, showinfo
import csv
from PIL import Image, ImageTk
import tkcap
from tkinter.filedialog import askopenfile

import os
from os.path import exists

import backend.backend as backend

class App:
    '''
    UI definition 
    '''   

    def __init__(self):
        self.root = Tk()
        self.root.title("Herramienta para la detección rápida de neumonía")

        # Bold Font
        fonti = font.Font(weight='bold')

        self.root.geometry("815x560")
        self.root.resizable(0, 0)

        # Labels
        self.lab1 = ttk.Label(self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con Heatmap", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Resultado:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Cédula Paciente:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE NEUMONÍA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Probabilidad:", font=fonti)

        # Two string variables to contain id an result
        self.ID = StringVar()
        self.result = StringVar()

        # Two input boxes
        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)

        #   GET ID
        self.ID_content = self.text1.get()

        #   TWO IMAGE INPUT BOXES
        self.text_img1 = Text(self.root, width=31, height=15)
        self.text_img2 = Text(self.root, width=31, height=15)
        self.text2 = Text(self.root)
        self.text3 = Text(self.root)

        #   BUTTONS
        self.button1 = ttk.Button(
            self.root, text="Predecir", state="disabled", command=self.run_model
        )
        self.button2 = ttk.Button(
            self.root, text="Cargar Imagen", command=self.load_img_file
        )
        self.button2.pack()
        self.button3 = ttk.Button(self.root, text="Borrar", command=self.delete)
        self.button4 = ttk.Button(self.root, text="PDF", command=self.create_pdf)
        self.button6 = ttk.Button(
            self.root, text="Guardar", command=self.save_results_csv
        )

        model_path = 'backend/WilhemNet_86.h5'

        if not exists(model_path):
            showinfo(title="Modelo no encontrado", message="Para esta version de la apicacion se debe de colocar en modelo en la carpeta 'backend' con el nombre de WilhemNet_86.h5.")

        #   WIDGETS POSITIONS
        self.lab1.place(x=110, y=65)
        self.lab2.place(x=545, y=65)
        self.lab3.place(x=500, y=350)
        self.lab4.place(x=65, y=350)
        self.lab5.place(x=122, y=25)
        self.lab6.place(x=500, y=400)
        self.button1.place(x=190, y=460)
        self.button2.place(x=70, y=460)
        self.button3.place(x=520, y=460)
        self.button4.place(x=410, y=460)
        self.button6.place(x=300, y=460)
        self.text1.place(x=200, y=350)
        self.text2.place(x=610, y=350, width=90, height=30)
        self.text3.place(x=610, y=400, width=90, height=30)
        self.text_img1.place(x=65, y=90)
        self.text_img2.place(x=500, y=90)

        #   FOCUS ON PATIENT ID
        self.text1.focus_set()

        #  se reconoce como un elemento de la clase
        self.array = None

        #   NUMERO DE IDENTIFICACIÓN PARA GENERAR PDF
        self.reportID = 0

        #   RUN LOOP
        self.root.mainloop()
    
    def load_img_file(self):
        ''' method for load images '''
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select image",
            filetypes=(
                ("JPEG", "*.jpeg"),
                ("DICOM", "*.dcm"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
            ),
        )

        back_methods = backend.Backend()

        if file_path:
            if file_path.endswith('jpeg'):                
                self.array, img2show =  back_methods.read_jpg_file(file_path)
            elif file_path.endswith('dcm'):
                self.array, img2show = back_methods.read_dicom_file(file_path)

            self.img1 = img2show.resize((250, 250), Image.ANTIALIAS)
            self.img1 = ImageTk.PhotoImage(self.img1)
            self.text_img1.image_create(END, image=self.img1)
            self.button1["state"] = "enabled"

    def run_model(self):
        ''' method to invoke predictions'''
        back_methods = backend.Backend()
        self.label, self.proba, self.heatmap = back_methods.predict(self.array)
        self.img2 = Image.fromarray(self.heatmap)
        self.img2 = self.img2.resize((250, 250), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        print("OK")
        self.text_img2.image_create(END, image=self.img2)
        self.text2.insert(END, self.label)
        self.text3.insert(END, "{:.2f}".format(self.proba) + "%")

    def delete(self):
        ''' Delete information from UI'''
        answer = askokcancel(
            title="Confirmación", message="Se borrarán todos los datos.", icon=WARNING
        )
        if answer:
            self.text1.delete(0, "end")
            self.text2.delete(1.0, "end")
            self.text3.delete(1.0, "end")
            self.text_img1.delete(self.img1, "end")
            self.text_img2.delete(self.img2, "end")
            showinfo(title="Borrar", message="Los datos se borraron con éxito")

    def create_pdf(self):
        cap = tkcap.CAP(self.root)
        ID = "Reporte" + str(self.reportID) + ".jpg"
        img = cap.capture(ID)
        img = Image.open(ID)
        img = img.convert("RGB")
        pdf_path = r"Reporte" + str(self.reportID) + ".pdf"
        img.save(pdf_path)
        self.reportID += 1
        showinfo(title="PDF", message="El PDF fue generado con éxito.")

    def save_results_csv(self):
        ''' Method to save information to a file'''
        with open('historial.csv', "a", encoding="utf-8") as csvfile:
            w = csv.writer(csvfile, delimiter="-")
            w.writerow(
                [self.text1.get(), self.label, "{:.2f}".format(self.proba) + "%"]
            )
            showinfo(title="Guardar", message="Los datos se guardaron con éxito.")

    def test_button(self):
        '''Return hello world test function'''
        print('hello world')
