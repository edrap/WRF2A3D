#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import warnings
warnings.filterwarnings('ignore')
import xarray  as xr

var = sys.argv[1].split(',')
dataset_in = str(sys.argv[2])
dataset_out = str(sys.argv[3])

ds = xr.open_dataset(dataset_in)

timesteps = ds.Time.values.shape[0] - 1

for timestep in range(timesteps, 0, -1):
    
    for v in var:
        
        if v in list(ds.variables):
            ds[v][timestep] = ds[v][timestep] - ds[v][timestep-1]
        else:
            print(v+" not in NetCDF variables")
        
ds.to_netcdf(dataset_out)
