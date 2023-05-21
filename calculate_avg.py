import pandas as pd
import numpy as np
from searchdata import *
import dateutil
from dateutil.relativedelta import *
from datetime import datetime, timedelta

def avgtemp(lat, lon, date):
    
    dt = pd.to_datetime(date)
    tmaxtotal = 0
    tmintotal = 0
    count = 0

    for i in range(2):
        ldate = dt - timedelta(days= i * 1)
        tmax = int(parseTmax(lat, lon, ldate.strftime("%Y-%m-%d")))
        tmin = int(parseTmin(lat, lon, ldate.strftime("%Y-%m-%d")))

        if not np.isnan(tmax):
            tmaxtotal += int(tmax)
            count += 1

        if not np.isnan(tmin):
            tmintotal += int(tmin)
            count += 1

        # print(ldate)
        # print(tmaxtotal)

    if count > 0:
        avgtemp = (tmaxtotal + tmintotal) / (2 * count)
    else:
        avgtemp = np.nan

    # print(avgtemp)
    return avgtemp

