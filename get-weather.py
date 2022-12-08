import requests
#import optargs
import json
import os

# System call for Windows ANSI color support
os.system("")

class bcolors:
    """https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

an_address="179 N 450 W, American Fork, UT"

def get_coordinates(address: str) -> dict:
    """Returns latitude and longitude based on address (type string). If time permits, will account for:
        - multiple matches
        - non-matches
        - passing of non-string type args
    """
    response = requests.get(f"https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address}&benchmark=2020&format=json")
    coords = json.loads(response.content)['result']['addressMatches'][0]['coordinates']

    return coords

def convert_coordinates(coords: dict) -> dict:
    """Convert latitude and longitude into gridpoints weather.gov will understand"""
    response = requests.get(f"https://api.weather.gov/points/{coords['y']:.4f},{coords['x']:.4f}")
    properties = json.loads(response.content)['properties']
    gridpoints = {key: value for key, value in properties.items() if key.startswith('grid')}
    return gridpoints

def retrieve_current_weather(grid_values: dict) -> dict:
    """Feed weather.gov newly generated gridpoints, return current local weather"""
    response = requests.get(f"https://api.weather.gov/gridpoints/{grid_values['gridId']}/{grid_values['gridX']},{grid_values['gridY']}/forecast")
    current_local_weather = json.loads(response.content)['properties']['periods'][0]['detailedForecast']
    #print(json.dumps(current_local_weather, indent=4))
    print(f"{current_local_weather}")
    return

coordtest = get_coordinates(an_address)

converttest = convert_coordinates(coordtest)

weathertest = retrieve_current_weather(converttest)
