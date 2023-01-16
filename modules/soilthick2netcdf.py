#!/usr/bin/env python
# coding: utf-8

import xarray  as xr
import sys

dataset_in_orig = str(sys.argv[1])
dataset_in_soil = str(sys.argv[2])
dataset_out = str(sys.argv[3])

ds_orig = xr.open_dataset(dataset_in_orig)
ds_soil = xr.open_dataset(dataset_in_soil)

ds_soil["DZS"] = ds_orig["DZS"][0]

ds_soil.to_netcdf(dataset_out, 'w')
