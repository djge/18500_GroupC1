import sys
from datetime import datetime
import math
import suncalc
from geopy.geocoders import Nominatim
from constant import address

def get_suncalc(location):
    date = datetime.now()
    geolocator = Nominatim(user_agent="capstone")
    location = geolocator.geocode(location, timeout=None)
    position = suncalc.get_position(date, location.longitude, location.latitude)
    alt = math.degrees(position['altitude'])
    azi = math.degrees(position['azimuth'])
    print(azi + 180, alt)
    return azi + 180, alt

def test_suncalc(location):
    date = datetime(2023, 4, 26, 17, 0, 0, 0)
    geolocator = Nominatim(user_agent="capstone")
    location = geolocator.geocode(location, timeout=None)
    position = suncalc.get_position(date, location.longitude, location.latitude)
    alt = math.degrees(position['altitude'])
    azi = math.degrees(position['azimuth'])
    print(azi, alt)
    return azi + 180, alt

def main():
    
    date = datetime.now()
    geolocator = Nominatim(user_agent="capstone")
    location = geolocator.geocode(address, timeout=None)
    #get_suncalc(location)
    test_suncalc(location)
    '''
    position = suncalc.get_position(date, location.longitude, location.latitude)
    print(math.degrees(position['azimuth']), math.degrees(position['altitude']))
    return'''

if __name__ == '__main__':
    main()
    