import pandas as pd
from math import radians, cos, sin, asin, sqrt
import geopy

def parseData(lat, lon, date):
    # Load the spreadsheet into a Pandas DataFrame
    df = pd.read_csv('data/weather/city_info.csv')
    
    # Define a function to calculate the distance between two sets of coordinates using the Haversine formula
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the earth in kilometers
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c
    
    # Calculate the distance between the input coordinates and each city in the DataFrame
    df['distance'] = df.apply(lambda row: haversine(lat, lon, row['Lat'], row['Lon']), axis=1)
    
    # Find the city with the smallest distance
    closest_city = df.loc[df['distance'].idxmin()]['ID']
    
    fpath = 'data/weather/' + str(closest_city) + '.csv'

    city_df = pd.read_csv(fpath)
    
    # Find the row in the DataFrame that matches the given date
    date_row = city_df.loc[city_df['Date'] == date]
    
    # If the row is found, return the corresponding temperature value
    if not date_row.empty:
        tmax = date_row.iloc[0]['tmax']
        tmin = date_row.iloc[0]['tmin']
        prcp = date_row.iloc[0]['prcp']
        return tmax, tmin, prcp

    # Otherwise, return an error message
    else:
        return "Temperature data not found for given date."
    

print(parseData(40.833458, -73.457279, '1869-01-01'))

