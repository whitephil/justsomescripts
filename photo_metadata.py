import pandas as pd
import geopandas as gpd
import os
from shapely.ops import nearest_points
from shapely.geometry import Point

os.chdir('E:\\Users\\phwh9568\\Photoindex_Metadata_py\\New')

filename = 'Bent_AG_20180124' #enter the filename, minus the file extension, as a string enclosed by quotes

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
photos['DDY'] = photos.apply((lambda row: dms2dd(row['DMSY'])), axis = 1)
photos['DDX'] = photos.apply((lambda row: dms2dd(row['DMSX'])), axis = 1)

#converts photos dataframe into a geodataframe by adding geometry
gdf = gpd.GeoDataFrame(photos, geometry=gpd.points_from_xy(photos.DDX, photos.DDY))
gdf.crs = {'init' :'epsg:4326'}

#import Colorado quads geojson file and drops unneeded columns
quads = gpd.read_file('CO_quads.geojson')
quads = quads[['USGS_QD_ID', 'QUAD_NAME', 'geometry']]

#import GNIS features and drop unneeded columns
places = gpd.read_file('CO_GNIS_SelectFeatures_201802.shp')
places = places[['FEATURE_NA', 'FEATURE_CL', 'MAP_NAME', 'geometry']]

#geppandas spatial join adds columns from quads to the photos geodataframe
photos_quads = gpd.sjoin(gdf, quads, how="inner", op='intersects')
photos_quads.drop(['index_right'], axis=1, inplace=True)

#creates a spatial index for the places gdf
places_index = places.sindex

#Creates bounding coordinates for the photos_quads dataframe
bounds = photos_quads.total_bounds

#Expands those bounds by .1 degree on all sides
bounds[0] = bounds[0] -.1
bounds[1] = bounds[1] -.1
bounds[2] = bounds[2] +.1
bounds[3] = bounds[3] +.1

#Near join between photos_quads & places. Note that the places df is over 300,000 points_from_xy
#This wil limit the amount of points to search through to only those that fall within the bounds (massive timesaver)
possible_matches_index = list(places_index.intersection(bounds))
possible_matches = places.iloc[possible_matches_index]
place_points = possible_matches.geometry.unary_union

#Nearest spatial join function
#Finds nearest in places possible matches and returns FEATURE_NA (landmark) and and FEATURE_CL (landmark type)
def near(point, pts=place_points):
    nearest = possible_matches.geometry == nearest_points(point, pts)[1]
    landmark = possible_matches[nearest].FEATURE_NA.get_values()[0]
    landmark_type = possible_matches[nearest].FEATURE_CL.get_values()[0]
    return landmark, landmark_type

#Applies near function to the photos_quads gdf
photos_quads['Landmark'] = photos_quads.apply(lambda row: near(row.geometry)[0], axis=1)
photos_quads['Landmark_type'] = photos_quads.apply(lambda row: near(row.geometry)[1], axis=1)

#drop unnecessary columns, rename columns appropriately, reset index, and export to csv
output = photos_quads.drop(['geometry'], axis=1)
output.rename(columns={"QUAD_NAME": "USGS_Topo_1_24000_Quad_Name"}, inplace=True)
output.set_index('Project-Roll-Frame', inplace=True)
output.to_csv(filename + '_geometa.csv')
