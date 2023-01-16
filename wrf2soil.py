#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings('ignore')
import xarray  as xr # NetCDF library
import sys
from wrf import rh, tk

dataset_in = str(sys.argv[1])
dataset_out = str(sys.argv[2])

ds_wrf = xr.open_dataset(dataset_in)

ds_wrf_soil = xr.Dataset(data_vars=None)

variables = [
             "TSLB",
             "SMOIS",
             "SH2O"
            ]

for var in variables:
    ds_wrf_soil[var] = ds_wrf[var]

ds_wrf_soil.to_netcdf(dataset_out, 'w')
