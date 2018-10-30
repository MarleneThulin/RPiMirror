import tkinter as tk


class DataObject:
    pos_row = None
    pos_col = None
    
    data_rows = 0
    data_cols = 0

    data = []

    def __init__(self, posy=None, posx=None):
        self.pos_row = posy
        self.pos_col = posx
        #print("init DataObject")


    def setDataSize(self, **kwargs):
        for key, val in kwargs.items():
            #print('[%s] => [%s]' % (str(key), str(val)))
            if key is 'columns':
                self.data_cols = val

            elif key is 'rows':
                self.data_rows = val

        self.data = [None] * self.data_rows

        for i in range(0, self.data_rows):
            self.data[i] = []
            for j in range(0, self.data_cols):           
                self.data[i].append(tk.StringVar())
                self.data[i][j].set("")
                

    def setData(self, newdata):
        #print("setData() rows = "+str(self.data_rows)+", cols="+str(self.data_cols))
        #print("Newdata [" + str(len(newdata))+"]["+str(len(newdata[0]))+"]")

        for i in range(0, self.data_rows):
            for j in range(0, self.data_cols):
                #print("Data [" + str(i)+"]["+str(j)+"]:" +str(self.data[i][j]))
                #print("New data [" + str(i)+"]["+str(j)+"]:" +str(newdata[i][j]))
                self.data[i][j].set(str(newdata[i][j]))
        
        
