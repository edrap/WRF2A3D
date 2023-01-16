#!/bin/bash


###### PATH TO PYTHON SCRIPTS ######

pyscripts_path="path to pyscripts"

wrf2surface_path=$pyscripts_path"/wrf2surface_full.py"
wrf2soil_path=$pyscripts_path"/wrf2soil.py"
wrf2snow_path=$pyscripts_path"/wrf2snow.py"
deaccumulate_path=$pyscripts_path"/deaccumulate.py"
return_dim_size_path=$pyscripts_path"/return_dim_size.py"
nearest_path=$pyscripts_path"/nearest_remap.py"
prevah_path=$pyscripts_path"/prevah2netcdf.py"
soilthick_path=$pyscripts_path"/soilthick2netcdf.py"
nowater_path=$pyscripts_path"/wrf_to_nowater.py"


###### CONFIGURATION PARAMETERS ######

deac_var_name="RAINNC,SNOWNC,GRAUPELNC,HAILNC,ACSNOM"
dim_name="Time"
start_step="14"
time_var="XTIME"
nearest_var_name="LU_INDEX,LANDLAKEMASK"


###### PATH TO RECTANGULAR GRID DEFINITION FOR CDO REMAP ######

rectangular_grid_path="path to rectangular grid"


###### SCRIPT ARGUMENTS ######

wrfout_path=$1    # WRFOUT PATH


###### WRFOUT PROCESSING ######

echo "###############################################"

echo "Start"

DATE=$(date +"%Y-%m-%dT%H:%M")
echo $DATE

working_path=$wrfout_path/processed
mkdir $working_path

swp_path=$working_path/alpine3d
mkdir $swp_path

swp_path=$swp_path/$DATE
mkdir $swp_path

swpin_path=$swp_path/input
mkdir $swpin_path
mkdir $swpin_path/meteo
mkdir $swpin_path/snowfiles
mkdir $swpin_path/poi

swpout_path=$swp_path/output
mkdir $swpout_path
mkdir $swpout_path/grids
mkdir $swpout_path/snowfiles

mkdir $swp_path/setup

swpmeteo_path=$swpin_path/meteo

rm $swpmeteo_path/*.nc

cd $wrfout_path

for file in wrfout* ; do

  echo "###############################################"

  echo "File: "$file

  echo "Extracting"
  python $wrf2surface_path $file $swpmeteo_path/$file"_surface.nc"
  python $wrf2soil_path $file $swpmeteo_path/$file"_soil.nc"
  python $wrf2snow_path $file $swpmeteo_path/$file"_snow.nc"

  cd $swpmeteo_path
  
  echo "Deaccumulating"
  python $deaccumulate_path $deac_var_name $file"_surface.nc" $file"_deacc.nc"
  rm $file"_surface.nc"

  echo "Slicing"
  end_step="$(python $return_dim_size_path $dim_name $file"_deacc.nc")"
  cdo -seltimestep,$start_step/$end_step $file"_deacc.nc" $file"_surface_sel.nc"
  cdo -seltimestep,$start_step/$end_step $file"_soil.nc" $file"_soil_sel.nc"
  cdo -seltimestep,$start_step/$end_step $file"_snow.nc" $file"_snow_sel.nc"
  rm $file"_deacc.nc"
  rm $file"_soil.nc"
  rm $file"_snow.nc"

  echo "Renaming time dimension and variable"
  ncrename -d $time_var,time -v $time_var,time $file"_surface_sel.nc"
  ncrename -d $time_var,time -v $time_var,time $file"_soil_sel.nc"
  ncrename -d $time_var,time -v $time_var,time $file"_snow_sel.nc"
  
  echo "Reprojecting"
  cdo remapbil,$rectangular_grid_path $file"_surface_sel.nc" $file"_surface_reprojected.nc"
  cdo remapbil,$rectangular_grid_path $file"_soil_sel.nc"    $file"_soil_reprojected.nc"

  echo $nearest_var_name" nearest remapping"
  cdo selvar,$nearest_var_name $file"_surface_sel.nc" vars_to_remap_nn.nc
  cdo remapnn,$rectangular_grid_path vars_to_remap_nn.nc vars_remapped_nn.nc
  rm -rf vars_to_remap_nn.nc
  cdo delvar,$nearest_var_name $file"_surface_reprojected.nc" surface_reprojected_removed.nc
  cdo merge surface_reprojected_removed.nc vars_remapped_nn.nc $file"_surface_nearest.nc"
  rm -rf surface_reprojected_removed.nc 
  rm -rf vars_remapped_nn.nc

  echo "Excluding sea surfaces"
  python $nowater_path $file"_surface_nearest.nc" noprevah
 
  cd $wrfout_path
  
done

echo "###############################################"

DATE=$(date +"%Y-%m-%dT%H:%M")
echo "$DATE"

echo "Done"

echo "###############################################"

exit 0
