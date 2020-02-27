from tkinter import *
from tkinter.ttk import Progressbar


class AppTracker(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # widgets
        self._status_label = Label(parent, anchor="w", font=("Gisha", 8), text="",
                                   background="#d9d9d9", foreground="#3f3f3f")
        self._status_label.grid(sticky="NEWS", row=1, rowspan=1, column=0, columnspan=3, ipady=1)

        self._progress_bar = Progressbar(parent, maximum=40, mode='determinate', orient="horizontal")
        self._loading_bar = Progressbar(parent, maximum=40, mode='indeterminate', orient="horizontal")

        # self._preset_button = Button(parent, border=0, font=("Gisha", 8), text="Change preset file..")
        # self._preset_button.grid(sticky="EW", row=1, rowspan=1, column=2, columnspan=1)

    @property
    def loading_bar(self):
        return self._loading_bar

    @property
    def progress_bar(self):
        return self._progress_bar

    @property
    def status_label(self):
        return self._status_label

    # @property
    # def preset_button(self):
    #     return self._preset_button

    def show_loading_bar(self):
        self._loading_bar.grid(sticky="EW", row=1, rowspan=1, column=2, columnspan=1)
        self._loading_bar.update_idletasks()

    def hide_loading_bar(self):
        self._loading_bar.stop()
        self._loading_bar.grid_forget()
        self._loading_bar.update_idletasks()

    def show_progress_bar(self):
        self._progress_bar.grid(sticky="EW", row=1, rowspan=1, column=2, columnspan=1)
        self._progress_bar.update_idletasks()

    def hide_progress_bar(self):
        self._progress_bar.grid_forget()
        self._progress_bar.update_idletasks()

    def update_status_label(self, text):
        self._status_label.configure(text=text)
        self._status_label.update_idletasks()

    def update_progress_bar(self, value):
        self._progress_bar['value'] = value
        self._progress_bar.update_idletasks()

    def update_loading_bar(self, value):
        self._loading_bar.step(value)
        self._loading_bar.update_idletasks()
