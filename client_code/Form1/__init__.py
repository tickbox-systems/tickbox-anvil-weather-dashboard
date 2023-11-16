from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from anvil.js.window import navigator

Plot.templates.default = "rally"

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Initialize location to Cambridge, UK
    self.set_location(52.205, 0.1218)
    
  def refresh(self):
    times, temps, summary_data = anvil.server.call('get_forecast_data', self.location)
    self.plot_1.data = go.Scatter(x=times, y=temps)
    self.plot_1.layout.title = "5-day Forecast" 
    self.temp_label.text = f"{temps[0]}°C"
    self.min_label.text = f"L:{summary_data['temp_min']}°C"
    self.max_label.text = f"H:{summary_data['temp_max']}°C"
    self.description_label.text = summary_data['description'].capitalize()
    self.icon.source = f"https://openweathermap.org/img/wn/{summary_data['icon']}@4x.png"

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.refresh()

  def set_location(self, lat, lon):
    self.location = {"lat": lat, "lon": lon}
    self.location_label.text = f"Showing weather forecast for {lat}, {lon}."
    self.refresh()
    
  def location_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    navigator.geolocation.getCurrentPosition(lambda p: self.set_location(p.coords.latitude, p.coords.longitude))
    self.location_button.enabled = False


    
    
