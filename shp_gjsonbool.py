import geopandas as gpd
import os
import glob
import json

#This Python script iterates over index map shapefiles and transforms them to geojson format,
#and converts appropriate attributes to json boolean values.
#Your input shapefiles should follow the Open Index Map project GIS Index Map Creation Requirements and Recommendations document.

os.chdir('E:\\path\\to\\your\\data\\directory')
#this top level folder should contain two more folders: 'Pre_Conversion' and 'Post_Conversion'.
#Pre_Conversion should have all the shapefiles you need to convert. Post_Conversion should be empty.
#note: I wrote this on windows, which requires a double slash, unix or mac can use single slashes in file paths, I think(?)

og_data = glob.glob('Pre_Conversion\\*.shp') #reads your files in the Pre folder

#The loop below reads each shapefile in the Pre folder, and converts it to geojson using geopandas
#Then it reads the geojson using the json library and converts appropriate fields to boolean values
#finally, it writes an updated geojson file w/ boolean attributes to the Post folder
#If any of the three boolean fields ('available', 'contLines', 'photomos') are absent it will ignore those fields.
for f in og_data:
    shapefile = gpd.read_file(f)
    newfile = f.split('.shp')[0] + '.geojson'
    shapefile.to_file(newfile, driver = 'GeoJSON')
    with open(newfile) as jsonfile:
        data = json.load(jsonfile)
        for feature in data['features']:
            if 'available' in feature['properties']:
                if feature['properties']['available']=='true':
                    feature['properties']['available'] = True
                elif feature['properties']['available']=='false':
                    feature['properties']['available'] = False
            elif 'available' not in feature['properties']:
                continue
        for feature in data['features']:
            if 'contLines' in feature['properties']:
                if feature['properties']['contLines']=='true':
                    feature['properties']['contLines'] = True
                elif feature['properties']['contLines']=='false':
                    feature['properties']['contLines'] = False
            elif 'contLines' not in feature['properties']:
                continue
        for feature in data['features']:
            if 'photomos' in feature['properties']:
                if feature['properties']['photomos']=='true':
                    feature['properties']['photomos'] = True
                elif feature['properties']['photomos']=='false':
                    feature['properties']['photomos'] = False
            elif 'photomos' not in feature['properties']:
                continue
    output = 'Post_Conversion\\' + newfile.split('\\')[1]
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(data, file)
