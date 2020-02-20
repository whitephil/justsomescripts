import pandas as pd
import geopandas as gpd
import os

os.chdir('C:\\Users\\phwh9568\\Data')

buildings = gpd.read_file('Colorado_Microsoft_Footprints\\Colorado.geojson')

countyUS = gpd.read_file('tl_2019_us_county\\tl_2019_us_county.shp')

countyUS = countyUS.to_crs({'init': 'epsg:4326'})

Colorado_Counties = countyUS.loc[countyUS['STATEFP'] == '08']
Colorado_Counties = Colorado_Counties[['NAMELSAD', 'geometry']]

CO_footprints = gpd.sjoin(buildings, Colorado_Counties, how='left', op='intersects')

CO_footprints.to_file('Colorado_Microsoft_Footprints\\Outputs\\CO_footprints.geojson', driver='GeoJSON')

print(len(CO_footprints))
print(CO_footprints.isna().sum())
