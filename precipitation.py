import pandas as pd
from searchdata import *
import dateutil
from dateutil.relativedelta import *
from datetime import datetime, timedelta

def humidity(lat, lon, date):
    
    dt = pd.to_datetime(date)
    tmaxtotal = 0
    tmintotal = 0

    for i in range(30):
        ldate = dt - timedelta(days= i * 1)
        tmaxtotal += int(parseTmax(lat, lon, ldate.strftime("%Y-%m-%d")))
        tmintotal += int(parseTmin(lat, lon, ldate.strftime("%Y-%m-%d")))

        print(ldate)
        print(tmaxtotal)

    avgtemp = (((tmaxtotal)/30) + ((tmintotal)/30))/2

    print(avgtemp)

humidity(46.789039, -100.787397, '2020-03-20')
