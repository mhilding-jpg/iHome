# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from urllib.request import urlopen
import json
import time
READ_API_KEY = 'YCW7RBBBL5I33G16' # Change this to your READ_API_KEY
CHANNEL_ID = '3312636' # Change this to your CHANNEL_ID
unoR4 = "https://api.thingspeak.com/channels/"+CHANNEL_ID+"/feeds.json?api_key="+READ_API_KEY
TS = urlopen(unoR4) # Change the URL to your read URL
response = TS.read( ) #Request the url
data = json.loads(response) # Get the response of the web server
feeds = data["feeds"] # The data are here, check it.
# It is also possible to read the values from one fields
field1 = "https://api.thingspeak.com/channels/"+CHANNEL_ID+"/fields/1.json?api_key="+READ_API_KEY
TS_1 = urlopen(unoR4) # Change the URL to your read URL
response_1 = TS_1.read( ) #Request the url
data_1 = json.loads(response_1) # Get the response of the web server
feeds_1 = data_1["feeds"] # The data are here, check it.
print(feeds_1)