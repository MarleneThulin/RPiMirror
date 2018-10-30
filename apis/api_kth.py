from .api import *
import time
import icalendar
import datetime
from dateutil.tz import tzlocal

config = cfparser.ConfigParser()

class KTH_APIrequester(APIrequester):

    url = ''
    model = None
    dorun = False
    update_interval = 60*60
    max_items = 6
    datafile = None
    update = None

    def __init__(self, modelobj, active=True):
        super().__init__()
        config.read('./apis/apiconfig.ini')
        self.url = str(config['API_ICAL']['url'])
        self.model = modelobj
        self.model.setDataSize(rows=self.max_items, columns=4)
        self.update = active
        self.datafile = './apis/kth_ical_schedule.ics'
        
    def request(self):
        #get and store icalendar file
        
        res = requests.get(self.url, allow_redirects=True)

        try:
            open(self.datafile, 'wb').write(res.content)
        except Exception:
            print("Failed to save calendar data")

        data = parse(self.datafile)

        if data is not None:
            try:
                self.model.setData(data)
            except Exception:
                pass

    def run(self):
        self.dorun = True
        while self.dorun == True:
            if self.update ==True:
                self.request()
            time.sleep(self.update_interval)

    def activate(self):
        self.update = True
        self.request()
    def inactivate(self):
        self.update = False

    def stop(self):
        self.dorun = False

def formatEvent(veventobj):
    #format list row from icalendar vevent
    dateformat = '%d/%m'
    timeformat = '%H:%M'
    lastrow = []

    #adjust start and end to local time zone
    startdatetime = (veventobj['DTSTART'].dt).astimezone(tzlocal())
    enddatetime = (veventobj['DTEND'].dt).astimezone(tzlocal())

    #add start and end time to data 
    datestr = startdatetime.strftime(dateformat)
    timestr = startdatetime.strftime(timeformat) + " -\n" + enddatetime.strftime(timeformat) 

    lastrow.append(datestr)
    lastrow.append(timestr)

    #format and add summary to data
    summary = str(veventobj['SUMMARY'])
    course = summary[summary.find('(')+1:summary.find(')')]
    summary = summary[0:summary.find('-')]+'- '+course+'\n'+summary[summary.find('-')+1:summary.find('(')]
    lastrow.append(summary)

    try: 
        location = str(veventobj['LOCATION'])

        #put linebreak at 1st comma in second half of string
        i = int(len(location)//2)-1
        half2 = location[i:]
        j = half2.find(',')
        if j!=-1:
            location = location[0:i]+half2[0:j]+'\n'+half2[j+2:]

        #add location to data
        lastrow.append(location)
    except Exception:
        lastrow.append("")

    return lastrow
      
def parse(filename, max_items= 6, num_days=7):
    
    cal = None

    #try opening calendar file
    try:
        cal = icalendar.Calendar.from_ical(open(filename, 'rb').read())
    except Exception:
        print("Error: unable to open icalendar file")
        return None
    
    #get all event objects
    try:
        events = cal.walk('vevent')
    except Exception:
        print("Error: unable to parse icalendar data")
        return None

    table = []
    

    #get current time (timezone aware) and set delta for timespan to search from now
    curtime = datetime.datetime.now(tzlocal())
    delta = datetime.timedelta(days = num_days)

    #search through the list for events in chosen interval 
    for i in range (0, len(events)):

        starttime = (events[i]['DTSTART'].dt).astimezone(tzlocal())
    
        #return if all events in the time interval is already parsed
        if(starttime>curtime+delta) or len(table)==max_items:
            return table

        #skip past events
        if curtime.year>starttime.year:
            continue
        if curtime.year==starttime.year and curtime.month>starttime.month:
            continue
        if curtime.month == starttime.month and curtime.day>starttime.day:
            continue
        if curtime.day == starttime.day: #skip today's events if now is past endtime 
            endtime = (events[i]['DTEND'].dt).astimezone(tzlocal())
            if curtime.hour>endtime.hour: 
                continue
       
        #else add the event in a new data table row
        table.append(formatEvent(events[i]))
