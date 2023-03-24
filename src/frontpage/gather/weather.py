import requests

def main(config, logger, city, coords):
    """ Main function for this command """

    logger.debug('foo')
    # TODO: Guess we need a class?

    # return get_weather(config, city, coords)

def get_coords(config, city):
    """ Return coords[lat,lon] based on <city> if given, or IP address location if not """

    # If we don't have 'city' to work out coords from, then use ipinfo
    if city is None:
        config['logger'].debug("Fetching coords from ipinfo")
        return requests.get('https://ipinfo.io/').json()['loc'].split(',')

    # If we have 'city' to work out coords from, use the openweather API to get them
    config['logger'].debug('Fetching coords from openweathermap API')
    coords = []
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={config['openweather_token']}").json()
    coords.append(response[0]['lat'])
    coords.append(response[0]['lon'])

    return coords

def get_weather(config, city, coords):
    """ Return weather for <city> or <coords>, depending on which is given """

    coords = city or config.get('coords')
    city = coords or config.get('city')

    if coords is None and city is None:
        coords = get_coords(config, city=None)

    # response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={config['openweather_token']}").json()
    # return response
