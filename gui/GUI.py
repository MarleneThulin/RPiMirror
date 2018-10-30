import tkinter as tk
import gui


class MainGUI(tk.Tk):
    root = tk.Tk()
    main_frame = None
    module_list = []
    model_list = []
    
    def __init__(self, model):
        self.model_list = model
    

    def hideModule(self,index):
        self.module_list[index].grid_remove()

    def showModule(self,index):
        self.module_list[index].grid()

    def quit(self, *args):
        print("captured ECS press")
        self.root.destroy()

    def start(self):

        self.root.configure(background="black")
        self.main_frame = tk.Frame(self.root, bg="black").grid(row=0, column=0)

        clock = gui.GUI_clock.ModuleGUIClock(self.main_frame)
        clock.grid(row=0, column=0, sticky=tk.W, padx=20, pady=20)
      
        #add data modules
        for i in range(0, len(self.model_list)):
            mod = gui.GUI_module.ModuleGUI(self.main_frame, self.model_list[i])
            self.module_list.append(mod)
            r = self.model_list[i].pos_row
            c = self.model_list[i].pos_col
            if r is None:
                r=i+1
            if c is None:
                c=0 
            mod.grid(row=r, column=c, sticky=tk.W, padx=20, pady=20)

        #bind Escape key to quit program
        self.root.bind('<Escape>', self.quit)

        #make full screen
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (width,height))
        #self.root.overrideredirect(1)
        self.root.focus_set()
        
       

        self.root.mainloop()

            
