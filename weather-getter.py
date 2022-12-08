import sys
import json
import os
import re
import requests
from requests.exceptions import HTTPError

# System call for Windows ANSI color support
os.system("")

class bcolors:
    """Pinch from https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def get_coordinates(address: str) -> dict:
    """Returns latitude and longitude based on address (type string). If time permits, will account for:
        - multiple matches
        - non-matches
        - passing of non-string type args
    """
    try:
        response = requests.get(f"https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address}&benchmark=2020&format=json")
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        if len(json.loads(response.content)['result']['addressMatches']) == 0:
            print("\n\tIt appears your inputed address is not found by census.gov.\n")
            return False
        else:
            coordinates = json.loads(response.content)['result']['addressMatches'][0]['coordinates']
            return coordinates


def convert_coordinates(coords: dict) -> dict:
    """Convert latitude and longitude into gridpoints weather.gov will understand"""
    try:
        response = requests.get(f"https://api.weather.gov/points/{coords['y']:.4f},{coords['x']:.4f}")
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        properties = json.loads(response.content)['properties']
        gridpoints = {key: value for key, value in properties.items() if key.startswith('grid')}
    
    return gridpoints


def retrieve_weather(grid_values: dict) -> dict:
    """Feed weather.gov newly generated gridpoints, return local weather"""
    try:
        response = requests.get(f"https://api.weather.gov/gridpoints/{grid_values['gridId']}/{grid_values['gridX']},{grid_values['gridY']}/forecast")
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        local_weather = json.loads(response.content)['properties']['periods']

    return local_weather


def help_statement() -> None:
    """Help statement, which prints to screen when no args are passed, or when 'help' arg is passed to script"""
    usage_string=f"'{bcolors.HEADER}COMMA DELINEATED ADDRESS{bcolors.OKBLUE}'"
    example_string="'1600 Pennsylvania Avenue NW, Washington, DC'"
    
    print(f"\n{bcolors.OKGREEN}Weather Getter Script:{bcolors.RESET} retrieve the weather forecast based on an address (USA only).")

    print(f"\n{'Basic Forecast:' : >19} {bcolors.OKBLUE} weather-getter {usage_string}{bcolors.RESET}")
    print(f"{'Example:' : >19} {bcolors.OKBLUE} weather-getter {example_string}{bcolors.RESET}   **note the commas\n")

    print(f"{'Extended Forecast:' : >19} {bcolors.OKBLUE} weather-getter 7d {usage_string}{bcolors.RESET}")
    print(f"{'Example:' : >19} {bcolors.OKBLUE} weather-getter 7d {example_string}{bcolors.RESET}\n")

    return None


def simple_regex_check(address: str) -> bool:
    """Slap-dash check for address formatting. This needs a better solution."""
    if re.search(",", address):
        return True
    else:
        return False


#________execution_below_______


if len(sys.argv) == 1 or 'help' in sys.argv:
    help_statement()

elif sys.argv[1] == '7d' and simple_regex_check(sys.argv[2]):
    _getcoords = get_coordinates(sys.argv[2])
    if _getcoords != False:
        _concoords = convert_coordinates(_getcoords)
        extended_local_weather = retrieve_weather(_concoords)

        print()
        for forecast in extended_local_weather:
            print(f"{bcolors.BOLD}{bcolors.OKCYAN}{forecast['name']}:{bcolors.RESET}\n{forecast['detailedForecast']}\n")
        print()

elif simple_regex_check(sys.argv[1]):
    _getcoords = get_coordinates(sys.argv[1])
    if _getcoords != False:
        _concoords = convert_coordinates(_getcoords)
        current_local_weather = retrieve_weather(_concoords)

        print(f"\n{bcolors.BOLD}{bcolors.OKCYAN}{current_local_weather[0]['name']}:{bcolors.RESET}\n{current_local_weather[0]['detailedForecast']}\n")
        print(f"{bcolors.BOLD}{bcolors.OKCYAN}{current_local_weather[1]['name']}:{bcolors.RESET}\n{current_local_weather[1]['detailedForecast']}\n")

else:
    help_statement()
    print(f"\n\t{bcolors.FAIL}{bcolors.BOLD}!!WARNING!!{bcolors.RESET}: It appears you may have malformed or misplaced arguments. Please follow the examples in the help text above.\n")
