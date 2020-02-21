"""
Contains model objects used throughout the library.
"""


# ****************************************************************
# Weather objects
# ****************************************************************
class Weather:
    """
    Represents weather at a certain point in time.
    This class can be used for both current weather and weathers
    in the "list" of the WeatherForecast class.
    """
    def __init__(self, coord = {}, weather = [], base = '', main = {}, visibility = -1, wind = {}, clouds = {}, rain = {}, snow = {}, dt = -1, sys = {}, timezone = -1, id = -1, name = '', cod = -1, dt_txt = ''):
        self.coord = coord
        self.weather = weather
        self.base = base
        self.main = main
        self.visibility = visibility
        self.wind = wind
        self.clouds = clouds
        self.rain = rain
        self.snow = snow
        self.dt =dt
        self.sys = sys
        self.timezone = timezone
        self.id = id
        self.name = name
        self.cod = cod
        self.dt_txt = dt_txt

class WeatherForecast:
    "Represents a collection of weathers forecasts, each represented as a Weather object."
    def __init__(self):
        self.list = []		# List of Weather objects
        # Other metadata common to all weathers in the list
        self.cod = 0
        self.message = 0
        self.cnt = -1		# Number of mesurements returned (remember that there are max 40 mesurements (every 3 hours for 5 days = 40 mesurements))  slef.cnt == len(self.list)
        self.city = {}





# ****************************************************************
# Request objects
# ****************************************************************
class RequestParameters:
    "Parameters for a GET request to the API."
    def __init__(self, api_key = '', endpoint = '', city_id = '', city_name = '', lat = '', lon = '', zip_code = '', mode = '', units = '', language = ''):
        self.api_key = api_key
        self.endpoint = endpoint
        self.city_id = city_id
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        self.zip_code = zip_code
        self.mode = mode
        self.units = units
        self.language = language