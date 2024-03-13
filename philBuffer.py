import arcpy    
from math import sin
from math import radians

def pointBuffer(inFile, outFilePath, outFileName, distance, numVertex):    
    crs = arcpy.Describe(inFile).spatialReference
    outfile = arcpy.management.CreateFeatureclass(outFilePath, outFileName, 'POLYGON', spatial_reference = crs)
    degree = 360/numVertex
    cursor = arcpy.da.SearchCursor(inFile,['SHAPE@'])
    for row in cursor:
        origin = row[0].getPart(0)
        array = arcpy.Array()
        point = arcpy.Point()
        A = 0
        count = 0
        for item in range(numVertex):
            count += 1
            A += degree
            C = 90
            B = 180 - (A+C)            
            yDelta = (distance*(sin(radians(B))))/(sin(radians(C)))
            xDelta = ((distance**2) - (yDelta**2))**.5
            if count > numVertex/2:
                xDelta = -xDelta            
            point.X = origin.X + xDelta
            point.Y = origin.Y + yDelta
            array.add(point)
        newPolygon = arcpy.Polygon(array)
        iCursor = arcpy.da.InsertCursor(outfile,['SHAPE@'])
        iCursor.insertRow([newPolygon])
        del iCursor
    
    del cursor
