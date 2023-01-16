#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings('ignore')
from wrf_utils import find_nearest_couple_idx
import xarray  as xr
import sys

var = sys.argv[1].split(',')
dataset_in_orig = str(sys.argv[2])
dataset_in_repr = str(sys.argv[3])
dataset_out = str(sys.argv[4])

ds_m = xr.open_dataset(dataset_in_orig)
ds_r = xr.open_dataset(dataset_in_repr)

if var != ['']:

    for i in range(0, ds_r.lat.shape[0]):
        for j in range(0, ds_r.lon.shape[0]):
            latlon_couples = find_nearest_couple_idx(ds_m.XLAT, ds_m.XLONG, ds_r.lat[i], ds_r.lon[j])       
            for v in var:
                ds_r[v][0, i, j] = ds_m[v][0, latlon_couples[0], latlon_couples[1]]

    for k in range(1, ds_r.time.shape[0]):
        for v in var:
            ds_r[v][k, :, :] = ds_r[v][0]

ds_r.to_netcdf(dataset_out)




