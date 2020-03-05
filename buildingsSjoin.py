import pandas as pd
import geopandas as gpd
import os

#See Building_Splitter.ipynb for comments

os.chdir('C:\\Users\\phwh9568\\Data')

buildings = gpd.read_file('Colorado_Microsoft_Footprints\\Colorado2.geojson')
countyUS = gpd.read_file('tl_2019_us_county\\tl_2019_us_county.shp')

countyUS = countyUS.to_crs({'init': 'epsg:4326'})

Colorado_Counties = countyUS.loc[countyUS['STATEFP'] == '08']
Colorado_Counties = Colorado_Counties[['NAMELSAD', 'geometry']]

CO_footprints = gpd.sjoin(buildings, Colorado_Counties, how='left', op='within')
CO_footprints.reset_index(inplace=True)
CO_footprints = CO_footprints.drop(['index_right'], axis = 1)

nulls = CO_footprints[CO_footprints.isna().any(axis=1)]
nulls = nulls.drop(['NAMELSAD'], axis = 1)
nulls = gpd.sjoin(nulls, Colorado_Counties, how='left', op='intersects')
nulls = nulls.drop(['index_right'], axis = 1)

countyList = list(Colorado_Counties['NAMELSAD'])

for name in countyList:
    countyFootPrints = CO_footprints.loc[CO_footprints['NAMELSAD'] == name]
    countyIntersects = nulls.loc[nulls['NAMELSAD'] == name]
    countyFootPrints = pd.concat([countyFootPrints, countyIntersects], ignore_index=True)
    countyFootPrints.rename(columns={'NAMELSAD':'County', 'index': 'FID'}, inplace = True)
    fileName = name.replace(" ","_")+'_Buildings'
    countyFootPrints.to_file('Colorado_Microsoft_Footprints\\'+fileName)
