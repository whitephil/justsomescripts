import pandas as pd
import geopandas as gpd
import os
from shapely.ops import nearest_points
from shapely.geometry import Point

os.chdir('C:\\Users\\phwh9568\\Photoindex_Metadata_py\\New\\May2020')

filename = 'Weld_20200430132018' #enter the filename, minus the file extension, as a string enclosed by quotes

photos = pd.read_csv(filename + '.csv')

#dms to decimal degrees converter function
def dms2dd(dms):
    if dms[0]=='-':
        dms = dms.split('-')[1]
        DEG = int(dms.split(' ')[0])
        MIN = int(dms.split(' ')[1])
        SEC = int(dms.split(' ')[2])
        DD = float('-' + str(DEG + (MIN *1/60) + (SEC * 1/60 * 1/60)))
    elif dms[0]!='-':
        DEG = int(dms.split(' ')[0])
        MIN = int(dms.split(' ')[1])
        SEC = int(dms.split(' ')[2])
        DD = float(DEG + (MIN *1/60) + (SEC * 1/60 * 1/60))
    return DD

#dms2dd applied across values in photos dataframe to new columns DMSY and DMSX
photos['DDLat'] = photos.apply((lambda row: dms2dd(row['Center Point Latitude#1'])), axis = 1)
photos['DDLon'] = photos.apply((lambda row: dms2dd(row['Center Point Longitude#1'])), axis = 1)

photos.to_csv(filename+'_DD.csv')
