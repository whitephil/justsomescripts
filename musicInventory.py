import glob
import csv
import os
import time

os.chdir('C:\\Users\\phwh9568\\Music\\iTunes\\iTunes Media\\Music')

timestamp = time.strftime('%Y_%m_%d')

folders = glob.glob('*')

with open('inventory'+timestamp+'.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['artist','album'])
    for artist in folders:
        albums = glob.glob(artist+'\\*')
        for album in albums:
            try:
                album = album.split('\\')[1]
            except:
                pass
            writer.writerow([artist,album])
