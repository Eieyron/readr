from tkinter import *


class AppMenu(Frame):
    def __init__(self, parent, progress_bar, status_label):
        Frame.__init__(self, parent)

        # load images
        self.ico_dir_d = PhotoImage(file="./assets/dir_d.png")
        self.ico_mul_d = PhotoImage(file="./assets/mul_d.png")
        self.ico_snl_d = PhotoImage(file="./assets/snl_d.png")

        self.ico_dir_h = PhotoImage(file="./assets/dir_h.png")
        self.ico_mul_h = PhotoImage(file="./assets/mul_h.png")
        self.ico_snl_h = PhotoImage(file="./assets/snl_h.png")

        # button arguments
        width = 120
        height = 120
        font = ("Segoe UI", 9)
        border = "0"
        compound = "top"
        relief = FLAT
        pad = (18, 18)

        # widgets from AppStatusTracker
        self.progress_bar = progress_bar
        self.status_label = status_label

        # widgets
        self._batch_button = Button(text="Select Image Folder", image=self.ico_dir_d, font=font, border=border,
                                    compound=compound, height=height, width=width, relief=relief)
        self._batch_button.grid(sticky="EW", column=0, row=0, padx=pad, pady=pad)

        self._single_button = Button(text="Select Single Image", image=self.ico_snl_d, font=font, border=border,
                                     compound=compound, height=height, width=width, relief=relief)
        self._single_button.grid(sticky="EW", column=1, row=0, padx=pad, pady=pad)

        self._mult_button = Button(text="Select Multiple Images", image=self.ico_mul_d, font=font, border=border,
                                   compound=compound, height=height, width=width, relief=relief)
        self._mult_button.grid(sticky="EW", column=2, row=0, padx=pad, pady=pad)

    # on hover enter and leave events
    def on_batch_enter(self, event):
        self.status_label.configure(text="Select a folder containing the document images to be read")
        self._batch_button.configure(image=self.ico_dir_h)

    def on_batch_leave(self, event):
        self.status_label.configure(text="")
        self._batch_button.configure(image=self.ico_dir_d)

    def on_mult_enter(self, event):
        self.status_label.configure(text="Select multiple document images to be read")
        self._mult_button.configure(image=self.ico_mul_h)

    def on_mult_leave(self, event):
        self.status_label.configure(text="")
        self._mult_button.configure(image=self.ico_mul_d)

    def on_single_enter(self, event):
        self.status_label.configure(text="Select a single document image to be read")
        self._single_button.configure(image=self.ico_snl_h)

    def on_single_leave(self, event):
        self.status_label.configure(text="")
        self._single_button.configure(image=self.ico_snl_d)

    @property
    def batch_button(self):
        return self._batch_button

    @property
    def mult_button(self):
        return self._mult_button

    @property
    def single_button(self):
        return self._single_button
