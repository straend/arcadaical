__author__ = 'slo'
import xmltodict
import icalendar
from datetime import datetime
import urllib
from pytz import timezone

class Fulcalendar():

    def __init__(self):
        self.cal = icalendar.Calendar()
        self.cal.add('prodid', '-//arbs by fik1//fik1.net//')
        self.cal.add('version', '0.91')
        self.BASE_URL_ARBS="https://famnen.arcada.fi/arbs/ws/arbs_ws.php?service=1&code=%s&group=%s"
        self.tz = timezone('Europe/Helsinki')

    def addCourse(self, course, group=0):
        url = self.getarbsurl(course, group)
        print(url)
        f = urllib.request.urlopen(url)
        xmltodict.parse(f, item_depth=2, item_callback=self.handle_booking)
        f.close()

    def getarbsurl(self, course, group):
        return (self.BASE_URL_ARBS %(course, group))

    def handle_booking(self, a, booking):
        if type(booking) is str:
            return True
        now = datetime.now(tz=self.tz)
        start = datetime.strptime(booking['start']['@time'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(booking['end']['@time'], "%Y-%m-%d %H:%M:%S")

        event = icalendar.Event()
        event['uid'] = a[1][1]["id"]
        event.add('dtstamp', now)
        event.add('summary', booking['title']['#text'])
        event.add('dtstart', self.tz.localize(start))
        event.add('dtend', self.tz.localize(end))

        if "#text" in booking['room']:
            event['location']= booking['room']['#text']

        info=""
        if None is not booking["info"]:
            info ="%s\n" % booking["info"]

        teachers="Teachers:"
        for t in booking['teachers'].items():
            if isinstance(t[1], list):
                for te in t[1]:
                    teachers = "%s\n%s"%(teachers,te["#text"])
            else:
                teachers = "%s\n%s" %(teachers, t[1]["#text"])

        event['description']="%s%s"%(info,teachers)

        self.cal.add_component(event)

        return True

    def getCal(self):
        return self.cal
