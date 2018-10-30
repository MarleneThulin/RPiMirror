from .api import *
import time
import datetime
from dateutil.tz import tzlocal

config = cfparser.ConfigParser()

class SMHI_APIrequester(APIrequester):

    dorun = 0
    max_items = 5
    delta_hours = 4
    model = None
    requeststr = None
    update = None
  
    def __init__(self, modelobj, active = True):
        super().__init__()
        self.model = modelobj
        self.model.setDataSize(rows=self.max_items, columns=3)
        self.update = active
        config.read('./apis/apiconfig.ini')

        #make request string
        self.requeststr = "https://opendata-download-metfcst.smhi.se"
        self.requeststr += "/api/category/" + str(config['API_SMHI']['category']) + "/version/" + str(config['API_SMHI']['version'])
        self.requeststr += "/geotype/point/lon/"+str(config['API_SMHI']['long'])+"/lat/"+str(config['API_SMHI']['lat'])+"/data.json"

    def request(self):
        #print("requesting weather forecast...")
        res = None
        res = requests.get(self.requeststr, allow_redirects=True)

        if res is None:
            print("Unable to fetch weather data")
            return
    
        data = parse(res, self.delta_hours, self.max_items)     

        if data is not None:
            try:
                self.model.setData(data)
            except Exception:
                pass

    def run(self):
        self.dorun = 1

        while self.dorun == 1:
            if self.update ==True:
                self.request()
            #sleep for 15 min
            time.sleep(15*60)

    def activate(self):
        self.update = True
        self.request()
    def inactivate(self):
        self.update = False   

    def stop(self):
        self.dorun = 0


def formatData(forecast):

    row = []

    #datestr = forecast['validTime'][0:forecast['validTime'].index('T')]
    timestr = forecast['validTime'][forecast['validTime'].index('T')+1:-4]

    #row.append(datestr)
    row.append(timestr)

    for i in forecast['parameters']:
        
        name = str(i.get('name'))
        if name is "t":
            row.append(str(i['values'][0])+' '+u'\xb0'+'C')      
        if "ws" in name:
            row.append(str(i['values'][0])+" m/s")

    return row

def parse(data, d_hours, max_items):

    d = None
    try:
        d = data.json().get("timeSeries")
    except Exception:
        print("Unable to parse weather data")
        return None
    
    table = []

    i = 2
    while i <= len(d) and len(table)<max_items:

        table.append(formatData(d[i]))
        i += d_hours
    
    return table

    
    
