'''
Created on Apr 15, 2018

@author: HP
'''
import shutil
import arcpy
import logging
import os
import zipfile
import time
class MyClass(object):
    '''
    classdocs
    '''


    
#initialize

arcpy.ResetEnvironments()

#Delete any existing trees

try:
    
    shutil.rmtree('C:\Users\harchena\Documents\Inside\\')
except:
    print("No original tree found. This is what will be generated. Passing off")
    pass

results=[]
ArrivalRaster=[]
Name=[]
mergedam=[]
FINALMERGEVALUE=[]
betterpathnameOUT=[] #Lists all dams about to be used by function
allcomposites=[]
wetdrys=[]
kmzlist=[]
errorlog=[] #Call this variable if a dam is missing in final output
kmzconverted=[]
arcpy.env.overwriteOutput = True #ALLOWING OVERWRITE !!! WATCH OUT !!!

#RemoveDuplicatesDef

duplicate=wetdrys
def RemoveDuplicate(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)

    return final_list



#Figure out names of folder

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]


#Checking what's currently made and making my modifications

try:
    
    shutil.rmtree('C:\Users\harchena\Documents\ArcGIS\Default.gdb')
except:
    print("no default found locally (good)... checking your network drive")
try:
    shutil.rmtree('H:\ARCGIS\Default.gdb')
except:
    print("no default found on network. check filepath. ARCGIS will attempt to regenerate... hold tight")
#Begin process



#Copy whole tree for local manipulation

root_src_dir = r'M:\gisapp\EQCAPP\BW\HAZDAM\DSS_WISE\DSS_WISE_Lite_Mapbook_Processing\InundationScript'    #Path/Location of the source directory
root_dst_dir = r'C:\Users\harchena\Documents\Inside\Workspace'  #Path to the destination folder


for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)

#rename files
try:
    rangeoffiles1=os.listdir(root_src_dir)
    for i in range(len(rangeoffiles1)):
        name=root_src_dir+"\\"+rangeoffiles1[i]
        os.rename(name,left(rangeoffiles1[i],5))
except:
    print('Unable to rename... possibly already renamed. Attempting to pass...')
    pass
    

#setting workspace variables

damdataroot=r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\DamData'
localdatabaseroot=r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database'
#Begin process

#Let's create some work enviornments for stability of I/O operations
try:
    arcpy.CreateFileGDB_management("H:\ARCGIS\\","Default.gdb")
    arcpy.CreateFileGDB_management(r'C:\Users\harchena\Documents\Inside\ScratchSpace',"Scratch.gdb")
    arcpy.env.workspace = "H:\ARCGIS\Default.gdb"
    arcpy.env.scratchWorkspace="C:\Users\harchena\Documents\Inside\Workspace\Scratch.gdb"
except:
    print("ARCGIS is having trouble creating a workspace. If you're encountering ER99999- this is why. Passing off...")
    pass
try:
    shutil.rmtree('H:\\InundationLayerDatabase\Database\CompositeRaster\CompositeRaster.gdb')
except:
    pass




#Let's make the file locations
try:
    os.makedirs(damdataroot)
    os.makedirs(r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database')
    os.makedirs(localdatabaseroot+'\CompositeRaster')
    os.makedirs(localdatabaseroot+'\MosaicRaster')
    os.makedirs(localdatabaseroot+'\ShapesAndStructures\StructureManipulation')
except:
    print('Unable to make enclosing folders. If your script has run successfully before, we will attempt to pass. If not, the script will break')





#Restart workstation. NOTE: this command deletes the default.gdb which is normally reformed at launch... but be careful.
try:
    
    shutil.rmtree('C:\Users\harchena\Documents\ArcGIS\Default.gdb')
except:
    print("no default found. check filepath.")
#Begin process

try:
    Createoutputcomposite=localdatabaseroot+'\CompositeRaster\\'
    arcpy.CreateFileGDB_management(Createoutputcomposite,"CompositeRaster.gdb")
except:
    print("unable to create composite gdb")

try:
    StructureSpace=localdatabaseroot+'\ShapesAndStructures\StructureManipulation\\'
    arcpy.CreateFileGDB_management(StructureSpace,"ConvertedStructures.gdb")
except:
    print("unable to create structures gdb")
#Set main directory
maindirectory=r'C:\Users\harchena\Documents\Inside\Workspace' #change working folder for 3

listinfolder= os.listdir(maindirectory)
listofdirectoryrange=len(listinfolder)
valuereturntest=range(listofdirectoryrange)

#remove thumbs from array
try:
    for i in valuereturntest[::1]:
        if listinfolder[i].startswith("Thumbs.db"):
            listinfolder=listinfolder[:-1]
except:
    pass



#Start for loop

#NOTE: Although in theory these for loops can be nested, my computer fails to make the proper directories. This could be because of incorrect code... but this works all the same.

stor=len(listinfolder)
valuereturn=range(stor)
valuereturn=range(stor)
for i in valuereturn[::1]:
    pathname=listinfolder[i]
    subpath=maindirectory+"\\"+pathname
    damsubfolders=os.listdir(subpath)
    valuereturn2=range(len(damsubfolders))
    betterpathname=left(pathname,5)
    betterpathnameOUT.append(betterpathname)
    export=damdataroot+"\\"+betterpathname
    for i in valuereturn2[::1]:
        if damsubfolders[i].startswith("RasterFiles"):
            stor=damsubfolders[i]
            
            zipfilepath=maindirectory+"\\"+pathname+"\\"+stor+"\\"
            os.chdir(subpath)
            try:
                with zipfile.ZipFile(stor,"r") as zip_ref:
                    zip_ref.extractall(export)
            except:
                print("already unzipped")
                try:
                    root_src_dir=r'C:\Users\harchena\Documents\Inside\InundationScript'
                    root_dst_dir = 'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\DamData'
                    for src_dir, dirs, files in os.walk(root_src_dir):
                        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
                        if not os.path.exists(dst_dir):
                            os.makedirs(dst_dir)
                            for file_ in files:
                                src_file = os.path.join(src_dir, file_)
                                dst_file = os.path.join(dst_dir, file_)
                                if os.path.exists(dst_file):
                                    os.remove(dst_file)
                                shutil.copy(src_file, dst_dir)
                except:
                    pass
        time.sleep(1)
        
maindirectory=r'C:\Users\harchena\Documents\Inside\Workspace' #change working folder for 3

listinfolder= os.listdir(maindirectory)
listofdirectoryrange=len(listinfolder)
valuereturntest=range(listofdirectoryrange)

stor=len(listinfolder)
valuereturn=range(stor)

for i in valuereturn[::1]:
    pathname=listinfolder[i]
    subpath=maindirectory+"\\"+pathname
    damsubfolders=os.listdir(subpath)
    valuereturn2=range(len(damsubfolders))
    betterpathname=left(pathname,5)
    #betterpathnameOUT.append(betterpathname)
    export=damdataroot+"\\"+betterpathname
    for i in valuereturn2[::1]:        
        if damsubfolders[i].startswith("Final"):
            stor=damsubfolders[i]
            import zipfile
            zipfilepath=maindirectory+"\\"+pathname+"\\"+stor+"\\"
            import os
            os.chdir(subpath)
            try:
                with zipfile.ZipFile(stor,"r") as zip_ref:
                    zip_ref.extractall(export)
            except:
                print("already unzipped")
                try:
                    shutil.copytree(stor,export)
                except:
                    print("file error or duplicate... attempting to replace")
                    try:
                            os.remove(stor)
                            shutil.copytree(stor,export)
                    except:
                        print("unable to replace file.")
                        pass

maindirectory=r'C:\Users\harchena\Documents\Inside\Workspace' #change working folder for 3

listinfolder= os.listdir(maindirectory)
listofdirectoryrange=len(listinfolder)
valuereturntest=range(listofdirectoryrange)

stor=len(listinfolder)
valuereturn=range(stor)

valuereturn=range(stor)
for i in valuereturn[::1]:
    pathname=listinfolder[i]
    subpath=maindirectory+"\\"+pathname
    damsubfolders=os.listdir(subpath)
    valuereturn2=range(len(damsubfolders))
    betterpathname=left(pathname,5)
    #betterpathnameOUT.append(betterpathname)
    export=damdataroot+"\\"+betterpathname
    for i in valuereturn2[::1]:
        if damsubfolders[i].endswith("Structures.kmz"):
            try:
                stor=damsubfolders[i]
                stor3=str(stor)
                print("found the kmz")
                try:
                    kmzpath="C:\Users\harchena\Documents\Inside\Workspace\\"+betterpathname+"\\"+stor3
                    shutil.copy(kmzpath,export)
                except:
                    print("Won't copy")
                    pass
            except:
                pass
            
                
            
          


#Pull damn numbers from DIR
path=damdataroot
dir(path)
os.listdir(path)
damslist=os.listdir(path)

#loops name creation
listofdams=damslist
stor=len(listofdams)
valuereturn=range(stor)

Listoffiles=os.listdir(damdataroot + "\\"+ betterpathname+"\\")
valuereturn3=range(len(Listoffiles))

#Creation of RasterConversion folder

ListofDamFolders=os.listdir(damdataroot)
valuereturn4=range(len(ListofDamFolders))
for i in valuereturn4[::1]:
    try:
        for i in valuereturn4[::1]:
            if ListofDamFolders[i].startswith("Thumbs.db"):
                ListofDamFolders=ListofDamFolders[:-1]
    except:
        pass
for i in valuereturn4:
    try:
        RasterConvPath= damdataroot + betterpathnameOUT[i]+"\\RasterConversion\\"
        os.mkdir(RasterConvPath)
    except:
        print("Unable to create folder or already present")
        pass

#CreateConversion
    
stepwise=range(len(betterpathnameOUT))

for i in stepwise[::1]:
    folder=damdataroot +"\\"+ betterpathnameOUT[i] 
    x=os.listdir(folder)
    stepwisesub=range(len(x))
    Rasterlocations=damdataroot+"\\"+betterpathnameOUT[i]
    for z in stepwisesub[::1]:
        namecheck=mid(x[z],8,12)
        if namecheck=="FloodArrival":
            try:
                NameFlood=x[z]
                arcpy.MakeRasterLayer_management(Rasterlocations + "\\" +NameFlood,"ARRIVALRASTER")
                #outfile2="G:\\Dams\\EAP Effort\\Automation\\InundationLayerDatabase\\DamData\\" +betterpathnameOUT[i]+"\\RasterConversion\\"
                #arcpy.RasterToPoint_conversion("H:\\InundationLayerDatabase\DamData\\" + betterpathnameOUT[i]+"\\"+Name,outfile2+betterpathnameOUT[i]+"ConvertedArrivalRaster")
            except:
                print("Unable to convert raster to points... Check path. Mission aborted!")
    folder=damdataroot +"\\"+ betterpathnameOUT[i] 
    x=os.listdir(folder)
    stepwisesub=range(len(x))
    for z in stepwisesub[::1]:
        namecheck=mid(x[z],8,10)
        if namecheck=="FloodDepth":
            try:
                NameDepth=x[z]
                arcpy.MakeRasterLayer_management(Rasterlocations + "\\" + NameDepth,"DEPTHRASTER")
                #outfile2="G:\\Dams\\EAP Effort\\Automation\\InundationLayerDatabase\\DamData\\" +betterpathnameOUT[i]+"\\RasterConversion\\"
                #arcpy.RasterToPoint_conversion("H:\\InundationLayerDatabase\DamData\\" + betterpathnameOUT[i]+"\\"+Name,outfile2+betterpathnameOUT[i]+"ConvertedDepthRaster")
            except:
                print("Unable to convert raster to points... Check path. Mission aborted!")
    for z in stepwisesub[::1]:
        namecheck=mid(x[z],8,3)
        if namecheck=="DEM":
            try:
                print("Made it here")
                NameDEM=x[z]
                arcpy.MakeRasterLayer_management(Rasterlocations + "\\" + NameDEM,"DEMRASTER")
                #outfile2="G:\\Dams\\EAP Effort\\Automation\\InundationLayerDatabase\\DamData\\" +betterpathnameOUT[i]+"\\RasterConversion\\"
                #arcpy.RasterToPoint_conversion("H:\\InundationLayerDatabase\DamData\\" + betterpathnameOUT[i]+"\\"+Name,outfile2+betterpathnameOUT[i]+"ConvertedDEMRaster")
            except:
                print("Unable to convert raster to points... Check path. Mission aborted!")
    outputname=betterpathnameOUT[i]+"COMPOSITE"
    #outputcomposite='H:\\InundationLayerDatabase\CompositeRaster'
    arcpy.env.workspace = localdatabaseroot+'\CompositeRaster\CompositeRaster.gdb\\'
    arcpy.CompositeBands_management ("ARRIVALRASTER.tif;DEPTHRASTER.tif;DEMRASTER.tif",betterpathnameOUT[i]+"COMP")
    allcomposites.append(betterpathnameOUT[i]+"COMP")

    
#arcpy.CreateRasterDataset_management('H:\\InundationLayerDatabase\Database\MosaicRaster','mosaicraster.tif')

arcpy.CreateRasterDataset_management(localdatabaseroot+'\MosaicRaster\\','Mosaic.tif',"","16_BIT_UNSIGNED","",3)
arcpy.Mosaic_management(allcomposites,localdatabaseroot+'\MosaicRaster\Mosaic.tif',"","",0,0)
#arcpy.MosaicToNewRaster_management(allcomposites,localdatabaseroot+'\MosaicRaster','mosaicraster.tif',"","","",3)
#arcpy.CopyRaster_management(localdatabaseroot+"\MosaicRaster\mosaicraster.tif",localdatabaseroot+"\MosaicRaster\MosiacClear.tif","","",0)

#MOSAIC RASTER DONE- MOVING ON TO STRUCTURES AND BOUNDARY


for i in stepwise[::1]:
    folder=damdataroot +"\\"+betterpathnameOUT[i] 
    x=os.listdir(folder)
    stepwisesub=range(len(x))
    Rasterlocations=damdataroot+betterpathnameOUT[i]
    for z in stepwisesub[::1]:
        namecheck=mid(x[z],8,12)
        if x[z].endswith(".shp"):
            try:
                NameWetDry=x[z]
                arcpy.MakeFeatureLayer_management(damdataroot+"\\"+betterpathnameOUT[i]+"\\"+x[z],betterpathnameOUT[i]+"WETDRY")
                wetdrys.append(betterpathnameOUT[i]+"WETDRY")
                
                
                #outfile2="G:\\Dams\\EAP Effort\\Automation\\InundationLayerDatabase\\DamData\\" +betterpathnameOUT[i]+"\\RasterConversion\\"
                #arcpy.RasterToPoint_conversion("H:\\InundationLayerDatabase\DamData\\" + betterpathnameOUT[i]+"\\"+Name,outfile2+betterpathnameOUT[i]+"ConvertedArrivalRaster")
            except:
                print("Unable find WETDRY... Check path. Mission aborted!")

#merge wetdrys
try:
    Createoutputcomposite2=localdatabaseroot+'\ShapesAndStructures\\'
    arcpy.CreateFileGDB_management(Createoutputcomposite2,"ShapesAndStructures.gdb")
except:
    print("unable to create composite gdb")

duplicate=wetdrys
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list
     
# Driver Code
print(Remove(duplicate))
wetdrys=Remove(wetdrys)
arcpy.Merge_management(wetdrys,localdatabaseroot+'\ShapesAndStructures\ShapesAndStructures.gdb\MergedWetDry')


#import KMZ



arcpy.env.workspace = r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database\ShapesAndStructures'
for i in stepwise[::1]:
    folder=damdataroot +"\\"+ betterpathnameOUT[i] 
    x=os.listdir(folder)
    stepwisesub=range(len(x))
    Rasterlocations=damdataroot+"\\"+betterpathnameOUT[i]
    for z in stepwisesub[::1]:
        namecheck=mid(x[z],8,12)
        if x[z].endswith(".kmz"):
            try:
                KMZNAME=x[z]
                KMZEXPORT=localdatabaseroot+'\ShapesAndStructures\StructureManipulation\\'+betterpathnameOUT[i]+"KMZ"
                arcpy.KMLToLayer_conversion(damdataroot+"\\"+betterpathnameOUT[i]+"\\"+KMZNAME,KMZEXPORT)
                arcpy.FeatureToPoint_management(KMZEXPORT+"\\"+betterpathnameOUT[i]+"_Structures.gdb\\"+"Placemarks\Points\\",r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database\ShapesAndStructures\StructureManipulation\ConvertedStructures.gdb\\'+betterpathnameOUT[i]+"KMZCONVERTED")
                kmzconverted.append(betterpathnameOUT[i]+"KMZCONVERTED")
                #arcpy.FeatureToPoint_management(r"D0008_Structures\Points",r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database\ShapesAndStructures\ShapesAndStructures.gdb\\'+betterpathnameOUT[i]+"KMZCONVERTED")                
            except:
                pass
arcpy.env.workspace = localdatabaseroot+'\ShapesAndStructures\ShapesAndStructures.gdb'
                                   


#merge KMZ            
#arcpy.env.workspace = localdatabaseroot+'\ShapesAndStructures\ShapesAndStructures.gdb'
#although arcgis' python console has no errors without creating a layer first... regular python does. hence this strange section of code                                
arcpy.env.workspace = localdatabaseroot+"\ShapesAndStructures\ShapesAndStructures\StructureManipulation\ConvertedStructures.gdb\\"
structuremergestep=range(len(kmzconverted))
kmzfullpathOUT=[]
newlayer=[]
for i in structuremergestep[::1]:
    kmzfullpath=localdatabaseroot+"\ShapesAndStructures\ShapesAndStructures\StructureManipulation\ConvertedStructures.gdb\\"+kmzconverted[i]
    name=r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database\ShapesAndStructures\StructureManipulation\ConvertedStructures.gdb\\'+kmzconverted[i]
    kmzfullpathOUT.append(name)
listtest=[]
for q in structuremergestep[::1]:
    newlayer=arcpy.mapping.Layer(kmzfullpathOUT[q])
    listtest.append(newlayer)

arcpy.Merge_management(listtest,localdatabaseroot+'\ShapesAndStructures\ShapesAndStructures.gdb\MergedStructures')

#Copy Database for publish. You'd think you could just copy the file... but you can't because ARCGIS stores a .lock and doesn't let go 

time.sleep(10)
try:
    os.makedirs(r'M:\gisapp\EQCAPP\BW\HAZDAM\DSS_WISE\DSS_WISE_Lite_Mapbook_Processing\InundationUpload\Composites.gdb')
    os.makedirs(r'M:\gisapp\EQCAPP\BW\HAZDAM\DSS_WISE\DSS_WISE_Lite_Mapbook_Processing\InundationUpload\Mosaic')
    os.makedirs(r'M:\gisapp\EQCAPP\BW\HAZDAM\DSS_WISE\DSS_WISE_Lite_Mapbook_Processing\InundationUpload\ShapesAndStructures.gdb')

except:
    print('Unable to make enclosing folders. If your script has run successfully before, we will attempt to pass. If not, the script will break')


#Composites
root_src_dir = r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database\CompositeRaster\CompositeRaster.gdb'    #Path/Location of the source directory
root_dst_dir =r'M:\gisapp\EQCAPP\BW\HAZDAM\DSS_WISE\DSS_WISE_Lite_Mapbook_Processing\InundationUpload\Composites.gdb'  #Path to the destination folder

for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)
#Mosaic
root_src_dir = r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database\MosaicRaster'    #Path/Location of the source directory
root_dst_dir = r'M:\gisapp\EQCAPP\BW\HAZDAM\DSS_WISE\DSS_WISE_Lite_Mapbook_Processing\InundationUpload\Mosaic' #Path to the destination folder

for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)
#Shapes and structures
root_src_dir = r'C:\Users\harchena\Documents\Inside\InundationLayerDatabase\Database\ShapesAndStructures\ShapesAndStructures.gdb'    #Path/Location of the source directory
root_dst_dir = r'M:\gisapp\EQCAPP\BW\HAZDAM\DSS_WISE\DSS_WISE_Lite_Mapbook_Processing\InundationUpload\ShapesAndStructures.gdb'  #Path to the destination folder

for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)
#Success mesage

print("Operation complete. If you're missing a dam, please check the error logs for what went wrong. Signing off!")

arcpy.CreateFileGDB_management(Createoutputcomposite,"CompositeRaster.gdb")


