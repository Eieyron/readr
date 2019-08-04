import os

from tkinter import *
from tkinter import filedialog

from modules.config import mean_px
from modules.config import std_px

from modules.extract import process_batch
from modules.extract import process_single

from modules.model import models

from modules.write import read_values
from modules.write import map_values
from modules.write import write_rows


class MainWindow(Frame):
    # icons

    # directory strings
    img_dir = ""

    # file strings
    csv_file = ""
    img_file = ""

    # lists
    img_files = []

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.ico_dir_d = PhotoImage(file="./assets/dir_d.png")
        self.ico_mul_d = PhotoImage(file="./assets/mul_d.png")
        self.ico_snl_d = PhotoImage(file="./assets/snl_d.png")

        self.ico_dir_h = PhotoImage(file="./assets/dir_h.png")
        self.ico_mul_h = PhotoImage(file="./assets/mul_h.png")
        self.ico_snl_h = PhotoImage(file="./assets/snl_h.png")

        self.batch_button = Button(
                                   # text='Process image directory',
                                   image=self.ico_dir_d,
                                   border="0",
                                   # compound="top",
                                   command=self.run_batch,
                                   height=100,
                                   width=100,
                                   relief=FLAT)
        self.batch_button.grid(sticky="EW",
                               column=0,
                               row=0,
                               padx=(18, 18),
                               pady=(18, 18)
                               )
        self.batch_button.bind("<Enter>", self.on_batch_enter)
        self.batch_button.bind("<Leave>", self.on_batch_leave)

        self.single_button = Button(
                                    # text='Process single image',
                                    image=self.ico_snl_d,
                                    border="0",
                                    # compound="top",
                                    command=self.run_single,
                                    height=100,
                                    width=100,
                                    relief=FLAT)
        self.single_button.grid(sticky="EW",
                                column=1,
                                row=0,
                                padx=(18, 18),
                                pady=(18, 18)
                                )
        self.single_button.bind("<Enter>", self.on_single_enter)
        self.single_button.bind("<Leave>", self.on_single_leave)

        self.mult_button = Button(
                                  # text='Process multiple images',
                                  image=self.ico_mul_d,
                                  border="0",
                                  # compound="top",
                                  command=self.run_multiple,
                                  height=100,
                                  width=100,
                                  relief=FLAT)
        self.mult_button.grid(sticky="EW",
                              column=2,
                              row=0,
                              padx=(18, 18),
                              pady=(18, 18)
                              )
        self.mult_button.bind("<Enter>", self.on_mult_enter)
        self.mult_button.bind("<Leave>", self.on_mult_leave)

        self.status = StringVar()
        self.status.set("Ready")
        self.status_label = Label(anchor="w",
                                  background="#d9d9d9",
                                  foreground="#3f3f3f",
                                  font=("Gisha", 9),
                                  relief=FLAT,
                                  text="",
                                  textvariable=self.status)
        self.status_label.grid(sticky="EW", row=1, columnspan=3)

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

    def process_batch(self, csv_file, img_dir):
        # process images
        batch = process_batch(img_dir)
        self.status.set("3/5 Extracted fields from {} image files".format(len(batch)))

        # read and map fields
        data = []
        for paper in batch:
            # read and map fields
            values = read_values(paper)
            row = map_values(values)
            data.append(row)

        self.status.set("4/5 Extracted values from fields")

        # write to file
        ret = write_rows(csv_file, data)
        self.status.set("5/5 {}".format(ret))

        return

    def process_multiple(self, csv_file, img_files):
        batch = []
        for file in img_files:
            paper = process_single(file)
            batch.append(paper)
        self.status.set("3/5 Extracted fields from {} image files".format(len(batch)))

        # read and map fields
        data = []
        for paper in batch:
            # read and map fields
            values = read_values(paper)
            row = map_values(values)
            data.append(row)

        self.status.set("4/5 Extracted values from fields")

        # write to file
        ret = write_rows(csv_file, data)
        self.status.set("5/5 {}".format(ret))

        return

    def process_single(self, csv_file, img_file):
        # process image
        paper = process_single(img_file)
        self.status.set("3/5 Extracted fields")

        # read and map fields
        values = read_values(paper)
        row = map_values(values)
        self.status.set("4/5 Extracted values from fields")

        # write to file
        # place in a list since write_rows accepts list
        data = [row]
        ret = write_rows(csv_file, data)
        self.status.set("5/5 {}".format(ret))

        return

    def run_batch(self):
        # clear previous values
        self.status.set("")
        self.csv_file = ''
        self.img_dir = ''

        # look for directory of batch
        self.img_dir = filedialog.askdirectory(initialdir="./", title="Select directory of image files")
        if self.img_dir == '':
            self.status.set("Aborted: no directory path selected")
            return
        elif not os.path.isdir(self.img_dir):
            self.status.set("Aborted: invalid directory path")
            return

        self.status.set("1/5 Successfully loaded directory")

        # look for csv file
        self.csv_file = filedialog.askopenfilename(initialdir="./", title="Select csv file")
        if self.csv_file == '':
            self.status.set("Aborted: no csv file selected")
            return
        elif not self.csv_file.endswith('.csv'):
            self.status.set("Aborted: invalid csv file")
            return

        self.status.set("2/5 Successfully loaded csv file")

        self.process_batch(self.csv_file, self.img_dir)

        self.status.set("Done")
        return

    def run_multiple(self):
        # clear previous values
        self.status.set("")
        self.csv_file = ''
        self.img_files = []

        # select multiple files
        self.img_files = list(filedialog.askopenfilenames(initialdir="./", title="Select image files"))
        if len(self.img_files) == 0:
            self.status.set("Aborted: no image files selected")
            return

        # filter out invalid files
        for file in self.img_files:
            if not (file.endswith('.png') or file.endswith('.jpg')):
                self.img_files.remove(file)
                self.status.set("Ignored {}: invalid image file format".format(file))

        if len(self.img_files) == 0:
            self.status.set("Aborted: no valid image files to read")
            return

        elif len(self.img_files) == 1:
            self.status.set("1/5 Successfully loaded image file")

            # look for csv file
            self.csv_file = filedialog.askopenfilename(initialdir="./", title="Select csv file")
            if self.csv_file == '':
                self.status.set("Aborted: no csv file selected")
                return
            elif not self.csv_file.endswith('.csv'):
                self.status.set("Aborted: invalid csv file")
                return

            self.status.set("2/5 Successfully loaded csv file")

            self.process_single(self.csv_file, self.img_files[0])

            self.status.set("Done")
            return

        else:
            self.status.set("1/5 Successfully loaded {} image files".format(len(self.img_files)))

            # look for csv file
            self.csv_file = filedialog.askopenfilename(initialdir="./", title="Select csv file")
            if self.csv_file == '':
                self.status.set("Aborted: no csv file selected")
                return
            elif not self.csv_file.endswith('.csv'):
                self.status.set("Aborted: invalid csv file")
                return

            self.status.set("2/5 Successfully loaded csv file")

            self.process_multiple(self.csv_file, self.img_files)

            self.status.set("Done")
            return

    def run_single(self):
        # clear previous values
        self.status.set("")
        self.csv_file = ''
        self.img_file = ''

        # look for directory of batch
        self.img_file = filedialog.askopenfilename(initialdir="./", title="Select image file")
        if self.img_file == '':
            self.status.set("Aborted: no image file selected")
            return
        elif not (self.img_file.endswith('.png') or self.img_file.endswith('.jpg')):
            self.status.set("Aborted: invalid image file")
            return

        self.status.set("1/5 Successfully loaded image file")

        # look for csv file
        self.csv_file = filedialog.askopenfilename(initialdir="./", title="Select csv file")
        if self.csv_file == '':
            self.status.set("Aborted: no csv file selected")
            return
        elif not self.csv_file.endswith('.csv'):
            self.status.set("Aborted: invalid csv file")
            return

        self.status.set("2/5 Successfully loaded csv file")

        self.process_single(self.csv_file, self.img_file)

        self.status.set("Done")
        return


def main():
    root = Tk()
    root.title("readr")
    root.resizable(0, 0)
    MainWindow(root).grid()
    root.mainloop()
