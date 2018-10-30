from gui import *
from apis import *
from model import *
import time
import configparser as cfparser
import threading

config = cfparser.ConfigParser()

mgui = None
modules = []
data_model = []
threads = []

def run():
    global mgui
    mgui = GUI.MainGUI(data_model)

    data_model.append(dataobject.DataObject(1,1))
    
    modules.append(api_sl.SL_APIrequester(data_model[0]))

    data_model.append(dataobject.DataObject(2,0))
    
    modules.append(api_kth.KTH_APIrequester(data_model[1]))

    data_model.append(dataobject.DataObject(2,1))
    
    modules.append(api_smhi.SMHI_APIrequester(data_model[2]))
    
    #request data from each active API module
    for i in range(0, len(modules)):
        modules[i].request()
        threads.append(threading.Thread(target=modules[i].run))
        threads[i].setDaemon(True)
        threads[i].start()
    
    mgui.start()


def stopthreads():
    for i in range(0, len(modules)):
        modules[i].stop()

run()

print("returned from main run()")

stopthreads()

