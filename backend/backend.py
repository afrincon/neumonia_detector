from tkinter import filedialog

#   METHODS

class Backend:
    '''
    Class to define methods used by UI
    '''
    def load_img_file(self) -> None:
        '''Methd to load images'''
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Select image",
            filetypes=(
                ("DICOM", "*.dcm"),
                ("JPEG", "*.jpeg"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
            ),
        )
        print(filepath)
        #if filepath:
        #    self.array, img2show = read_dicom_file(filepath)
        #    self.img1 = img2show.resize((250, 250), Image.ANTIALIAS)
        #    self.img1 = ImageTk.PhotoImage(self.img1)
        #    self.text_img1.image_create(END, image=self.img1)
        #    self.button1["state"] = "enabled"