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
	"start_date": "2023-01-01",
	"end_date": "2023-04-04",
    "hourly": ["shortwave_radiation", "direct_radiation", "diffuse_radiation", "direct_normal_irradiance", "terrestrial_radiation", "shortwave_radiation_instant", "direct_radiation_instant", "diffuse_radiation_instant", "direct_normal_irradiance_instant", "terrestrial_radiation_instant"],
	"daily": "shortwave_radiation_sum",
	"timezone": "GMT"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_shortwave_radiation = hourly.Variables(0).ValuesAsNumpy()
hourly_direct_radiation = hourly.Variables(1).ValuesAsNumpy()
hourly_diffuse_radiation = hourly.Variables(2).ValuesAsNumpy()
hourly_direct_normal_irradiance = hourly.Variables(3).ValuesAsNumpy()
hourly_terrestrial_radiation = hourly.Variables(4).ValuesAsNumpy()
hourly_shortwave_radiation_instant = hourly.Variables(5).ValuesAsNumpy()
hourly_direct_radiation_instant = hourly.Variables(6).ValuesAsNumpy()
hourly_diffuse_radiation_instant = hourly.Variables(7).ValuesAsNumpy()
hourly_direct_normal_irradiance_instant = hourly.Variables(8).ValuesAsNumpy()
hourly_terrestrial_radiation_instant = hourly.Variables(9).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
hourly_data["direct_radiation"] = hourly_direct_radiation
hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
hourly_data["terrestrial_radiation"] = hourly_terrestrial_radiation
hourly_data["shortwave_radiation_instant"] = hourly_shortwave_radiation_instant
hourly_data["direct_radiation_instant"] = hourly_direct_radiation_instant
hourly_data["diffuse_radiation_instant"] = hourly_diffuse_radiation_instant
hourly_data["direct_normal_irradiance_instant"] = hourly_direct_normal_irradiance_instant
hourly_data["terrestrial_radiation_instant"] = hourly_terrestrial_radiation_instant


hourly_dataframe = pd.DataFrame(data = hourly_data)
hourly_dataframe['Data'] = hourly_dataframe['date'].dt.strftime('%Y-%m-%d')
hourly_dataframe['Hora'] = hourly_dataframe['date'].dt.strftime('%H')
hourly_dataframe['Hora'] = hourly_dataframe['Hora'].astype(int)
hourly_dataframe = hourly_dataframe.drop('date',axis = 1)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_shortwave_radiation_sum = daily.Variables(0).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s"),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum

daily_dataframe = pd.DataFrame(data = daily_data)
daily_dataframe.rename(columns={'date': 'Data'}, inplace=True)
daily_dataframe['Data'] = pd.to_datetime(daily_dataframe['Data'])
daily_dataframe['Data'] = daily_dataframe['Data'].dt.strftime('%Y-%m-%d')

df = pd.merge(hourly_dataframe,daily_dataframe, on='Data', how='inner')
df.to_csv('../../../datasets/parte2/teste/radiation.csv', index=False)