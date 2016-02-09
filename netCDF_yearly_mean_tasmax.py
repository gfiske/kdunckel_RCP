#netCDF_yearly_mean_tasmax.py
#gfiske Aug 2015
#reduces JGCRI RCP climate change temperature scenarios by year
#for kdunckel
#Maine, USA

import arcpy, os, glob
arcpy.CheckOutExtension("spatial")

# Set local variables
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = "C:/data/Downloads/netcdfs/"

# Set nc specific variables
variable = "tasmax"
x_dimension = "longitude"
y_dimension = "latitude"
band_dimension = ""
dimension = "time"
valueSelectionMethod = "BY_VALUE"

# Set one input nc file for testing
##nc = "C:/data/Downloads/netcdfs/ea_tasmax_rcp45_ME_2020.nc"

# Set all the nc files as input
# Make a list of all the .tif files in the directory
path = "C:/data/Downloads/netcdfs/"
Mylist = glob.glob(path + '*.nc')
for nc in Mylist:
    # Set output location directory
    outLoc = "C:/data/Downloads/netcdfs/output" + nc[-7:-3]
    year = nc[-7:-3]
    if not os.path.exists(outLoc):
        os.makedirs(outLoc)
    # Get nc properties and dimensions
    nc_FP = arcpy.NetCDFFileProperties(nc)
    nc_Dim = nc_FP.getDimensions()
    
    # Loop through dimensions
    for dimension in nc_Dim:
        top = nc_FP.getDimensionSize(dimension)
        for i in range(1, top + 1):
            if dimension == "time":
                dimension_values = nc_FP.getDimensionValue(dimension, i)
                nowFile = str(dimension_values)
                dv1 = ["time", dimension_values]
                dimension_values = [dv1]
    
                outfile = variable + str(i)
                arcpy.MakeNetCDFRasterLayer_md(nc, variable, x_dimension, y_dimension, outfile, band_dimension, dimension_values, valueSelectionMethod)
                arcpy.CopyRaster_management(outfile, outLoc + "//" + outfile + ".tif", "", "", "", "NONE", "NONE", "")
                print dimension_values, i
    
    # Create the mean of all the individual monthly rasters for current year
    arcpy.env.workspace = outLoc
    indiv_rasters = arcpy.ListRasters("*", "TIF")
    outMeanFile = "Mean" + year + ".tif"
    arcpy.gp.CellStatistics_sa((indiv_rasters), outMeanFile, "MEAN", "DATA")
    # Delete individual monthly rasters
    for monthly in indiv_rasters:
        arcpy.Delete_management(monthly)
        