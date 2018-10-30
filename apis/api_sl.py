import time
import datetime
from dateutil.tz import tzlocal
from .api import *

config = cfparser.ConfigParser()

class SL_APIrequester():
    apikey = ""
    stationid = None
    max_items = 5
    minutes_from_now = 3
    model = None
    dorun = False
    update = None
  
    def __init__(self, modelobj, active=True):
        super().__init__()
        self.model = modelobj
        self.model.setDataSize(rows=self.max_items, columns=3)
        self.update = active
        #get api key from file
        config.read('./apis/apiconfig.ini')
        self.apikey = str(config['API_SL']['trafiklab1'])

        #get max_journeys, station id

    def request(self):
        
        reqtime = datetime.datetime.now(tzlocal()) + datetime.timedelta(minutes = self.minutes_from_now)

        #t = time.localtime()
        #right justify with '0' to ensure hour and min args have 2 digits
        h = str(reqtime.hour).rjust(2, '0')
        m = str(reqtime.minute).rjust(2, '0')
        timearg = h+":"+m
        
        rstring = "https://api.resrobot.se/v2/departureBoard?key="+ self.apikey +"&id=740001178&time="+timearg+"&maxJourneys="+ str(self.max_items) +"&passlist=0&format=json"
        r = None
        r = requests.get(rstring)

        #parse api data
        data = parse(r)

        if data is not None:
            #update model with api data
            try:
                self.model.setData(data)
            except Exception:
                pass

    def run(self):
        self.dorun = True

        #wait to make request at start of minute
        t = time.localtime()
        while t.tm_sec != 0:
            time.sleep(1)
            t = time.localtime()
        
        while self.dorun == True:
            if self.update == True:
                #request new API data every minute
                self.request()
            time.sleep(60)
            
    def activate(self):
        self.update = True
        self.request()
    def inactivate(self):
        self.update = False

    def stop(self):
        self.dorun = False



def parse(data):
    try:
        d = data.json().get("Departure")
    except Exception:
        print("Failed to parse API data")
        return None

    table = [None] * len(d)

    for i in range(0, len(d)):
        table[i] = []
        table[i].append(d[i].get("transportNumber"))
        s = d[i].get("direction")
        if '(' in s:
            s = s[0:s.index('(')]
        table[i].append(s)
        table[i].append(d[i].get("time")[0:5])
           
    return table
