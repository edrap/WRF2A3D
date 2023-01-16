# WRF2A3D

These scripts permit to prepare the output files of [WRF](https://www.mmm.ucar.edu/models/wrf) model simulations and use them as input files for [Alpine3D](https://www.slf.ch/en/services-and-products/alpine-3d.html) model.

## Usage example

The following commands show some examples of how to generate all the files necessary to force Alpine3D from WRF output data.

### Prepare the meteorological forcing for Alpine3D:
```console
meteoForcing.sh /media/Maxtor3/EXP1
```

### Prepare the initial conditions for Alpine3D:
```console
initCond.sh "/media/Maxtor3/EXP1/processed/alpine3d/2023-01-05T00:47/input/meteo" "wrfout_ABR01_2020-03-21_12:00:00_surface_nearest.nc" "wrfout_ABR01_2020-03-21_12:00:00_soil_reprojected.nc" "/media/Maxtor3/EXP1/wrfout_ABR01_2020-03-21_12:00:00"
```

### Generate the .sno files for Alpine3D snow/soil initial conditions:
```console
python sno_grid_generator.py surface_initial_step_prevah.nc soil_initial_step_thick.nc /home/edrap/alpine3d/vir_common.txt "/home/edrap/alpine3d/2023-01-04T13:22/input/snowfiles/" t0_ 20
```

