#!/bin/bash

source /home/raparelli/anaconda3/etc/profile.d/conda.sh
conda activate python3

echo "###############################################"
#telegram "####"

echo "Start"
telegram.sh "wrfout_merge_full.sh started"

DATE=$(date +"%Y-%m-%dT%H:%M")
echo "$DATE"
#telegram "$DATE"

#echo "Type your working_path"
#read working_path
#echo "Do you want to deaccumulate? (yes or no)"
#read deac_wrfout
#echo "Do you want to select a timestep range? (yes or no)"
#read timesel_wrfout

wrfout_path=$1
#wrfout_path="/media/Maxtor3/wrf-snow/T5"

working_path="$wrfout_path""/processed"
mkdir "$working_path"

swp_path="$working_path""/snowpack"
mkdir "$swp_path"

swp_path="$swp_path""/""$DATE"
mkdir "$swp_path"

swpin_path="$swp_path""/input"
mkdir "$swpin_path"

swpout_path="$swp_path""/output"
mkdir "$swpout_path"

mkdir "$swp_path""/setup"

wrf2surface_path="/home/raparelli/scripts/wrf2surface_full.py"
wrf2soil_path="/home/raparelli/scripts/wrf2soil.py"
wrf2snow_path="/home/raparelli/scripts/wrf2snow.py"

deaccumulate_path="/home/raparelli/scripts/deaccumulate.py"
deac_var_name="RAINNC,SNOWNC,GRAUPELNC,HAILNC,ACSNOM"

return_dim_size_path="/home/raparelli/scripts/return_dim_size.py"
dim_name="Time"
#start_step="8"
start_step="14"
#start_step="2"

time_var="XTIME"

#rectangular_grid_path="/home/raparelli/petrarca/wrf-snow/rectangular_grid.txt"
#rectangular_grid_path="/home/raparelli/data1/sim_paolo/wrf/rectangular_grid.txt"
#rectangular_grid_path="/home/raparelli/data1/sim_paolo/wrf/rectangular_grid_bartolini.txt"
#rectangular_grid_path="/home/raparelli/data1/sim_paolo/wrf/rectangular_grid_central_apennine.txt"
rectangular_grid_path="/home/raparelli/data1/sim_paolo/rectangular_grid_central_apennine_1km.txt"

#round_path="/home/raparelli/scripts/round.py"
#round_var_name="LU_INDEX"

nearest_path="/home/raparelli/scripts/nearest_remap.py"
nearest_var_name="LU_INDEX"

prevah_path="/home/raparelli/scripts/prevah2netcdf.py"

soilthick_path="/home/raparelli/scripts/soilthick2netcdf.py"

nowater_path="/home/raparelli/scripts/wrf_to_nowater.py"

rm "$swpin_path""/"*.nc
rm "$swpin_path""/"*.netcdf

cd "$wrfout_path"

for file in wrfout_ABR01* ; do

  echo "###############################################"
  #telegram "####"

  echo "File: ""$file"
  #telegram "File: ""$file"

  #echo output/"$file"
  #rm "$swpin_path""/""$file""_elab.nc"
  #cdo -seltimestep,1/24 -sellevidx,1 -selgrid,1 "$file" "$swpin_path""/""$file""_sel.nc"

  echo "Extracting"
  #cdo -sellevidx,1 -selgrid,1 "$file" "$swpin_path""/""$file""_sel.nc"
  python "$wrf2surface_path" "$file" "$swpin_path""/""$file""_surface.nc"
  #cdo -selzaxis,4 "$file" "$swpin_path""/""$file""_soil.nc"
  python "$wrf2soil_path" "$file" "$swpin_path""/""$file""_soil.nc"
  python "$wrf2snow_path" "$file" "$swpin_path""/""$file""_snow.nc"

  echo "Deaccumulating"
  #if [ "$deac_wrfout" == "yes" ]; then
  python "$deaccumulate_path" "$deac_var_name" "$swpin_path""/""$file""_surface.nc" "$swpin_path""/""$file""_deacc.nc"
  rm "$swpin_path""/""$file""_surface.nc"
    #file="$swpin_path""/""$file""_deacc.nc"
    #done
  #fi

  echo "Slicing"
  end_step="$(python "$return_dim_size_path" "$dim_name" "$swpin_path""/""$file""_deacc.nc")"
  #if [ "$timesel_wrfout" == "yes" ]; then
  cdo -seltimestep,"$start_step"/"$end_step" "$swpin_path""/""$file""_deacc.nc" "$swpin_path""/""$file""_surface_sel.nc"
  cdo -seltimestep,"$start_step"/"$end_step" "$swpin_path""/""$file""_soil.nc" "$swpin_path""/""$file""_soil_sel.nc"
  cdo -seltimestep,"$start_step"/"$end_step" "$swpin_path""/""$file""_snow.nc" "$swpin_path""/""$file""_snow_sel.nc"
  rm "$swpin_path""/""$file""_deacc.nc"
  rm "$swpin_path""/""$file""_soil.nc"
  rm "$swpin_path""/""$file""_snow.nc"
  #  file="$swpin_path""/""$file""_sel.nc"
  #  rm "$swpin_path""/""$file""_deacc.nc"
  #fi

  echo "Renaming time dimension and variable"
  ncrename -d "$time_var",time -v "$time_var",time "$swpin_path""/""$file""_surface_sel.nc"
  ncrename -d "$time_var",time -v "$time_var",time "$swpin_path""/""$file""_soil_sel.nc"
  ncrename -d "$time_var",time -v "$time_var",time "$swpin_path""/""$file""_snow_sel.nc"
  #cdo -O setreftime,1970-01-01,0,1s "$swpin_path""/""$file""_sel.nc" "$swpin_path""/""$file""_sel_epoch.nc"
  #cdo -a -copy "$swpin_path""/""$file""_sel.nc" "$swpin_path""/""$file""_sel_abs.nc"

done

# else
#
#   for file in wrfout* ; do
#     #echo "$file"
#     unlink "$swpin_path""/""$file"
#     ln -s "$file" "$swpin_path""/""$file"
#   done
#
# fi
echo "###############################################"

cd "$swpin_path"

echo "Merging"
cdo mergetime wrfout*"_surface_sel.nc" surface_merged.netcdf
cdo mergetime wrfout*"_soil_sel.nc" soil_merged.netcdf
cdo mergetime wrfout*"_snow_sel.nc" snow_merged.netcdf
rm -rf wrfout*

# echo "Reprojecting"
# cdo remapbil,"$rectangular_grid_path" surface_merged.netcdf surface_reprojected.netcdf
# cdo remapbil,"$rectangular_grid_path" soil_merged.netcdf soil_reprojected.netcdf
# #cdo remapbil,"$rectangular_grid_path" snow_merged.netcdf snow_reprojected.netcdf
# 
# #echo "Rounding"
# #python "$round_path" "$round_var_name" reprojected.netcdf rounded.netcdf
# 
# echo "$nearest_var_name"" nearest remapping"
# #python "$nearest_path" "$nearest_var_name" surface_merged.netcdf surface_reprojected.netcdf surface_nearest.netcdf
# cdo selvar,"$nearest_var_name" surface_merged.netcdf vars_to_remap_nn.netcdf
# cdo remapnn,"$rectangular_grid_path" vars_to_remap_nn.netcdf vars_remapped_nn.netcdf
# rm -rf vars_to_remap_nn.netcdf
# ncrename -v "$nearest_var_name","$nearest_var_name""_bil" surface_reprojected.netcdf surface_reprojected_renamed.netcdf
# cdo merge surface_reprojected_renamed.netcdf vars_remapped_nn.netcdf surface_nearest.netcdf
# rm -rf surface_reprojected_renamed.netcdf 
# rm -rf vars_remapped_nn.netcdf
# 
# echo "Extracting first timestep"
# ncks -O -d time,0 surface_nearest.netcdf surface_initial_step.netcdf
# ncks -O -d time,0 soil_reprojected.netcdf soil_initial_step.netcdf
# #ncks -O -d time,0 snow_reprojected.netcdf snow_initial_step.netcdf
# #ncks -O -d time,0 rounded.netcdf initial_step.netcdf
# 
# ######################## commentend because missing variables in netcdf
# echo "Adding Prevah Land Use"
# python "$prevah_path" surface_initial_step.netcdf surface_initial_step_prevah.netcdf 20
# echo "Adding thickness of soil levels"
# python "$soilthick_path" "$wrfout_path""/""$file" soil_initial_step.netcdf soil_initial_step_thick.netcdf
# #########################
# 
# echo "Excluding water surfaces"
# python "$nowater_path" surface_initial_step_prevah.netcdf prevah
# python "$nowater_path" surface_nearest.netcdf noprevah
# 
# echo "Preparing Alpine3D directories"
# alp_path="$working_path""/alpine3d"
# mkdir "$alp_path"
# 
# alp_path="$alp_path""/""$DATE"
# mkdir "$alp_path"
# 
# alpin_path="$alp_path""/input"
# mkdir "$alpin_path"
# mkdir "$alpin_path""/meteo"
# mkdir "$alpin_path""/snowfiles"
# mkdir "$alpin_path""/surface-grids"
# mkdir "$alpin_path""/poi"
# 
# alpout_path="$alp_path""/output"
# mkdir "$alpout_path"
# mkdir "$alpout_path""/grids"
# mkdir "$alpout_path""/snowfiles"
# 
# alpset_path="$alp_path""/setup"
# mkdir "$alpset_path"
# # 
# # #ln -s surface_nearest.netcdf "$alpin_path""/meteo/surface_nearest.netcdf"
# # #ln -s surface_initial_step_prevah.netcdf "$alpin_path""/surface-grids/surface_initial_step_prevah.netcdf"
# # 
# # ######################### commentend because not needed
# # #cp surface_nearest.netcdf "$alpin_path""/meteo/surface_nearest.netcdf"
# # #cp surface_initial_step_prevah.netcdf "$alpin_path""/surface-grids/surface_initial_step_prevah.netcdf"
# # #cp soil_initial_step_thick.netcdf "$alpin_path""/surface-grids/soil_initial_step_thick.netcdf"
# # #########################
# # 
# # echo "###############################################"
# # #telegram "####"

DATE=$(date +"%Y-%m-%dT%H:%M")
echo "$DATE"
#telegram "$DATE"

echo "Done"
telegram.sh "wrfout_merge_full.sh finished"

echo "###############################################"
#telegram "####"

exit 0
