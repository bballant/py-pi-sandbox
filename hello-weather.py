"""
Life is great
"""

import time
import urllib.request
import urllib.parse

from PIL import Image, ImageDraw

d = Image.new("RGB", (70, 9))
i = ImageDraw.Draw(d)
i.text((0, 0), "Hello World!")
d.save("a.png")

# You'll need to get a token from openweathermap.org, looks like:
# 'b6907d289e10d714a6e88b30761fae22'
OPEN_WEATHER_TOKEN = ""

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
LOCATION = "Manhattan, US"
DATA_SOURCE_URL = "http://api.openweathermap.org/data/2.5/weather"

if len(OPEN_WEATHER_TOKEN) == 0:
    raise RuntimeError("You fool!")
                                                                                
# Set up where we'll be fetching data from                                      
params = {"q": LOCATION, "appid": OPEN_WEATHER_TOKEN}                           
data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)

print(data_source)

response = urllib.request.urlopen(data_source)
if response.getcode() == 200:
    value = response.read()
    print("Response is", value)
else:
   print("Unable to retrieve data at {}".format(data_source))
