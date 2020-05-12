import requests
import json
import pandas as pd
import csv
from time import sleep
import os

# Set the working directory. Double slashes required for windows, single slashes fine for mac
os.chdir('C:\\Users\\phwh9568\\Geocode')

# the url for the mapquest api
# if you want to query the mapbquest "open" api, replace the "www" in this url with "open"
url = 'http://www.mapquestapi.com/geocoding/v1/address?'

# the api key + the beginning of the location query
# PASTE IN YOUR KEY AND BE SURE TO LEAVE "&location=" RIGHT AFTER
keyLoc = 'key=YOUR KEY HERE&location='

# imports the input csv into a pandas dataframe, csv should have "Address" as header and full addresses in each row
data = pd.read_csv('BoulderDisp.csv')

with open('BoulderDisp_GeocodedResults_test.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['precinct','address', 'latitude', 'longitude', 'geocode quality code', 'geocode quality'])
    for index, row in data.iterrows():
        sleep(0.1)
        query = url + keyLoc + row['Address']
        response = requests.get(query)
        jsonContents = json.loads(response.content.decode('utf-8'))
        if len(jsonContents['results'])>0:
            writer.writerow([row['Precinct'], row['Address'],
                        jsonContents['results'][0]['locations'][0]['latLng']['lat'],
                        jsonContents['results'][0]['locations'][0]['latLng']['lng'],
                        jsonContents['results'][0]['locations'][0]['geocodeQualityCode'],
                        jsonContents['results'][0]['locations'][0]['geocodeQuality'],
                        query])
        else: writer.writerow(['No Data'])


# The loop above creates a new output csv,
# iterates through list of addresses building a new query for each,
# sends a query every 1.5 seconds,
# parses json response,
# writes address, lat, long, and query url into rows of the output csv
# appends new row to output csv for each response
# if the response contains no data, writes "no data" into first cell of row
