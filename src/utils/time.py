import dateutil.parser
import time, datetime

def string2timestamp(s):
    d = dateutil.parser.parse(s)
    t = d.timetuple()
    timeStamp = int(time.mktime(t))
    timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000
    return timeStamp