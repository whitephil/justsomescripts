#%%
import os
from glob import glob
import geopandas as gpd
from osgeo import gdal

# %%

drive = 'e:\\'
os.chdir(drive)

# %%
print(glob(drive))

# %%

print(glob(drive+'State*'))
# %%
print(glob(drive+'State*/parcel.shp'))
# %%
state_dirs = glob(drive+'State*')
# %%
county_dirs = [glob(state+'/*') for state in state_dirs]
# %%
counties = [county for sublist in county_dirs for county in sublist]
# %%
no_shx = []
for county in counties:
    files = glob(county+'/*')
    if county+'\Parcels.shx' not in files and county+'\parcels.shx' not in files:
        no_shx.append(county+'\parcels.shp')


#%%
no_shx = [county+'\parcels.shp' if county+'\parcels.shx' not in glob(county+'/*') for county in counties] 


#%%
no_shx = [county+'\parcels.shp' for county in counties if county+'\parcles.shx' not in glob(county+'/*')]




# %%

for county in county_dirs[4]:
    if 'parcels.shx' not in glob(county+'\*'):
        print(county)



# %%
for county in county_dirs[4]:
    print(glob(county+'\parcel.shp'))
# %%
print(county_dirs[4][5])
# %%
print(glob(county_dirs[4][5]+'\*'))
# %%
if county_dirs[4][5]+'\\Parcels.shx' not in glob(county_dirs[4][5]+'/*'):
    print('no')
# %%
for state in county_dirs:
    print(state)
# %%


