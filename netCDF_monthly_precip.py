
#netCDF_monthly_precip.py
#gfiske Aug 2015
#converts netcdf files to raster format and changes precip per day to Mean precip per month
#usess JGCRI RCP climate change scenarios data
#for kdunckel
#Maine, USA 

# Import arcpy module
import arcpy, glob, os
from arcpy import env
from arcpy.sa import *

# Check out any necessary licenses
arcpy.CheckOutExtension("Spatial")

# set local variables
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = "\\\\Atlas\\d\\gfiske\\kdunckel\\netcdfs\\precip\\test\\"

#make a dictionary of number of days per each month
dict = {'1': '31', 
        '2': '28', 
        '3': '31',
        '4': '30',
        '5': '31',
        '6': '30',
        '7': '31',
        '8': '31',
        '9': '30',
        '10': '31',
        '11': '30',
        '12': '31'}

#set nc specific variables
variable = "pr"
x_dimension = "longitude"
y_dimension = "latitude"
band_dimension = "time"
#valueSelectionMethod = "BY_VALUE"
valueSelectionMethod = "BY_INDEX"
 
# Set input directory with nc files
path = "\\\\Atlas\\d\\gfiske\\kdunckel\\netcdfs\\precip\\test\\"
# Make a list of all the .nc files in the directory
Mylist = glob.glob(path + '*.nc')
 
for nc in Mylist:
        #set output location
        outLoc = "\\\\Atlas\\d\\gfiske\\kdunckel\\netcdfs\\precip\\test\\output" + nc[-7:-3]
        year = nc[-7:-3]
        if not os.path.exists (outLoc):
                os.makedirs(outLoc) 
        
        # Get nc properties and dimensions
        nc_FP = arcpy.NetCDFFileProperties(nc)
        nc_Dim = nc_FP.getDimensions()

        #Loop through dimesions and create raster
        for dimension in nc_Dim:
                top = nc_FP.getDimensionSize(dimension)
                for i in range(1, top + 1):
                    if dimension == "time":
                        dimension_values = nc_FP.getDimensionValue(dimension, i)
                        nowFile = str(dimension_values)
                        dv1 = ["time", dimension_values]
                        dimension_values = [dv1]
                        outfile = variable + str(i)
                        myIndex = str(i - 1)
                        arcpy.MakeNetCDFRasterLayer_md(nc, variable, x_dimension, y_dimension, outfile, "", "time " + myIndex, valueSelectionMethod)
                        # convert rasters from mm/day to mm/month
                        outTimes = Times(outfile, int(dict[str(i)]))
                        # write file from memory to disk
                        arcpy.CopyRaster_management(outTimes, outLoc + "\\" + outfile + ".tif", "", "", "", "NONE", "NONE", "")
                        #print dimension_values, i

        arcpy.env.workspace = outLoc
        indiv_rasters = arcpy.ListRasters("*", "TIF")
        outMeanFile = outLoc + "\\Mean" + str(year) + ".tif"
        arcpy.gp.CellStatistics_sa((indiv_rasters), outMeanFile, "MEAN", "DATA")
        #optionally delete all indiv rasters
        for j in indiv_rasters:
                arcpy.Delete_management(j)

print "script finished successfully..."

