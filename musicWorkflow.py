import os
import csv
import pandas as pd
import boto3
from pydub import AudioSegment
from pydub.utils import mediainfo
from shutil import copyfile

def clear():
    os.system('cls')

s3 = boto3.client('s3')
dir1 = os.path.abspath(r'E:\flac')
dir2 = os.path.abspath(r'C:\Users\phwh9568\OneDrive - UCB-O365\UCB\Music\iTunes\iTunes Media\Music')


dirList = os.listdir(dir1)
artistList = []
albumList = []

for item in dirList:
    if item.endswith('.csv'):
        pass
    else:
        artistList.append(item)
# print(artistList)

inAlbums = pd.read_csv(os.path.join(dir1,'albumList.csv'))

inAlbumList = inAlbums['Album'].tolist()

with open(os.path.join(dir1,'albumList.csv'), 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    #writer.writerow(['Artist', 'Album']) only use this for first ever rip
    for artist in artistList:
        artistdir = os.path.join(dir1, artist)
        albums = os.listdir(artistdir)
        for album in albums:
            if album in inAlbumList:
                pass
            else:
                print(album, ' in progress...')
                files = os.listdir(os.path.join(dir1,artist,album))
                outdir = os.makedirs(os.path.join(dir2)+'/'+artist+'/'+album)
                #convert tracks from flac to mp3
                for file in files:
                    if file.endswith('flac'):
                        print(file,' conversion in progress')
                        filename = file[:-5]
                        flac = AudioSegment.from_file(os.path.join(dir1,artist,album,file), 'flac')
                        tags = mediainfo(os.path.join(dir1,artist,album,file)).get('TAG',None)
                        flac.export(os.path.join(dir2,artist,album,filename+'.m4a'), format='ipod', tags=tags)


                    #copy album art to mp3 folder
                    if file.endswith('jpg'):
                        print('image copied')
                        copyfile(os.path.join(dir1,artist,album,file), os.path.join(dir2,artist,album,file))

                clear()

                #update album list csv
                writer.writerow([artist, album])
                print(album,' conversion complete')

#this could be built into previous loop, but kept separate because
#these steps take longer and I might want to work on the new files while this is in progress
for artist in artistList:
    artistdir = os.path.join(dir1, artist)
    albums = os.listdir(artistdir)

    for album in albums:
        if album in inAlbumList:
            pass
        else:
            files = os.listdir(os.path.join(dir1,artist,album))

            #upload tracks to s3
            for file in files:
                print(file,' upload in progress...')
                s3.upload_file(os.path.join(dir1,artist,album,file), 'outpw-music', artist+'/'+album+'/'+file)
                clear()
                print(file,' complete')

            print(album,' upload complete')

#update AlbumList.csv on s3
s3.upload_file(os.path.join(dir1,'AlbumList.csv'), 'outpw-music', 'AlbumList.csv')
print('album list uploaded to s3 bucket')
