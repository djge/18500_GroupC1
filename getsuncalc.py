import sys
from datetime import datetime
import math
import suncalc
from geopy.geocoders import Nominatim
from constant import address

def get_suncalc(location):
    date = datetime.now()
    geolocator = Nominatim(user_agent="capstone")
    location = geolocator.geocode(location)
    position = suncalc.get_position(date, location.longitude, location.latitude)
    print(math.degrees(position['azimuth']), math.degrees(position['altitude']))
    return math.degrees(position['azimuth']), math.degrees(position['altitude'])

def test_suncalc(location):
    date = datetime(2023, 2, 15, 10, 14, 0, 0)
    geolocator = Nominatim(user_agent="capstone")
    location = geolocator.geocode(location)
    position = suncalc.get_position(date, location.longitude, location.latitude)
    print(math.degrees(position['azimuth']), math.degrees(position['altitude']))
    return math.degrees(position['azimuth']), math.degrees(position['altitude'])

def main():
    
    date = datetime.now()
    geolocator = Nominatim(user_agent="capstone")
    location = geolocator.geocode(address)
    test_suncalc(location)
    '''
    position = suncalc.get_position(date, location.longitude, location.latitude)
    print(math.degrees(position['azimuth']), math.degrees(position['altitude']))
    return'''

if __name__ == '__main__':
    main()
    