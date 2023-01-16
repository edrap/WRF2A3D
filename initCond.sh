#!/bin/bash


###### PATH TO PYTHON SCRIPTS ######

pyscripts_path="path to pyscripts"

prevah_path=$pyscripts_path"/prevah2netcdf.py"
soilthick_path=$pyscripts_path"/soilthick2netcdf.py"
nowater_path=$pyscripts_path"/wrf_to_nowater.py"


###### SCRIPT ARGUMENTS ######

a3d_inpath=$1    # PATH TO INPUT/METEO DIRECTORY
surface_file=$2    # PATH TO _surface_nearest.nc FILE
soil_file=$3    # PATH TO _soil_reprojected.nc FILE
orig_file=$4    # PATH TO ORIGINAL WRFOUT FILE


###### WRFOUT PROCESSING ######

echo "###############################################"

echo "Start"

DATE=$(date +"%Y-%m-%dT%H:%M")
echo $DATE

cd $a3d_inpath

echo "Extracting first timestep"
ncks -O -d time,0 $surface_file surface_initial_step.nc
ncks -O -d time,0 $soil_file soil_initial_step.nc

echo "Adding Prevah Land Use"
python "$prevah_path" surface_initial_step.nc surface_initial_step_prevah.nc 20

echo "Adding thickness of soil levels"
python $soilthick_path $orig_file soil_initial_step.nc soil_initial_step_thick.nc

echo "Excluding sea surfaces"
python $nowater_path surface_initial_step_prevah.nc prevah

echo "###############################################"

DATE=$(date +"%Y-%m-%dT%H:%M")
echo "$DATE"

echo "Done"

echo "###############################################"

exit 0
