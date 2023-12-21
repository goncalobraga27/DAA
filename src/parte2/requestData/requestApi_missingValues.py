import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 41.5518,
	"longitude": -8.4229,
	"start_date": "2023-03-15",
	"end_date": "2023-04-04",
	"hourly": ["temperature_2m", "relative_humidity_2m", "pressure_msl", "cloud_cover", "wind_speed_10m"],
	"daily": ["temperature_2m_max", "temperature_2m_min"],
	"timezone": "GMT"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_pressure_msl = hourly.Variables(2).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["pressure_msl"] = hourly_pressure_msl
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

hourly_dataframe = pd.DataFrame(data = hourly_data)
hourly_dataframe.rename(columns={'temperature_2m': 'temp'}, inplace=True)
hourly_dataframe.rename(columns={'relative_humidity_2m': 'humidity'}, inplace=True)
hourly_dataframe.rename(columns={'pressure_msl': 'pressure'}, inplace=True)
hourly_dataframe.rename(columns={'cloud_cover': 'clouds_all'}, inplace=True)
hourly_dataframe.rename(columns={'wind_speed_10m': 'wind_speed'}, inplace=True)
hourly_dataframe['Data'] = hourly_dataframe['date'].dt.strftime('%Y-%m-%d')
hourly_dataframe['Hora'] = hourly_dataframe['date'].dt.strftime('%H')
hourly_dataframe['Hora'] = hourly_dataframe['Hora'].astype(int)
hourly_dataframe = hourly_dataframe.drop('date',axis = 1)


# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s"),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min

daily_dataframe = pd.DataFrame(data = daily_data)
daily_dataframe.rename(columns={'temperature_2m_max': 'temp_max'}, inplace=True)
daily_dataframe.rename(columns={'temperature_2m_min': 'temp_min'}, inplace=True)
daily_dataframe.rename(columns={'date': 'Data'}, inplace=True)
daily_dataframe['Data'] = pd.to_datetime(daily_dataframe['Data'])
daily_dataframe['Data'] = daily_dataframe['Data'].dt.strftime('%Y-%m-%d')


df = pd.merge(hourly_dataframe,daily_dataframe, on='Data', how='inner')

new_min = 0
new_max = 100
df['clouds_all'] = ((df['clouds_all'] - df['clouds_all'].min()) /
                            (df['clouds_all'].max() - df['clouds_all'].min()) *
                            (new_max - new_min) + new_min)
df.to_csv('../../../datasets/parte2/teste/missingWeatherData.csv', index=False)

