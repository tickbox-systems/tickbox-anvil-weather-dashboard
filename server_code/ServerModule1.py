import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
from datetime import datetime

@anvil.server.callable
def get_forecast_data(location):
  API_URL = f"http://api.openweathermap.org/data/2.5/forecast?lat={location['lat']}&lon={location['lon']}&appid={anvil.secrets.get_secret('api_key')}&units=metric"
  response = anvil.http.request(API_URL,json=True)
  # Extract forecast data
  times = [datetime.fromtimestamp(i['dt']) for i in response['list']]
  temps = [i['main']['temp'] for i in response['list']]
  # Extract summary data
  summary_data = {"temp_min": response['list'][0]['main']['temp_min'], 
                  "temp_max": response['list'][0]['main']['temp_max'], 
                  "description": response['list'][0]['weather'][0]['description'], 
                  "icon": response['list'][0]['weather'][0]['icon']}
  return times, temps, summary_data
