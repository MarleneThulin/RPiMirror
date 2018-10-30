import tkinter as tk
#import Tkinter as tk

class ModuleGUI(tk.Frame):

    model = None
    labels = None

    def __init__(self, prnt, model):
        self.model = model
        super().__init__(prnt, bg="black")

        if model is not None:
            labels = [None] * model.data_rows

            for i in range(0, model.data_rows):
                labels[i] = []
                for j in range(0, model.data_cols):
                    labels[i].append(tk.Label(self, textvariable=model.data[i][j], fg="white", bg="black", font="Helvetica 14 bold"))
                    labels[i][j].grid(row=i, column=j, sticky=tk.W, padx=10)
                


                #tk.Label(self, text="Module, " +str(model.data_rows)  + "x" + str(model.data_cols), fg="white", bg="black", font="Helvetica 40 bold" ).grid(row=0, column=0, sticky=tk.W)
