import sys
from datetime import datetime
import math
import suncalc
from geopy.geocoders import Nominatim
from constant import address

def get_coordinates():
    geolocator = Nominatim(user_agent="new_capstone_user_1234")
    location = geolocator.geocode(address)
    return location.longitude, location.latitude

def get_suncalc(longitude, latitude):
    date = datetime.now()
    position = suncalc.get_position(date, longitude, latitude)
    #print(math.degrees(position['azimuth']), math.degrees(position['altitude']))
    return math.degrees(position['azimuth']), math.degrees(position['altitude'])

def test_suncalc(longitude, latitude):
    date = datetime(2023, 2, 15, 10, 14, 0, 0)
    position = suncalc.get_position(date, longitude, latitude)
    print(math.degrees(position['azimuth']), math.degrees(position['altitude']))
    return math.degrees(position['azimuth']), math.degrees(position['altitude'])

def main():
    date = datetime.now()
    geolocator = Nominatim(user_agent="new_user_capstone+3")
    location = geolocator.geocode(address)
    test_suncalc(location)
    '''
    position = suncalc.get_position(date, location.longitude, location.latitude)
    print(math.degrees(position['azimuth']), math.degrees(position['altitude']))
    return'''

if __name__ == '__main__':
    main()
    