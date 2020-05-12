import requests
import json
import os
import csv
import pandas as pd
import time

os.chdir('C:\\Users\\phwh9568\\Music\\iTunes\\iTunes Media\\Music')
timestamp = time.strftime('%Y_%m_%d')

headers = {'User-Agent': 'philsScript/1.0'}

token = '&per_page=100&page=1&token=wAHenInXjcuQuuXhlPkEiviflCelGLFqHPEtonfN'

url = 'https://api.discogs.com/database/search?'

inventory = pd.read_csv('inventory_EditedAlbumNames.csv')

with open('albumYears'+timestamp+'.csv', 'a', newline='', encoding='utf-8') as f:
    writer=csv.writer(f)
    writer.writerow(['artist', 'album', 'year'])
    for index, row in inventory.iterrows():
        time.sleep(1)
        album = row['album'].replace(' ', '%20')
        artist = row['artist'].replace(' ', '%20')
        query =  url + 'title=' + album + '&artist=' + artist + token
        response = requests.get(query,headers=headers)
        data = json.loads(response.content.decode('utf-8'))
        if len(data['results']) > 0:
            if 'year' in data['results'][0]:
                year = data['results'][0]['year']
                writer.writerow([row['artist'],row['album'],year])
            else:
                writer.writerow([row['artist'],row['album'],'unknown'])
        else:
            writer.writerow([row['artist'],row['album'],'unknown'])
