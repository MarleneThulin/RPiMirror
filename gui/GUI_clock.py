import time
import gui
#import Tkinter as tk
import tkinter as tk

class ModuleGUIClock(gui.GUI_module.ModuleGUI):

    label_clock = None
    parent = None

    def update_clock(self):
        
        t = time.localtime()
        if self.label_clock is not None: 
            self.label_clock.configure(text= time.strftime("%H:%M:%S",t))
        self.after(1000, self.update_clock)

    def __init__(self, prnt):
        super().__init__(prnt, model=None)
        self.parent = prnt

        self.label_clock = tk.Label(self, text="00:00:00", fg="white", bg="black", font="Helvetica 44 bold" )
        self.label_clock.grid()
        self.update_clock()
