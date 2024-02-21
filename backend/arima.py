# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.eval_measures import rmse
import requests

# Function to fetch data from the NASA EONET API
def fetch_eonet_data():
    url = 'https://eonet.gsfc.nasa.gov/api/v3/events'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Failed to fetch data from the EONET API')
        return None

# Function to extract relevant time series data from the fetched data
def extract_time_series_data(eonet_data):
    # Process the data as needed to extract time series data
    # For example, extract relevant events and their dates
    # Here, we'll simply create a placeholder dataframe with dummy data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31')
    values = [0] * len(dates)
    time_series_data = pd.DataFrame({'Date': dates, 'Value': values})
    return time_series_data

# Fetch data from the EONET API
eonet_data = fetch_eonet_data() #! current error, fetch_eonet_data creates errors

# Extract time series data from the fetched data
time_series_data = extract_time_series_data(eonet_data)

# Visualize the time series data
plt.figure(figsize=(10, 6))
plt.plot(time_series_data['Date'], time_series_data['Value'])
plt.title('Time Series Data')
plt.xlabel('Date')
plt.ylabel('Value')
plt.show()

# Fit an ARIMA model
# Specify the order (p, d, q) parameters based on analysis of the time series data
p = 1  # Autoregressive (AR) order
d = 1  # Differencing (I) order
q = 1  # Moving average (MA) order

model = ARIMA(time_series_data['Value'], order=(p, d, q))
results = model.fit()

# Forecast future values
forecast_steps = 10  # Change this value as needed
forecast = results.forecast(steps=forecast_steps)

# Plot the forecast
plt.figure(figsize=(10, 6))
plt.plot(time_series_data['Date'], time_series_data['Value'], label='Actual')
plt.plot(time_series_data['Date'].iloc[-1] + pd.to_timedelta(range(1, forecast_steps + 1), 'D'), forecast, label='Forecast')
plt.title('Time Series Forecast')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()

# Evaluate the forecast
# For example, calculate RMSE
actual_values = time_series_data['Value'].iloc[-forecast_steps:]
forecast_values = results.predict(start=len(time_series_data), end=len(time_series_data) + forecast_steps - 1)
forecast_rmse = rmse(actual_values, forecast_values)
print('Forecast RMSE:', forecast_rmse)
