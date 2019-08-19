from tkinter import *
from tkinter import filedialog

from classes.appmenu import AppMenu
from classes.apptracker import AppTracker

# needed, ignore unused and missing references errors
from modules.config import file_error
from modules.config import mean_px
from modules.config import std_px

from modules.interface import *

from modules.model import models


def main():
    root = Tk()
    try:
        root.iconbitmap('./assets/icon.ico')
    except TclError:
        root.iconphoto(True, PhotoImage(file="./assets/icon.gif"))
    root.title("readr")
    root.resizable(0, 0)

    app_tracker = AppTracker(root)
    app_tracker.grid(row=1)

    app_menu = AppMenu(root, app_tracker.progress_bar, app_tracker.status_label)
    app_menu.grid(row=0)

    # disables app functions if something's wrong
    if file_error is None:
        app_menu.batch_button.configure(command=lambda
                                        at=app_tracker:
                                        run_batch(at))
        app_menu.mult_button.configure(command=lambda
                                       at=app_tracker:
                                       run_mult(at))
        app_menu.single_button.configure(command=lambda
                                         at=app_tracker:
                                         run_single(at))

        app_menu.batch_button.bind("<Enter>", app_menu.on_batch_enter)
        app_menu.batch_button.bind("<Leave>", app_menu.on_batch_leave)

        app_menu.mult_button.bind("<Enter>", app_menu.on_mult_enter)
        app_menu.mult_button.bind("<Leave>", app_menu.on_mult_leave)

        app_menu.single_button.bind("<Enter>", app_menu.on_single_enter)
        app_menu.single_button.bind("<Leave>", app_menu.on_single_leave)

        app_tracker.update_status_label("Ready")

    else:
        app_menu.batch_button.configure(state=DISABLED)
        app_menu.mult_button.configure(state=DISABLED)
        app_menu.single_button.configure(state=DISABLED)

        app_tracker.update_status_label("Error: {} {}".format(file_error[0], file_error[1]))

    root.mainloop()


# functions assigned on click of buttons
def run_batch(app_tracker):
    img_dir = filedialog.askdirectory(initialdir="./", title="Select directory of image files")

    app_tracker.show_progress_bar()

    img_dir = check_batch(app_tracker, img_dir)

    if img_dir is not None:
        data = extract_batch(app_tracker, img_dir)

        csv_file = filedialog.asksaveasfilename(initialdir="./", title="Save data to", confirmoverwrite=False,
                                                filetypes=(("All files", "*.*"), ("CSV files", "*.csv")))

        csv_file = check_file(app_tracker, csv_file)

        if csv_file is not None:
            write_data(app_tracker, csv_file, data)

    app_tracker.hide_progress_bar()


def run_mult(app_tracker):
    img_files = list(filedialog.askopenfilenames(initialdir="./", title="Select image files",
                                                 filetypes=(("All files", "*.*"), ("JPEG files", "*.jpg"),
                                                            ("PNG files", "*.png"))))
    app_tracker.show_progress_bar()

    img_files = check_multiple(app_tracker, img_files)

    if img_files is not None:
        data = extract_multiple(app_tracker, img_files)

        csv_file = filedialog.asksaveasfilename(initialdir="./", title="Save data to", confirmoverwrite=False,
                                                filetypes=(("All files", "*.*"), ("CSV files", "*.csv"),))

        csv_file = check_file(app_tracker, csv_file)

        if csv_file is not None:
            write_data(app_tracker, csv_file, data)

    app_tracker.hide_progress_bar()


def run_single(app_tracker):
    img_file = filedialog.askopenfilename(initialdir="./", title="Select image file",
                                          filetypes=(("All files", "*.*"), ("JPEG files", "*.jpg"),
                                                     ("PNG files", "*.png")))
    app_tracker.show_progress_bar()

    img_file = check_single(app_tracker, img_file)

    if img_file is not None:
        data = extract_single(app_tracker, img_file)

        csv_file = filedialog.asksaveasfilename(initialdir="./", title="Save data to", confirmoverwrite=False,
                                                filetypes=(("All files", "*.*"), ("CSV files", "*.csv")))

        csv_file = check_file(app_tracker, csv_file)

        if csv_file is not None:
            write_data(app_tracker, csv_file, data)

    app_tracker.hide_progress_bar()
