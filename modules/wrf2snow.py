#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings('ignore')
import xarray  as xr
import sys
from wrf import rh, tk

dataset_in = str(sys.argv[1])
dataset_out = str(sys.argv[2])

ds_wrf = xr.open_dataset(dataset_in)

ds_wrf_snow = xr.Dataset(data_vars=None)

variables = ["SNBC",
             "SNGRE",
             "SNICE",
             "SNLIQ",
             "TSNO"]

for var in variables:
    try:
        ds_wrf_snow[var] = ds_wrf[var]
    except Exception as e:
        print(e)

ds_wrf_snow["ZSSN"] = ds_wrf["ZSNSO"][:, 0:3, :, :]
ds_wrf_snow["ZSSN"].attrs["units"] = "-"
ds_wrf_snow["ZSSN"].attrs["FieldType"] = ds_wrf["ZSNSO"].attrs["FieldType"]
ds_wrf_snow["ZSSN"].attrs["MemoryOrder"] = "XY"
ds_wrf_snow["ZSSN"].attrs["description"] = "THICKNESS OF SNOW LAYERS"
ds_wrf_snow["ZSSN"].attrs["stagger"] = ""

ds_wrf_snow.to_netcdf(dataset_out, 'w')
