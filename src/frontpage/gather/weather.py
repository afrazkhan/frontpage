import requests
import sys

class Weather():
    """ TODO """

    def __init__(self, logger, config, city, coords):
        self.logger = logger
        self.config = config
        self.coords = coords or self.config.get('coords')
        self.city = city or self.config.get('city')

        try:
            self.openweather_token = self.config['openweather_token']
        except KeyError as e:
            self.logger.error(f"No openweather token found in configuration: {e}")
            sys.exit(1)

    def get_coords(self, config, city):
        """ Return coords[lat,lon] based on <city> if given, or IP address location if not """

        # If we don't have 'city' to work out coords from, then use ipinfo
        if city is None:
            self.logger.debug("Fetching coords from ipinfo")
            return requests.get('https://ipinfo.io/').json()['loc'].split(',')

        # If we have 'city' to work out coords from, use the openweather API to get them
        self.logger.debug('Fetching coords from openweathermap API')
        coords = []
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={config['openweather_token']}").json()
        coords.append(response[0]['lat'])
        coords.append(response[0]['lon'])

        return coords

    def main(self):
        """ Return weather for <city> or <coords>, depending on which is given """

        if self.coords is None:
            self.logger.debug('coords not found in arguments, using get_coords()')
            coords = self.get_coords(self.config, self.city)

        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={self.openweather_token}&units=metric").json()
        return response
