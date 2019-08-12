import os

from tkinter import *
from tkinter import filedialog

# needed, ignore unused and missing references error in IDE
from modules.config import file_error
from modules.config import mean_px
from modules.config import std_px

from modules.extract import process_batch
from modules.extract import process_single

from modules.model import models

from modules.write import read_values
from modules.write import map_values
from modules.write import write_rows


class MainWindow(Frame):

    # directory strings
    img_dir = ""

    # file strings
    csv_file = ""
    img_file = ""

    # lists
    img_files = []

    # stored data
    data = None

    def __init__(self, parent):
        Frame.__init__(self, parent)

        # load images
        self.ico_dir_d = PhotoImage(file="./assets/dir_d.png")
        self.ico_mul_d = PhotoImage(file="./assets/mul_d.png")
        self.ico_snl_d = PhotoImage(file="./assets/snl_d.png")

        self.ico_dir_h = PhotoImage(file="./assets/dir_h.png")
        self.ico_mul_h = PhotoImage(file="./assets/mul_h.png")
        self.ico_snl_h = PhotoImage(file="./assets/snl_h.png")

        width = 120
        height = 120

        self.batch_button = Button(
                                   text="Select Image Folder",
                                   image=self.ico_dir_d,
                                   font=("Segoe UI", 9),
                                   border="0",
                                   compound="top",
                                   command=self.run_batch,
                                   height=height,
                                   width=width,
                                   relief=FLAT)
        self.batch_button.grid(sticky="EW",
                               column=0,
                               row=0,
                               padx=(18, 18),
                               pady=(18, 18)
                               )

        self.single_button = Button(
                                    text="Select Single Image",
                                    image=self.ico_snl_d,
                                    font=("Segoe UI", 9),
                                    border="0",
                                    compound="top",
                                    command=self.run_single,
                                    height=height,
                                    width=width,
                                    relief=FLAT)
        self.single_button.grid(sticky="EW",
                                column=1,
                                row=0,
                                padx=(18, 18),
                                pady=(18, 18)
                                )

        self.mult_button = Button(
                                  text="Select Multiple Images",
                                  image=self.ico_mul_d,
                                  border="0",
                                  font=("Segoe UI", 9),
                                  compound="top",
                                  command=self.run_multiple,
                                  height=height,
                                  width=width,
                                  relief=FLAT)
        self.mult_button.grid(sticky="EW",
                              column=2,
                              row=0,
                              padx=(18, 18),
                              pady=(18, 18)
                              )

        self.status = StringVar()
        self.status_label = Label(anchor="w",
                                  background="#d9d9d9",
                                  foreground="#3f3f3f",
                                  font=("Gisha", 9),
                                  relief=FLAT,
                                  text="",
                                  textvariable=self.status)
        self.status_label.grid(sticky="EW", row=1, columnspan=3)

        if file_error is None:
            self.batch_button.bind("<Enter>", self.on_batch_enter)
            self.batch_button.bind("<Leave>", self.on_batch_leave)
            self.mult_button.bind("<Enter>", self.on_mult_enter)
            self.mult_button.bind("<Leave>", self.on_mult_leave)
            self.single_button.bind("<Enter>", self.on_single_enter)
            self.single_button.bind("<Leave>", self.on_single_leave)

            self.status.set("Ready")
        else:
            self.batch_button.configure(state=DISABLED)
            self.mult_button.configure(state=DISABLED)
            self.single_button.configure(state=DISABLED)

            self.status.set("Error: {} {}".format(file_error[0], file_error[1]))

    # on hover enter and leave events
    def on_batch_enter(self, event):
        self.status.set("Select a folder containing the document images to be read")
        self.batch_button.configure(image=self.ico_dir_h)

    def on_batch_leave(self, event):
        self.status.set("")
        self.batch_button.configure(image=self.ico_dir_d)

    def on_mult_enter(self, event):
        self.status.set("Select multiple document images to be read")
        self.mult_button.configure(image=self.ico_mul_h)

    def on_mult_leave(self, event):
        self.status.set("")
        self.mult_button.configure(image=self.ico_mul_d)

    def on_single_enter(self, event):
        self.status.set("Select a single document image to be read")
        self.single_button.configure(image=self.ico_snl_h)

    def on_single_leave(self, event):
        self.status.set("")
        self.single_button.configure(image=self.ico_snl_d)

    # process_* called by run_*
    def process_batch(self, img_dir):
        self.status.set("Working, please wait...")
        # process images
        batch = process_batch(img_dir)
        self.status.set("2/5 Extracted fields from {} image files".format(len(batch)))

        # read and map fields
        self.data = []
        for paper in batch:
            # read and map fields
            values = read_values(paper)
            row = map_values(values)
            self.data.append(row)

        self.status.set("3/5 Extracted values from fields")

        return

    def process_multiple(self, img_files):
        self.status.set("Working, please wait...")
        batch = []
        for file in img_files:
            paper = process_single(file)
            batch.append(paper)
        self.status.set("2/5 Extracted fields from {} image files".format(len(batch)))

        # read and map fields
        self.data = []
        for paper in batch:
            # read and map fields
            values = read_values(paper)
            row = map_values(values)
            self.data.append(row)

        self.status.set("3/5 Extracted values from fields")

        return

    def process_single(self, img_file):
        self.status.set("Working, please wait...")
        # process image
        paper = process_single(img_file)
        self.status.set("2/5 Extracted fields")

        # read and map fields
        values = read_values(paper)
        row = map_values(values)
        self.status.set("3/5 Extracted values from fields")

        # place in a list since write_rows accepts list
        self.data = [row]

        return

    # called by Buttons
    def run_batch(self):
        self.status.set("")
        self.csv_file = ''
        self.img_dir = ''

        self.data = None

        # look for directory of batch
        self.img_dir = filedialog.askdirectory(initialdir="./", title="Select directory of image files")
        if self.img_dir == '':
            self.status.set("Aborted: no directory path selected")
        elif not os.path.isdir(str(self.img_dir)):
            self.status.set("Aborted: invalid directory path")
        else:
            self.status.set("1/5 Successfully loaded directory")
            self.process_batch(self.img_dir)
            self.write_data()

    def run_multiple(self):
        self.status.set("")
        self.csv_file = ''
        self.img_files = []

        self.data = None

        # select multiple files
        self.img_files = list(filedialog.askopenfilenames(initialdir="./", title="Select image files",
                                                          filetypes=(("All files", "*.*"), ("JPEG files", "*.jpg"),
                                                                     ("PNG files", "*.png"))))
        if len(self.img_files) == 0:
            self.status.set("Aborted: no image files selected")
        else:
            for file in self.img_files:
                if not (file.endswith('.png') or file.endswith('.jpg')):
                    self.img_files.remove(file)
                    self.status.set("Ignored {}: invalid image file format".format(file))

            if len(self.img_files) == 0:
                self.status.set("Aborted: no valid image files to read")
            elif len(self.img_files) == 1:
                self.status.set("1/5 Successfully loaded image file")
                self.process_single(self.img_files[0])
                self.write_data()
            elif len(self.img_files) > 1:
                self.status.set("1/5 Successfully loaded {} image files".format(len(self.img_files)))
                self.process_multiple(self.img_files)
                self.write_data()

    def run_single(self):
        # clear previous values
        self.status.set("")
        self.csv_file = ''
        self.img_file = ''

        self.data = None

        # look for directory of batch
        self.img_file = filedialog.askopenfilename(initialdir="./", title="Select image file",
                                                   filetypes=(("All files", "*.*"), ("JPEG files", "*.jpg"),
                                                              ("PNG files", "*.png")))
        if self.img_file == '':
            self.status.set("Aborted: no image file selected")
        elif not (self.img_file.endswith('.png') or self.img_file.endswith('.jpg')):
            self.status.set("Aborted: invalid image file")
        else:
            self.status.set("1/5 Successfully loaded image file")
            self.process_single(self.img_file)
            self.write_data()

    # called by run_* functions
    def write_data(self):
        self.csv_file = filedialog.asksaveasfilename(initialdir="./", title="Save data to", confirmoverwrite=False,
                                                filetypes=(("All files", "*.*"), ("CSV files", "*.csv")))
        if self.csv_file == '':
            self.status.set("Aborted: no csv file selected")
        elif not self.csv_file.endswith('.csv'):
            self.status.set("Aborted: invalid csv file")
        else:
            self.status.set("4/5 Successfully loaded csv file")
            ret = write_rows(self.csv_file, self.data)
            self.status.set("5/5 {}".format(ret))


def main():
    root = Tk()
    try:
        root.iconbitmap('./assets/icon.ico')
    except TclError:
        root.iconphoto(True, PhotoImage(file="./assets/icon.gif"))
    root.title("readr")
    root.resizable(0, 0)
    MainWindow(root).grid()
    root.mainloop()
