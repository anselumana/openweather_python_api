import json
import requests
from openweather_python_api.object_model import Weather, WeatherForecast, RequestParameters



class WeatherApi:
    """
    This class represents the object through which to access the API.
    
    API calls are made through the "update" method, which accepts a parameter
    that allows to configure the web request.
    You can also choose to use parameters from the config file.

    Calling "update" will store weather objects as instance fields.
    """

    def __init__(self):
        # Public fields
        self.current_weather = Weather()
        self.forecast_weather = WeatherForecast()
        # Private(pseudo) fields
        self.__request_parameters = RequestParameters()


    # ****************************************************************
    # "update" method and pseudo-private helpers
    # ****************************************************************
    def update(self, request_parameters = None):
        """
        Do a web request to an API endpoint.
        URL composition is made with values from the parameters dict.
        The json data returned is used to create the corresponding weather
        object in the object model which is then stored as an instance field.

        Returns:
            - None
        """
        # Validate parameters
        if not self.__validate_parameters(request_parameters):
            raise Exception('Invalid parameters!')

        self.__request_parameters = request_parameters
        
        # Compose the url string for the request
        url = self.__compose_url()
        # API call
        res = requests.get(url)

        if self.__is_request_for_current_weather():
            self.current_weather = self.__build_weather(res.json())
        elif self.__is_request_for_forecast_weather():
            self.forecast_weather = self.__build_forecast_weather(res.json())


    # Section: request parameters
    def __validate_parameters(self, request_parameters):
        "Returns True if valid else False. (Basically makes sure all mandatory parameters are present)."
        res = True
        if request_parameters is None:
            res = False
        else:
            if not  request_parameters.api_key:
                res = False
            if not  request_parameters.endpoint:
                res =  False
            if not request_parameters.city_id and not request_parameters.city_name and (request_parameters.lat == request_parameters.lon == '') and not request_parameters.zip_code:
                res = False
        return res
    
    # Section: URL composition
    def __compose_url(self):
        "Returns a url build with data from the config file and self.parameters."
        url = ''
        url += self.__request_parameters.endpoint + '?'  # base endpoint
        url += self.__get_api_key_query_string() + '&'   # api key query string
        url += self.__get_city_query_string() + '&'      # city query string
        url += self.__get_mode_query_string() + '&'      # mode query string
        url += self.__get_units_query_string() + '&'     # units query string
        url += self.__get_language_query_string() + '&'  # language query string
        return url

    def __get_api_key_query_string(self):
        "Returns the API key query string."
        return 'APPID=' + self.__request_parameters.api_key

    def __get_units_query_string(self):
        "Returns the units query string for the request. Can be 'standard', 'metric', or '???'."
        return 'units=' + self.__request_parameters.units

    def __get_language_query_string(self):
        "Returns the language query string of the request."
        return 'lang=' + self.__request_parameters.language

    def __get_city_query_string(self):
        """
        Returns the query string for the city.
        In the API a location can be defined as its id, name, coordinates (lat, lon) or zip code.
        This is also the order of choice if more thatn one is present in the self.parameters.
        """
        query_string = ''
        if self.__request_parameters.zip_code:
            query_string = 'zip=' + self.__request_parameters.zip_code
        if self.__request_parameters.lat and self.__request_parameters.lon:
            query_string = 'lat=' + self.__request_parameters.lat + '&' + 'lon=' + self.__request_parameters.lon
        if self.__request_parameters.city_name:
            query_string = 'q=' + self.__request_parameters.city_name
        if self.__request_parameters.city_id:
            query_string = 'id=' + self.__request_parameters.city_id
        return query_string

    def __get_mode_query_string(self):
        "Returns the mode query string of the request. Can be 'json', 'xml', or 'html'."
        return 'mode=' + self.__request_parameters.mode

    # Section: determining current vs forecast weather
    def __is_request_for_current_weather(self):
        # Get the last part of the endpoint
        endpoint = self.__request_parameters.endpoint.split('/')[-1]
        return True if endpoint == 'weather' else False

    def __is_request_for_forecast_weather(self):
        # Get the last part of the endpoint
        endpoint = self.__request_parameters.endpoint.split('/')[-1]
        return True if endpoint == 'forecast' else False

    # Section: Building objects from dictionaries
    def __build_weather(self, json_dict):
        "Returns a Weather object from the json dictionary."
        current_weather = Weather()
        for key in json_dict:
            setattr(current_weather, key, json_dict[key])
        return current_weather

    def __build_forecast_weather(self, json_dict):
        "Returns a ForecastWeather object from the json dictionary."
        forecast_weather = WeatherForecast()
        for key in json_dict:
            if key == 'list':
                # Build a list of Weather objects
                weather_list = self.__build_weather_list(json_dict[key])
                setattr(forecast_weather, key, weather_list)
                continue
            setattr(forecast_weather, key, json_dict[key])
        return forecast_weather
        
    def __build_weather_list(self, weather_list):
        "Returns a list of Weather objects from a list of dictionaries."
        final_list = []
        for weather in weather_list:
            final_list.append(self.__build_weather(weather))
        return final_list



if __name__ == '__main__':
    api = WeatherApi()
