from tkinter import filedialog
from tkinter import *

# from fn import * 

class MainWindow(Frame):
    
    # directory strings
    dir_batch = "./"

    # file strings
    file_out = "./"
    file_img = "./"

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.toProcess = StringVar(None, "single")
        
        self.batch_radio = Radiobutton(text='Process batch  ', variable=self.toProcess, value="batch")
        self.batch_radio.grid(sticky="NEWS")

        self.paper_radio = Radiobutton(text='Process paper  ', variable=self.toProcess, value="single")
        self.paper_radio.grid(sticky="NEWS")

        self.browse_button = Button(text='Browse', command=self.browse, height=1)
        self.browse_button.grid(sticky="NEWS")

        self.run_button = Button(text='Run', command=self.run, height=1)
        self.run_button.grid(sticky="NEWS")

        self.save_button = Button(text='Save', command=self.save, height=1)
        self.save_button.grid(sticky="NEWS")

        self.status=StringVar()
        self.status_label=Label(justify=LEFT, relief=SUNKEN, text="", textvariable=self.status)
        self.status_label.grid(sticky="NEWS")

    # filedialog gets the whole dir string
    def browse(self):
        self.status.set("Browsing...")

        if self.toProcess.get() == "batch":
            # look for directory of batch
            self.dir_batch = filedialog.askdirectory(initialdir="./", title="Select directory of batch")
            print(self.dir_batch)
            # processBatch

        if self.toProcess.get() == "single":
            # look for file to process
            self.file_input = filedialog.askopenfilename(initialdir="./", title="Select file")
            print(self.file_input)
            # processSingle

    def run(self):
        self.status.set("processing")

        int(self.toProcess.get())

    def save(self):
        print(int(self.toProcess.get()))
        self.status.set("saving")

def main():
    root=Tk()
    root.title("")
    MainWindow(root).grid()
    root.mainloop()