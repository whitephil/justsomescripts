# Based on: https://gis.stackexchange.com/questions/116672/georeferencing-raster-using-gdal-and-python

from osgeo import gdal, osr
import os

os.chdir('where_ever')

src_ds = gdal.Open('BOW001021_UnProj.tif')
format = 'GTiff'
driver = gdal.GetDriverByName(format)

dst_ds = driver.CreateCopy('new_Proj4.tif', src_ds, 0)

gt = [473085.999990,1.0604760375422084,0,4434856.364309,0,-1.0604760375422084]

dst_ds.SetGeoTransform(gt)

epsg = 32613 #utm zone 13n

srs = osr.SpatialReference()

srs.ImportFromEPSG(epsg)

dest_wkt = srs.ExportToWkt()

dst_ds.SetProjection(dest_wkt)

dst_ds = None #closes the data set
src_ds = None
