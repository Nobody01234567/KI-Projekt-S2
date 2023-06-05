import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from searchdata import checkForFire, load_fire_data


def iterate_days(start_year, end_year):
    start_date = datetime(start_year, 1, 1)  # Start date of the range
    end_date = datetime(end_year, 12, 31)    # End date of the range

    current_date = start_date
    while current_date <= end_date:
        print(current_date)
        current_date += timedelta(days=1)

def check_fire(row, lat, lon):
    return 1 if checkForFire(lat, lon, row.Date) else 0


def add_fire_column(city_df, lat, lon):
    # Add a new column 'fire' initialized with 0
    city_df['fire'] = 0

    # Load fire data

    # Apply the checkForFire() function to each row in the DataFrame
    city_df['fire'] = city_df.apply(lambda row: check_fire(row, lat, lon), axis=1)

    return city_df


def add_fire_column_old(city_df, lat, lon):
    # Add a new column 'fire' initialized with 0
    city_df['fire'] = 0

    with ThreadPoolExecutor() as executor:
        # Apply the checkForFire() function to each row in the DataFrame
        results = list(executor.map(lambda row: check_fire(row, lat, lon, fire_data), city_df.itertuples()))

    city_df['fire'] = results

    return city_df

def filter_dataframe_by_years(df, start_year, end_year):
    # Convert the date column to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter the DataFrame based on the specified years
    df = df.query(f"{start_year} <= Date.dt.year <= {end_year}").copy()

    return df



def return_df(data_path):
    df = pd.read_csv(data_path)
    return df

# @profile
def city_dataframes(weather_folder, start_year, end_year):

    info_df = pd.read_csv(weather_folder + '/city_info.csv')

    # create empty dict to store a dataframe and
    # coordinates of each city listed in 'city_info'

    city_dfs = {}

    for index, row in info_df.iterrows():

        city_id = row['ID']
        city_df = pd.read_csv(weather_folder + '/' + city_id + '.csv')
        # keep only the data that is between the two given years
        city_df = filter_dataframe_by_years(city_df, start_year, end_year)
        city_lat = row['Lat']
        city_lon = row['Lon']

        # adds a column to the city_df that states
        # if there has been a fire on that day
        city_df = add_fire_column(city_df, city_lat, city_lon)

        city_dfs.setdefault(city_id, [])
        city_dfs[city_id].append(city_df)

        city_dfs[city_id].append(city_lat)
        city_dfs[city_id].append(city_lon)

    # the city_dfs dict contains data in the following format:
    # {city_id: [city_df, city_lat, city_lon], ...}

    return city_dfs


print(city_dataframes('data/weather', 2021, 2021))
