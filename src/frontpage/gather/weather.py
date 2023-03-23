import requests

def main(config, city, coords):
    """ Main function for this command """

    return get_weather(config, city, coords)

def get_coords(config, city):
    """ Return coords[lat,lon] based on <city> if given, or IP address location if not """

    if city is None:
        return requests.get('https://ipinfo.io/').json()['loc'].split(',')

    coords = []
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={config['openweather_token']}").json()
    coords.append(response[0]['lat'])
    coords.append(response[0]['lon'])

    return coords

def get_weather(config, city, coords):
    """ Return weather for <city> or <coords>, depending on which is given """

    if coords is None and config.get('coords') is None and config.get('city') is None:
        coords = get_coords(config, city)
    else:
        coords = coords.split(',')

    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={config['openweather_token']}").json()
    return response
