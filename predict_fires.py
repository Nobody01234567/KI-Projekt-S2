import pandas as pd
from datetime import datetime, timedelta


def iterate_days(start_year, end_year):
    start_date = datetime(start_year, 1, 1)  # Start date of the range
    end_date = datetime(end_year, 12, 31)    # End date of the range

    current_date = start_date
    while current_date <= end_date:
        print(current_date)
        current_date += timedelta(days=1)


def return_df(data_path):
    df = pd.read_csv(data_path)
    return df


def city_dataframes(weather_folder, start_year, end_year):

    info_df = pd.read_csv(weather_folder + '/city_info.csv')

    # create empty dict to store a dataframe and
    # coordinates of each city listed in 'city_info'

    city_dfs = {}

    for index, row in info_df.iterrows():

        city_id = row['ID']
        city_df = pd.read_csv(weather_folder + '/' + city_id + '.csv')
        city_lat = row['Lat']
        city_lon = row['Lon']
        city_dfs.setdefault(city_id, [])
        city_dfs[city_id].append(city_df)

        city_dfs[city_id].append(city_lat)
        city_dfs[city_id].append(city_lon)

    # the city_dfs dict contains data in the following format:
    # {city_id: [city_df, city_lat, city_lon], ...}

    return city_dfs


weather_df = city_dataframes('data/weather', 2000, 2000)

for key in weather_df:
    print(key)
