import pandas as pd
from math import radians, cos, sin, asin, sqrt
import geopy
import arrow



def parseData(lat, lon, date):
    # Load the spreadsheet into a Pandas DataFrame
    weather_df = pd.read_csv('data/weather/city_info.csv')
    fire_df = pd.read_csv('data/modis_2021_United_States.csv')
    
    # Define a function to calculate the distance between two sets of coordinates using the Haversine formula
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the earth in kilometers
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c
    
    # Calculate the distance between the input coordinates and each city in the DataFrame
    weather_df['distance'] = weather_df.apply(lambda row: haversine(lat, lon, row['Lat'], row['Lon']), axis=1)

    fire_df['distance'] = fire_df.apply(lambda row: haversine(lat, lon, row['latitude'], row['longitude']), axis=1)

    closest_fire = fire_df.loc[fire_df['distance'].idxmin()]


        


    # Find the city with the smallest distance
    # closest_city = weather_df.loc[weather_df['distance'].idxmin()]['ID']
    
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
    

# print(parseData(40.833458, -73.457279, '1869-01-01'))

def checkForFire(lat, lon, date):

    fire_df = pd.read_csv('data/modis_2021_United_States.csv')

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the earth in kilometers
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c 

    fire_df['distance'] = fire_df.apply(lambda row: haversine(lat, lon, row['latitude'], row['longitude']), axis=1)

    closest_fire = fire_df.loc[fire_df['distance'].idxmin()]

    closest_dist = closest_fire['distance']
    
    closest_date = arrow.get(closest_fire['acq_date'])
    
    delta = abs(closest_date - arrow.get(date))

    if closest_dist < 30 and delta.days < 10  :
        print('There has been a fire in this Area. It occured on ' + closest_fire['acq_date'] + ' and was ' + str(closest_dist) + ' km away from the specified coordinates. Coordinates: ' + str(closest_fire['latitude']) + ',' + str(closest_fire['longitude']) )        
    else:
        print('There has not been a fire in this Area during the specified date.')


checkForFire(46.789039, -100.787397, '1988-12-08')


