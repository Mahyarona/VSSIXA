'''
Created on June 01 2019
@author: Mahyar Aboutalebi (Mahyar.Aboutalebi@gmail.com)
Modified on Sep 26 2019
DESCRIPTION
===========
This package contains the python codes for the second mode of Vegetation Sepctral-Structural Infromation eXtraction Algorithm (VSSIXA-II).
The secodn mode of VSSIXA works with both LiDAR and Point cloud data to extract sepctral and structural information of a canopy.
The full desciption of VSSIXA is described in the READEME file and the following paper:
Aboutalebi etl al., "Incorporation of Unmanned Aerial Vehicle (UAV) Point Cloud Product into Remote Sensing Evapotranspiration Models", Remote Sensing, 2019. (Submitted)
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
==============================================================================
 List of input variables and parameters used in VSSIXA-II
==============================================================================
START      = The first FID in the shapefile
END        = The last FID in the shapefile
Address    = The directory of input files
Address2   = The director of temp files created during the procedure
Shp_FileName         = The shapefile name that contains grids for VSSIXA calculation (e.g. A Fishnet)
Shp_Append_FileName  = The shapefile name that VSSIXA ouputs will append to its ATTibute Table (e.g. A Copy of Fishnet)
Shp_Grid_FileName    = An arbitrary name for temporray files
LAS_FileName         = Point cloud filename
R_TIF       = Red band filename
G_TIF       = Green band filename
B_TIF       = Blue band filename
N_TIF       = NIR band filename
NDVI_TIF    = NDVI band filename
NDVI_Up_TIF = Upscale NDVI band filename (Upscale to Tr pixel resolution)
Tr_TIF      = Tr band filename
PointCloud_Density = PointCloud Density
Lidar_Density      = LiDAR Density
NDVI_Soil_Threshold = A threshold to separate soil points from non-soil points 
NDVI_Veg_Threshold  = A threshold to separate vegetation  points from nonvegetation points 
Height_InterRow_Threshold  = A height threshold to separate interrows from non-interrows points
Height_Vine_Threshold      = A height threshold for pure vine canopy points 
Height_Vine                = Average of canopy height
Max_Height_Threshold       = Maximum canopy height
NDVI_Veg  = A NDVI threshold for pure vegetation points
NDVI_Soil = A NDVI  threshold for pure soil points 
==============================================================================
 List of output variables and parameters used in VSSIXA-II
==============================================================================
R    = Red Band
G    = Green Band
B    = Blue Band
N    = NIR Band
NDVI = The Normalized Difference Vegetation Index 
Tr   = Radiometric Tempreture
Ts0  = Soil temperature based on NDVI-Tr relationship
Tc0  = Canopy temperature  based on NDVI-Tr relationship
TsH  = Soil temperature based on Height-Tr relationship
TcH  = Canopy temperature  based on Height-Tr relationship
H_V    = Vegetation Height
R_V    = Vegetation Red Band 
G_V    = Vegetation Green Band
B_V    = Vegetation Blue Band
N_V    = Vegetation NIR Band
NDVI_V = Vegetation NDVI
H_C    = Canopy Height
R_C    = Canopy Red Band 
G_C    = Canopy Green Band
B_C    = Canopy Blue Band
N_C    = Canopy NIR Band
NDVI_C = Canopy NDVI
H_Intr    = Interrow Height
R_Intr    = Interrow Red Band 
G_Intr    = Interrow Green Band
B_Intr    = Interrow Blue Band
N_Intr    = Interrow NIR Band
NDVI_Intr = Interrow NDVI
VolumeAboveV  = Volume of Vegetation
SAreaAboveV   = Surface Area of Vegetation
AreaAboveV    = Area of Vegetation
VolumeAboveC  = Volume of Canopy
SAreaAboveC   = Surface Area of Canopy
AreaAboveC    = Area of Canopy
VolumeAboveIntr  = Volume of Interrow
SAreaAboveIntr   = Surface Area of Interrow
AreaAboveIntr    = Area of Interrow
'''

#============ Import Library ====================# 
import arcpy
import pandas as pd
from osgeo import ogr
from arcpy import env
import csv
import os
import glob

import gdal
from scipy.stats import linregress
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle as rect

import os.path
import sys
import arcgisscripting

import fnmatch
from xlwt import Workbook
#================================================#

#===============Set Initial Values===============#
import shutil

START=2001
END=2516

R=np.zeros(END)
G=np.zeros(END)
B=np.zeros(END)
N=np.zeros(END)
NDVI=np.zeros(END)
NDVI_Up=np.zeros(END)



Ts0=np.zeros(END)
Tc0=np.zeros(END)

TsH=np.zeros(END)
TcH=np.zeros(END)

Tr=np.zeros(END)



VolumeAboveV=np.zeros(END)
SAreaAboveV=np.zeros(END)
AreaAboveV=np.zeros(END)

VolumeAboveC=np.zeros(END)
SAreaAboveC=np.zeros(END)
AreaAboveC=np.zeros(END)

VolumeAboveIntr=np.zeros(END)
SAreaAboveIntr=np.zeros(END)
AreaAboveIntr=np.zeros(END)


H_V=np.zeros(END)
R_V=np.zeros(END)
G_V=np.zeros(END)
B_V=np.zeros(END)
N_V=np.zeros(END)
NDVI_V=np.zeros(END)

H_C=np.zeros(END)
R_C=np.zeros(END)
G_C=np.zeros(END)
B_C=np.zeros(END)
N_C=np.zeros(END)
NDVI_C=np.zeros(END)

H_Intr=np.zeros(END)
R_Intr=np.zeros(END)
G_Intr=np.zeros(END)
B_Intr=np.zeros(END)
N_Intr=np.zeros(END)
NDVI_Intr=np.zeros(END)

#===============Set Inputs===============#

Address="C:/Utah State University/Lodi_South/DataForCode_20140809_1041/ExtractForEachGrid"
Address2="C:/Utah State University/Lodi_South/DataForCode_20140809_1041"


#Shp_FileName='20140809_1041_Lodi_LAI_Rectangle.shp'
#Shp_Append_FileName= "20140809_1041_Lodi_LAI_Rectangle_Lidar_Append.shp"

#Shp_FileName='20140809_1041_Lodi_LAI_Square.shp'
#Shp_Append_FileName= "20140809_1041_Lodi_LAI_Square_Lidar_Append.shp"

Shp_FileName='20140809_1041_Lodi_LAI_Square_SubFishnet_South.shp'
Shp_Append_FileName= "20140809_1041_Lodi_LAI_Square_SubFishnet_South_Lidar_Append.shp"

Shp_Grid_FileName="LAI2014_Modified_BufferGridX.shp"
LAS_FileName='SLM_001_002_20140809_1041_DEM.las'
LAS_Lidar_FileName='Sierra_Loma_Mar2013_Lodi2017_merge_offset_neg31_505.las'



R_TIF='20140809_1041_R.tif'
G_TIF='20140809_1041_G.tif'
B_TIF='20140809_1041_B.tif'
N_TIF='20140809_1041_N.tif'
NDVI_TIF='20140809_1041_NDVI.tif'
NDVI_Up_TIF='20140809_1041_NDVI_Up.tif'
Tr_TIF='20140809_1041_Tr.tif'

PointCloud_Density=0.128
Lidar_Density=0.128

NDVI_Soil_Threshold=0.55
NDVI_Veg_Threshold=0.63

Height_InterRow_Threshold=0.5
Height_Vine_Threshold=1.0
Height_Vine=2.0
Max_Height_Threshold =3


NDVI_Veg= 0.80  #0.85  #0.60 #0.85 #0.72;
NDVI_Soil= 0.45 #0.51 #0.30 #0.51 #0.55;


arcpy.CreateFileGDB_management(Address, "fGDB.gdb")
arcpy.env.overwriteOutput = True


#===============Strart Calculation===============#
for i in range (START,END):

    try:

        # Select One Feature Among Features in the Shapefile
        env.workspace = Address2
        Shapefile = Shp_FileName.replace('.shp','_lyr')
        arcpy.MakeFeatureLayer_management(Shp_FileName, Shapefile)
        arcpy.SelectLayerByAttribute_management(Shapefile, 'NEW_SELECTION', '"FID" ='+ str(i))

        arcpy.CopyFeatures_management(Shapefile,
                                      Address+"/"+Shp_Grid_FileName+str(i))
    

        # Extract Point Cloud in each grid "3.6 *3.6" of Fishnet shapefile
        env.workspace = Address2
        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 10N")
        arcpy.env.overwriteOutput = True
        arcpy.ddd.ExtractLas(LAS_FileName,
                             Address,
                             boundary=Address+"/"+Shp_Grid_FileName,
                             #name_suffix='subset', remove_vlr=True, 
                             rearrange_points='MAINTAIN_POINTS') 
                             #out_las_dataset='extracted_PointCloud.lasd')


        # Extract Ground Lidar points in each grid "3.6 *3.6" of Fishnet shapefile
        env.workspace = Address2
        arcpy.env.overwriteOutput = True
        arcpy.ddd.ExtractLas(LAS_Lidar_FileName,
                             Address,
                             boundary=Address+"/"+Shp_Grid_FileName,
                             #name_suffix='subset', remove_vlr=True, 
                             rearrange_points='MAINTAIN_POINTS') 
                             #out_las_dataset='extracted_lidar.lasd')

    

        # Extract by Mask for R,G,B,NIR,NDVI, NDVI_Up, Tr for each Feature in the Shapefile
    
        for file in [R_TIF,G_TIF,B_TIF,N_TIF,NDVI_TIF,NDVI_Up_TIF,Tr_TIF]:
        
            RasterName=Address2+"/"+file
            print (RasterName)

            InRaster = RasterName
            InMask = Address+"/"+Shp_Grid_FileName
            OutRaster = Address+"/"+'BandsExtract.tif'
            gp = arcgisscripting.create()
            arcpy.gp.ExtractByMask_sa(InRaster, InMask, OutRaster)
        
            array_M = arcpy.RasterToNumPyArray(OutRaster, nodata_to_value = 99999)
            array_N = np.ma.masked_array(array_M, array_M == 99999)
        
           
            Mean_Raster=array_N.mean()
            Mean_Raster=np.float64(Mean_Raster)
            print (Mean_Raster)
            #print (file)
        

            if file==R_TIF:
                R[i]=Mean_Raster
                R_Array=array_N;
            
            elif file==G_TIF:
                G[i]=Mean_Raster
                G_Array=array_N;
            
            elif file==B_TIF:
                B[i]=Mean_Raster
                B_Array=array_N;
            
            elif file==N_TIF:
                N[i]=Mean_Raster
                N_Array=array_N;
            
            elif file==NDVI_TIF:
                NDVI[i]=Mean_Raster
                NDVI_Array=array_N;
            
            elif file==NDVI_Up_TIF:
                NDVI_Up[i]=Mean_Raster
                NDVI_Up_Array=array_N;
            
            elif file==Tr_TIF:
                Tr[i]=Mean_Raster
                Tr_Array=array_N;

        # Calculate Ts and Tc from Hector Nieto Approach
                slope, intercept, correlation,pvalue,stderr=linregress(NDVI_Up_Array.data.reshape(-1)[((NDVI_Up_Array.data.reshape(-1) >= 0) & (NDVI_Up_Array.data.reshape(-1) <= 1))],Tr_Array.data.reshape(-1)[((NDVI_Up_Array.data.reshape(-1) >= 0) & (NDVI_Up_Array.data.reshape(-1) <= 1))])

                if any(t >= NDVI_Veg and t<=1 for t in NDVI_Up_Array.data.reshape(-1)):
                    Tc=Tr_Array.data.reshape(-1)[((NDVI_Up_Array.data.reshape(-1) >= NDVI_Veg) & (NDVI_Up_Array.data.reshape(-1) <= 1))].mean()

                else:
                    Tc=intercept+slope*NDVI_Veg

                if any(t >= 0 and t<=NDVI_Soil for t in NDVI_Up_Array.data.reshape(-1)):
            
                    Ts=Tr_Array.data.reshape(-1)[((NDVI_Up_Array.data.reshape(-1) >= 0) & (NDVI_Up_Array.data.reshape(-1) <= NDVI_Soil))].mean()

                else:
                    Ts=intercept+slope*NDVI_Soil
                       
                Ts0[i]=Ts
                Tc0[i]=Tc

    except Exception:
        print('Error00: Extract LAS files and Raster files in the Shapefile Region')
        R[i]=0
        G[i]=0
        B[i]=0
        N[i]=0
        NDVI[i]=0
        NDVI_Up[i]=0
        Tr[i]=0
        Ts0[i]=0
        Tc0[i]=0
        pass


        # LAS (Point Clouds) to MultiPoint (Shapefile)  
        print('LAS (Point Clouds) to MultiPoint')
    
    try:
        arcpy.ddd.LASToMultipoint(Address+"/"+LAS_FileName,
                                  Address+"/"+"LastoMulti.shp", PointCloud_Density,
                                  None, "ANY_RETURNS", None, "PROJCS['WGS_1984_UTM_Zone_10N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                                  "las", 1, "NO_RECURSION")
          
    
   # MultiPoint to SinglePoints
        print('MultiPoint to SinglePoints')
        
        arcpy.management.MultipartToSinglepart(Address+"/"+"LastoMulti.shp",
                                               Address+"/"+"LastoMulti02_MultipartToSing.shp")

    # Add Z toAttribute of SinglePoints
        print('Add Z toAttribute of SinglePoints')
        arcpy.ddd.AddZInformation(Address+"/"+"LastoMulti02_MultipartToSing.shp", "Z", None)


        
    # Append R, G, B, N, NDVI, NDVI_Up, Tr To each Point
        print('Append R, G, B, N, NDVI, NDVI_Up, Tr To each Point')
        
        arcpy.sa.ExtractValuesToPoints(Address+"/"+"LastoMulti02_MultipartToSing.shp",
                                       Address2+"/"+R_TIF,
                                       Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_R", "INTERPOLATE", "VALUE_ONLY")    
        arcpy.management.AlterField(  Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_R", "RASTERVALU", "R", "R", "FLOAT", 4, "NULLABLE", "DO_NOT_CLEAR")


   

        arcpy.sa.ExtractValuesToPoints(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_R",
                                       Address2+"/"+G_TIF,
                                       Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RG", "INTERPOLATE", "VALUE_ONLY")   
        arcpy.management.AlterField(  Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RG", "RASTERVALU", "G", "G", "FLOAT", 4, "NULLABLE", "DO_NOT_CLEAR")


    
       
        arcpy.sa.ExtractValuesToPoints(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RG",
                                       Address2+"/"+B_TIF,
                                       Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGB", "INTERPOLATE", "VALUE_ONLY")
        arcpy.management.AlterField(  Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGB", "RASTERVALU", "B", "B", "FLOAT", 4, "NULLABLE", "DO_NOT_CLEAR")

        
    
    
        arcpy.sa.ExtractValuesToPoints(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGB",
                                       Address2+"/"+N_TIF,
                                       Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBN", "INTERPOLATE", "VALUE_ONLY")
        arcpy.management.AlterField( Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBN", "RASTERVALU", "N", "N", "FLOAT", 4, "NULLABLE", "DO_NOT_CLEAR")

    
    

    
        arcpy.sa.ExtractValuesToPoints(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBN",
                                       Address2+"/"+NDVI_TIF,
                                       Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVI", "INTERPOLATE", "VALUE_ONLY")
        arcpy.management.AlterField( Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVI", "RASTERVALU", "NDVI", "NDVI", "FLOAT", 4, "NULLABLE", "DO_NOT_CLEAR")


        

        arcpy.sa.ExtractValuesToPoints(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVI",
                                       Address2+"/"+Tr_TIF,
                                       Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr", "INTERPOLATE", "VALUE_ONLY")
        
        arcpy.management.AlterField( Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr", "RASTERVALU", "Tr", "Tr", "FLOAT", 4, "NULLABLE", "DO_NOT_CLEAR")
        arcpy.CopyFeatures_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr",
                                      Address+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr.shp")

    except Exception:
        print('Error01: LAS to Multipoint/ Multipoint to Single Points/ Add Z values/ Append RGBNT to Single Points')
        pass


    try:

    # LAS (NASA Ground) to MultiPoint
        arcpy.ddd.LASToMultipoint(Address+"/"+LAS_Lidar_FileName,
                                  Address+"/"+"LastoMultiG.shp", Lidar_Density,
                                  None, "ANY_RETURNS", None, "PROJCS['WGS_1984_UTM_Zone_10N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                                  "las", 1, "NO_RECURSION")
          
    
    # NASA MultiPoint to NASA SinglePoints
        arcpy.management.MultipartToSinglepart(Address+"/"+"LastoMultiG.shp",
                                               Address+"/"+"LastoMulti02_MultipartToSingG.shp")

    # Add Z toAttribute of NASA SinglePoints
        arcpy.ddd.AddZInformation(Address+"/"+"LastoMulti02_MultipartToSingG.shp", "Z", None)


    except Exception:
        print('Error02: NASA Lidar LAS to Multipoint/ Multipoint to Single Points/ Add Z values')
        pass


    #try:
    # exit()
    #except Exception:
    #    print('Exit')
    #    pass     

     
    try:
    #  Joint Z from NASA Lidar to PointClouds
        arcpy.analysis.SpatialJoin(Address+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr.shp",
                               Address+"/"+"LastoMulti02_MultipartToSingG.shp",
                               Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_"+str(i), "JOIN_ONE_TO_MANY", "KEEP_ALL",
                               #'Id "Id" true true false 6 Long 0 6,First,#,LastoMulti02_MultipartToSing,Id,-1,-1;PointCount "PointCount" true true false 10 Long 0 10,First,#,LastoMulti02_MultipartToSing,PointCount,-1,-1;ORIG_FID "ORIG_FID" true true false 10 Long 0 10,First,#,LastoMulti02_MultipartToSing,ORIG_FID,-1,-1;Z "Z" true true false 19 Double 0 0,First,#,LastoMulti02_MultipartToSing,Z,-1,-1;Id_1 "Id" true true false 4 Long 0 0,First,#,ground0_MultipartToSinglepar,Id,-1,-1;PointCount_1 "PointCount" true true false 4 Long 0 0,First,#,LastoMulti02_MultipartToSingG,PointCount,-1,-1;ORIG_FID_1 "ORIG_FID" true true false 4 Long 0 0,First,#,LastoMulti02_MultipartToSingG,ORIG_FID,-1,-1;Z_1 "Z" true true false 8 Double 0 0,First,#,LastoMulti02_MultipartToSingG,Z,-1,-1;ZG "ZG" true true false 255 Double 0 0,First,#,LastoMulti02_MultipartToSingG,Z,-1,-1', "CLOSEST", None, None)
                               'Id "Id" true true false 10 Long 0 10,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,Id,-1,-1;PointCount "PointCount" true true false 10 Long 0 10,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,PointCount,-1,-1;ORIG_FID "ORIG_FID" true true false 10 Long 0 10,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,ORIG_FID,-1,-1;Z "Z" true true false 19 Double 0 0,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,Z,-1,-1;R "R" true true false 13 Float 0 0,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,R,-1,-1;G "G" true true false 13 Float 0 0,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,G,-1,-1;B "B" true true false 13 Float 0 0,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,B,-1,-1;N "N" true true false 13 Float 0 0,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,N,-1,-1;NDVI "NDVI" true true false 13 Float 0 0,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,NDVI,-1,-1;Tr "Tr" true true false 13 Float 0 0,First,#,LastoMulti02_MultipartToSing_RGBNNDVITr,Tr,-1,-1;Z_1 "Z" true true false 19 Double 0 0,First,#,LastoMulti02_MultipartToSingG,Z,-1,-1', "CLOSEST_GEODESIC", None, None)


    # Calculate Height inside PointCloud Attribute Table
        arcpy.AddField_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_"+str(i), "ZG", "float", "", "", "")

        arcpy.management.CalculateField(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_"+str(i), "ZG", "!Z! - !Z_1!", "PYTHON3", None)

        arcpy.MakeFeatureLayer_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_"+str(i), Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_"+str(i)+"_lyr")

        arcpy.management.SelectLayerByAttribute(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_"+str(i)+"_lyr", "NEW_SELECTION", "ZG >= 0", None)

        arcpy.management.CopyFeatures(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_"+str(i)+"_lyr",
                                      Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i), None, None, None, None)

    except Exception:
        print('Error03: Join Soil to Single Points/ Calculate ZG= Z-Z1/ Filter ZG>=0')
        pass


    
    # Create Datasets: Vegetation, Canopy, Interrows Points Based on NDVI and Heights


    # (1) Vegetation Data
    try:

        arcpy.MakeFeatureLayer_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i),
                                          Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr")
        
        arcpy.SelectLayerByAttribute_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr",'NEW_SELECTION', '"NDVI" >'+str(NDVI_Veg_Threshold))
        
        arcpy.CopyFeatures_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr",
                                      Address+"/"+"Veg_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".shp")
   
    except Exception:
        print('Error04 : Create Veg Single Points ZG>=0 and NDVI> NDVI Veg Threshold')
        pass


    #(2) Canopy Data: OR Veg without Noise
    
    try:

        

        arcpy.MakeFeatureLayer_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i),
                                          Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr")
        
        arcpy.SelectLayerByAttribute_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr",
                                                'NEW_SELECTION', '"NDVI" >'+str(NDVI_Veg_Threshold)+' And '+ '"ZG" >'+str(Height_InterRow_Threshold))

        arcpy.CopyFeatures_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr",
                                      Address+"/"+"Veg_Canopy_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".shp")

    except Exception:
        print('Error05: Create Canopy Single Points ZG>=0 and NDVI>NDVI_Veg_Threshold and ZG> Height_InterRow_Threshold')
        pass
    

    # (3) Interrow Data
    try:

        arcpy.MakeFeatureLayer_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i),
                                          Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr")
        
        arcpy.SelectLayerByAttribute_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr",
                                                'NEW_SELECTION', '"NDVI" >'+str(NDVI_Veg_Threshold)+' And '+ '"ZG" <'+str(Height_InterRow_Threshold))

        arcpy.CopyFeatures_management(Address+"/"+"fGDB.gdb"+"/"+"LastoMulti02_MultipartToSing_RGBNNDVITr_JoinZ_Filter_"+str(i)+"_lyr",
                                      Address+"/"+"Veg_Interrow_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".shp")


    except Exception:
        print('Error06: Create Interrows Single Points ZG>=0 and NDVI>NDVI_Veg_Threshold and ZG<Height_InterRow_Threshold')
        pass


    # Export RGBNNDVI to CSV For Total
    
    try:
        input_fct = Address+"/"+"Veg_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".dbf"
        output_csv = Address+"/"+"Veg_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".csv"
        csv_delimiter = ","
        arcpy.env.overwriteOutput = True

        fld_list = arcpy.ListFields(input_fct)
        fld_names = [fld.name for fld in fld_list]

        with open(output_csv, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=csv_delimiter)
            writer.writerow(fld_names)
            with arcpy.da.SearchCursor(input_fct, fld_names) as cursor:
              for row in cursor:
                writer.writerow(row)
            csv_file.close()
            

    # Calculate Ts and Tc Based on Mahyar Aboutalebi Approach (T-Hieght)
    
        df = pd.read_csv(Address+"/"+"Veg_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".csv")
        H_Data=df["ZG"]
    ##H_Data=H_Tr["Z"]-np.percentile(H_Tr["Z"], 1)
        Tr_data=df["Tr"]

        H_Data2=H_Data[((H_Data >= 0) & (H_Data <= 3))]
        Tr_Data2=Tr_data[((H_Data >= 0) & (H_Data <= 3))]
        DataHTr=pd.DataFrame({"H":H_Data2,"Tr":Tr_Data2})
        AvgHTr=DataHTr.groupby("Tr").mean()
        tr1=AvgHTr.index.values
        hh2=AvgHTr.values
        hh3=[val for sublist in hh2 for val in sublist]
        slope, intercept, correlation,pvalue,stderr=linregress(hh3,tr1)
        #DataHTr.drop_duplicates(subset=['C'], keep=False)   Check it later  
        slope, intercept, correlation,pvalue,stderr=linregress(H_Data[((H_Data >= 0) & (H_Data <= Max_Height_Threshold))],Tr_data[((H_Data >= 0) & (H_Data <= Max_Height_Threshold))])
                
        if any(h >= 0 and h<=0.5 for h in H_Data):
                Ts_H=Tr_data[((H_Data >= 0) & (H_Data <= Height_InterRow_Threshold))].mean()
            
        else:
            Ts_H=intercept+slope*0

        
        if any(h >= Height_Vine_Threshold and h<=Max_Height_Threshold for h in H_Data):
            Tc_H=Tr_data[((H_Data >= Height_Vine_Threshold) & (H_Data <= Max_Height_Threshold))].mean()
                           
        else:
            Tc_H=intercept+slope*Height_Vine
            #H_Data=df["ZG"]-np.percentile(df["ZG"], 1)
            #H_Data=H_Tr["ZG"]        
            
        TsH[i]=Ts_H
        TcH[i]=Tc_H


        print('H-Tr profile Done')

    except Exception:
        print('Error07: Veg to CSV and Calculate TsH and TcH')
        TsH[i]=0
        TcH[i]=0
        pass



    try:
    # Calcuate H, RGBN NDVI for Total 
        df = pd.read_csv(Address+"/"+"Veg_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".csv")
        H_V[i]=df["ZG"].mean()
        R_V[i]=df["R"].mean()
        G_V[i]=df["G"].mean()
        B_V[i]=df["B"].mean()
        N_V[i]=df["N"].mean()
        NDVI_V[i]=df["NDVI"].mean()


    except Exception:
        
        H_V[i]=0
        R_V[i]=0
        G_V[i]=0
        B_V[i]=0
        N_V[i]=0
        NDVI_V[i]=0

        print('Error08 : Veg HRGBNTr Info Zero')
        pass

    
    try:
    # Export RGBNNDVI to CSV For Canopy
        input_fct = Address+"/"+"Veg_Canopy_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".dbf"
        output_csv = Address+"/"+"Veg_Canopy_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".csv"
        csv_delimiter = ","
        arcpy.env.overwriteOutput = True

        fld_list = arcpy.ListFields(input_fct)
        fld_names = [fld.name for fld in fld_list]

        with open(output_csv, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=csv_delimiter)
            writer.writerow(fld_names)
            with arcpy.da.SearchCursor(input_fct, fld_names) as cursor:
              for row in cursor:
                writer.writerow(row)
            csv_file.close()

    # Calcuate H, RGBN NDVI for Canopy 
        df = pd.read_csv(Address+"/"+"Veg_Canopy_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".csv")
        H_C[i]=df["ZG"].mean()
        R_C[i]=df["R"].mean()
        G_C[i]=df["G"].mean()
        B_C[i]=df["B"].mean()
        N_C[i]=df["N"].mean()
        NDVI_C[i]=df["NDVI"].mean()

    except Exception:

        H_C[i]=0
        R_C[i]=0
        G_C[i]=0
        B_C[i]=0
        N_C[i]=0
        NDVI_C[i]=0

        print('Error09 : Canopy HRGBNTr Info Zero')
        pass



    try:
    # Export RGBNNDVI to CSV For Grass
        input_fct = Address+"/"+"Veg_Interrow_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".dbf"
        output_csv = Address+"/"+"Veg_Interrow_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".csv"
        csv_delimiter = ","
        arcpy.env.overwriteOutput = True

        fld_list = arcpy.ListFields(input_fct)
        fld_names = [fld.name for fld in fld_list]

        with open(output_csv, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=csv_delimiter)
            writer.writerow(fld_names)
            with arcpy.da.SearchCursor(input_fct, fld_names) as cursor:
              for row in cursor:
                writer.writerow(row)
            csv_file.close()

    # Calcuate H, RGBN NDVI for Grass 
        df = pd.read_csv(Address+"/"+"Veg_Interrow_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".csv")
        H_Intr[i]=df["ZG"].mean()
        R_Intr[i]=df["R"].mean()
        G_Intr[i]=df["G"].mean()
        B_Intr[i]=df["B"].mean()
        N_Intr[i]=df["N"].mean()
        NDVI_Intr[i]=df["NDVI"].mean()


    except Exception:

        H_Intr[i]=0
        R_Intr[i]=0
        G_Intr[i]=0
        B_Intr[i]=0
        N_Intr[i]=0
        NDVI_Intr[i]=0

        print('Error10: Interrow HRGBNTr Info Zero')
        pass


    # Create 4 TINS: Soil, Vegetation, Canopy, Interrows Points
    try:     
   
        env.workspace = Address
        
        OutputTinV="TINV"+str(i)
        OutputTinC="TINC"+str(i)
        OutputTinIntr="TINInt"+str(i)

    except Exception:
        print('Error11: TIN Name problems')
        pass
        

    try:         
        arcpy.ddd.CreateTin(OutputTinV,
                        "PROJCS['WGS_1984_UTM_Zone_10N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                        "Veg_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".shp ZG Mass_Points <None>", "DELAUNAY")

    except Exception:
        print('Error12: TIN V problems')
        pass
    

    
    try:
        env.workspace = Address
        arcpy.ddd.CreateTin(OutputTinC,
                        "PROJCS['WGS_1984_UTM_Zone_10N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                        "Veg_Canopy_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".shp ZG Mass_Points <None>", "DELAUNAY")
    except Exception:
        print('Error13: TIN C problems')
        pass

    
    try: 
        arcpy.ddd.CreateTin(OutputTinIntr,
                        "PROJCS['WGS_1984_UTM_Zone_10N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                        "Veg_Interrow_JoinGtoPcloud_RGBNNDVITr_"+str(i)+".shp ZG Mass_Points <None>", "DELAUNAY")

    except Exception:
        print('Error14: TIN Intr problems')
        pass


    

    # Create 3 SurfaceDifference_3d:  Vegetation, Canopy, Interrows TINS versus Zero Elevation Surface

    try:

        OutputV="testV"+str(i)
        OutputC="testC"+str(i)
        OutputIntr="testIntr"+str(i)

    except Exception:
        print('Error15: SurfaceVolume Name problems')
        pass
        

    try:
        
        arcpy.ddd.SurfaceVolume(OutputTinV, Address+"/"+ OutputV+".csv", "ABOVE", 0, 1, 0)
        
    except Exception:
        print('Error16: SurfaceVolume V problems')
        pass
    


    try:
        
        arcpy.ddd.SurfaceVolume(OutputTinC, Address+"/"+ OutputC+".csv", "ABOVE", 0, 1, 0)
    except Exception:
        print('Error17: SurfaceVolume C problems')
        pass
    


    try: 
        arcpy.ddd.SurfaceVolume(OutputTinIntr, Address+"/"+ OutputIntr+".csv", "ABOVE", 0, 1, 0)
    except Exception:
        print('Error18: SurfaceVolume Intr problems')
        pass

    



    # Read Volume and Surafce For Total Volume
    try:  
        df = pd.read_csv(Address+"/"+OutputV+".csv")
        VolumeAboveV[i]=df.iloc[0][6]
        SAreaAboveV[i]=df.iloc[0][5]
        AreaAboveV[i]=df.iloc[0][4]

    except Exception:
        
        VolumeAboveV[i]=0
        SAreaAboveV[i]=0
        AreaAboveV[i]=0
        
        print('Error19: Veg Structure Info Zero')
        pass




    # Read Volume and Surafce For Canopy Volume
    try:  
        df = pd.read_csv(Address+"/"+OutputC+".csv")
        VolumeAboveC[i]=df.iloc[0][6]
        SAreaAboveC[i]=df.iloc[0][5]
        AreaAboveC[i]=df.iloc[0][4]


    except Exception:

        VolumeAboveC[i]=0
        SAreaAboveC[i]=0
        AreaAboveC[i]=0
        
        
        print('Error20: Canopy Structure Info Zero')
        pass


    # Read Volume and Surafce For Interrows
    try:  
        df = pd.read_csv(Address+"/"+OutputIntr+".csv")
        VolumeAboveIntr[i]=df.iloc[0][6]
        SAreaAboveIntr[i]=df.iloc[0][5]
        AreaAboveIntr[i]=df.iloc[0][4]
        print(i)


    except Exception:

        VolumeAboveIntr[i]=0
        SAreaAboveIntr[i]=0
        AreaAboveIntr[i]=0
        print(i)

        print('Error21: Intr Structure Info Zero')
        pass


    # Remove Files
    
    try:
        files01 = glob.glob(Address+"/"+'*.las')
        for f in files01:
            os.remove(f)            
    except Exception:
        print('Error22: Remove 1')
        pass
    


    try:        
        files01 = glob.glob(Address+"/"+'*.lasx')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error23: Remove 2')
        pass

    
    try:
        shutil.copy(Address+"/"+'Veg_JoinGtoPcloud_RGBNNDVITr_'+str(i)+'.csv', Address+"/"+'CSV'+"/"+'Veg_JoinGtoPcloud_RGBNNDVITr_'+str(i)+'.csv')
    except Exception:
        print('Error24: Remove 3')
        pass        


    try:
        files01 = glob.glob(Address+"/"+'Veg_JoinGtoPcloud_RGBNNDVITr_'+str(i-1)+'*')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error26: Remove 4-1')
        pass
    

    try:
        files01 = glob.glob(Address+"/"+'Veg_Canopy_JoinGtoPcloud_RGBNNDVITr_'+str(i-1)+'*')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error26: Remove 4-2')
        pass


    try:
        files01 = glob.glob(Address+"/"+'Veg_Interrow_JoinGtoPcloud_RGBNNDVITr_'+str(i-1)+'*')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error26: Remove 4-3')
        pass
    

    try:
        files01 = glob.glob(Address+"/"+'Soil*')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error27: Remove 5')
        pass

        #files01 = glob.glob(Address+"/"+'test*')
        #for f in files01:
        #    os.remove(f)
        
    try:
        files01 = glob.glob(Address+"/"+'testC'+str(i-1)+'*')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error28: Remove 6')
        pass
    

    try:
        files01 = glob.glob(Address+"/"+'testV'+str(i-1)+'*')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error29: Remove 7')
        pass
    

    try:
        files01 = glob.glob(Address+"/"+'testIntr'+str(i-1)+'*')
        for f in files01:
            os.remove(f)
    except Exception:
        print('Error30: Remove 8')
        pass



    try:
        files02 = glob.glob(Address+"/"+'report*')
        for f in files02:
            os.remove(f)
    except Exception:
        print('Error31: Remove 9')
        pass
    

    try:
        files02 = glob.glob(Address+"/"+'LAI*')
        for f in files02:
            os.remove(f)
    except Exception:
        print('Error32: Remove 10')
        pass
    

    try:
        files02 = glob.glob(Address+"/"+'LastoMulti02_MultipartToSing_RGBNNDVITr_Soil*')
        for f in files02:
            os.remove(f)
    except Exception:
        print('Error33: Remove 11')
        pass
    
            
    try:
        shutil.rmtree(Address+"/"+OutputTinV)
    except Exception:
        print('Error34: Remove 12')
        pass

    
    try:
        shutil.rmtree(Address+"/"+OutputTinC)
    except Exception:
        print('Error35: Remove 14')
        pass

    
    try:
        shutil.rmtree(Address+"/"+OutputTinIntr)
    except Exception:
        print('Error36: Remove 15')
        pass

    try:
        files02 = glob.glob(Address+"/"+'Lasto*')
        for f in files02:
            os.remove(f)
    except Exception:
        print('Error37: Remove 16')
        pass


    try:
        files02 = glob.glob(Address+"/"+'LastoMulti*')
        for f in files02:
            os.remove(f)
    except Exception:
        print('Error38: Remove 17')
        pass

        

print('Append')

arcpy.env.workspace = Address2
try:
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "R", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "G", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "B", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "N", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "NDVI", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "Tr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "Ts", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "Tc", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "TsH", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "TcH", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "H_V", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "R_V", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "G_V", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "B_V", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "N_V", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "NDVI_V", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "H_C", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "R_C", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "G_C", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "B_C", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "N_C", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "NDVI_C", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "H_Intr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "R_Intr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "G_Intr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "B_Intr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "N_Intr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "NDVI_Intr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "VolumeV", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "SAreaV", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "AreaV", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "VolumeC", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "SAreaC", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "AreaC", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "VolumeIntr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "SAreaIntr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.AddField(Address2+"/"+Shp_Append_FileName, "AreaIntr", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    


except Exception:
    print('Error39: Append')
    pass

cur = arcpy.UpdateCursor(Address2+"/"+Shp_Append_FileName)

                                                                                                         
#Start=20
#j=0
j=START
for row in cur:
    if row.FID==START:
        row.setValue('R', np.float64(R[j]))
        row.setValue('G', np.float64(G[j]))
        row.setValue('B', np.float64(B[j]))
        row.setValue('N', np.float64(N[j]))
        row.setValue('NDVI', np.float64(NDVI[j]))

        row.setValue('Tr', np.float64(Tr[j]))

        row.setValue('Ts', np.float64(Ts0[j]))
        row.setValue('Tc', np.float64(Tc0[j]))

        row.setValue('TsH', np.float64(TsH[j]))
        row.setValue('TcH', np.float64(TcH[j]))

        row.setValue('H_V', np.float64(H_V[j]))
        row.setValue('R_V', np.float64(R_V[j]))
        row.setValue('G_V', np.float64(G_V[j]))
        row.setValue('B_V', np.float64(B_V[j]))
        row.setValue('N_V', np.float64(N_V[j]))
        row.setValue('NDVI_V', np.float64(NDVI_V[j]))

        row.setValue('H_C', np.float64(H_C[j]))
        row.setValue('R_C', np.float64(R_C[j]))
        row.setValue('G_C', np.float64(G_C[j]))
        row.setValue('B_C', np.float64(B_C[j]))
        row.setValue('N_C', np.float64(N_C[j]))
        row.setValue('NDVI_C', np.float64(NDVI_C[j]))
        
        row.setValue('H_Intr', np.float64(H_Intr[j]))
        row.setValue('R_Intr', np.float64(R_Intr[j]))
        row.setValue('G_Intr', np.float64(G_Intr[j]))
        row.setValue('B_Intr', np.float64(B_Intr[j]))
        row.setValue('N_Intr', np.float64(N_Intr[j]))
        row.setValue('NDVI_Intr', np.float64(NDVI_Intr[j]))


        row.setValue('VolumeV', np.float64(VolumeAboveV[j]))
        row.setValue('SAreaV', np.float64(SAreaAboveV[j]))
        row.setValue('AreaV', np.float64(AreaAboveV[j]))
        
        row.setValue('VolumeC', np.float64(VolumeAboveC[j]))
        row.setValue('SAreaC', np.float64(SAreaAboveC[j]))
        row.setValue('AreaC', np.float64(AreaAboveC[j]))
        
        row.setValue('VolumeIntr', np.float64(VolumeAboveIntr[j]))
        row.setValue('SAreaIntr', np.float64(SAreaAboveIntr[j]))
        row.setValue('AreaIntr', np.float64(AreaAboveIntr[j]))
        
        print(row.FID)


    
        j=j+1
        START=START+1
        print(j)
        cur.updateRow(row)




