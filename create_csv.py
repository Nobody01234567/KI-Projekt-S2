import pandas as pd
from calculate_avg import *

def create_data_2021():
    # Load the spreadsheets into pandas dataframes
    city_id = 'USW00023271'
    modis_df = pd.read_csv('data/modis_2021_United_States.csv')
    weather_df = pd.read_csv('data/weather/' + city_id + '.csv')
    city_info_df = pd.read_csv('data/weather/city_info.csv')

    # Find the coordinates for the given weather spreadsheet
    city_filename = 'weather_data.csv'
    city_row = city_info_df[city_info_df['ID'] == city_id]
    latitude = float(city_row['Lat'].values[0])
    longitude = float(city_row['Lon'].values[0])

    print("Latitude:", latitude)
    print("Longitude:", longitude)

    # Convert 'Date' column to datetime format
    weather_df['Date'] = pd.to_datetime(weather_df['Date'])

    # Create an empty dataframe for data_2021
    data_2021 = pd.DataFrame(columns=['date', 'fire', 'temperature', 'precipitation'])

    # Load dates of the weather data for the year 2021 into the dataframe
    data_2021['date'] = pd.date_range('2021-01-01', '2021-12-31')

    # Load precipitation data into the 'precipitation' column
    data_2021['precipitation'] = weather_df.loc[weather_df['Date'].dt.year == 2021, 'prcp'].values

    print("Precipitation data:")
    print(data_2021['precipitation'])

    # Calculate average temperature for each day and insert into 'temperature' column
    data_2021['temperature'] = data_2021['date'].apply(lambda date: avgtemp(latitude, longitude, date))

    print("Temperature data:")
    print(data_2021['temperature'])

    # Check for fire using checkForFire() function and insert boolean values into 'fire' column
    data_2021['fire'] = data_2021['date'].apply(lambda x: checkForFire(latitude, longitude, x, modis_df))

    # Save the dataframe to a new CSV file
    data_2021.to_csv('data_2021.csv', index=False)

def weather_2021():    
    weather_df = pd.read_csv('data/weather/USW00023271.csv')
    weather_df['Date'] = pd.to_datetime(weather_df['Date'])
    weather_2021 = weather_df[weather_df['Date'].dt.year == 2021]
    weather_2021.to_csv('USW00023271_2021.csv', index=False)

# weather_2021()
create_data_2021()
