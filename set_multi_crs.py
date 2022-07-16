import time
ti = time.time()
import os
from glob import glob
import geopandas as gpd

indir = r'C:\Users\phwh9568\OneDrive - UCB-O365\UCB\Desktop\gid_208175\CANADA\SHP'
os.chdir(indir)
outdir = r'C:/Users/phwh9568/data/canada_geol'

files = glob('*/*.shp')

for f in files:
    fName = f.split('\\')[1]
    gdf = gpd.read_file(f)
    gdf.set_crs(epsg=3978, inplace=True)
    gdf.to_crs(epsg=3978, inplace=True)
    gdf.to_file(outdir+r'/'+fName)
    
print(time.time() - ti)