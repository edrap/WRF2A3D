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

ds_wrf_mono = xr.Dataset(data_vars=None)

variables = ["ACSNOM",
             "ALBEDO",
             "ALBOLD",
             "GRAUPELNC",
             "ISNOW",
             "LWDNB",
             "LWUPB",
             "Q2",
             "RAINNC",
             "GRAUPELNC",
             "HAILNC",
             "SNBCTOP",
             "SNEQVO",
             "SNGRETOP",
             "SNOW",
             "SNOWC",
             "SNOWH",
             "SNOWNC",
             "SR",
             "SWDOWN",
             "SWUPB",
             "T2",
             "TG",
             "U10",
             "V10",
             "HGT",
             "PSFC",
             "SFROFF",
             "TSK",
             "LU_INDEX",
             "LAI",
             "ALBBCK",
             "LANDMASK",
             "LAKEMASK"]

for var in variables:
    ds_wrf_mono[var] = ds_wrf[var]

ds_wrf_mono["LANDLAKEMASK"] = ds_wrf["LANDMASK"] + ds_wrf["LAKEMASK"]
ds_wrf_mono["LANDLAKEMASK"].attrs["units"] = "-"
ds_wrf_mono["LANDLAKEMASK"].attrs["FieldType"] = ds_wrf["LANDMASK"].attrs["FieldType"]
ds_wrf_mono["LANDLAKEMASK"].attrs["MemoryOrder"] = "XY"
ds_wrf_mono["LANDLAKEMASK"].attrs["description"] = "Land mask plus lake mask"
ds_wrf_mono["LANDLAKEMASK"].attrs["stagger"] = ""

ds_wrf_mono["PSUM_PH"] = 1 - ds_wrf["SR"]
ds_wrf_mono["PSUM_PH"].attrs["units"] = "-"
ds_wrf_mono["PSUM_PH"].attrs["FieldType"] = ds_wrf["SR"].attrs["FieldType"]
ds_wrf_mono["PSUM_PH"].attrs["MemoryOrder"] = "XY"
ds_wrf_mono["PSUM_PH"].attrs["description"] = "Precipitation phase"
ds_wrf_mono["PSUM_PH"].attrs["stagger"] = ""

ds_wrf_mono["PSUM_S"] = ds_wrf["SNOWNC"] + ds_wrf["GRAUPELNC"]
ds_wrf_mono["PSUM_S"].attrs["units"] = "mm"
ds_wrf_mono["PSUM_S"].attrs["FieldType"] = ds_wrf["SNOWNC"].attrs["FieldType"]
ds_wrf_mono["PSUM_S"].attrs["MemoryOrder"] = "XY"
ds_wrf_mono["PSUM_S"].attrs["description"] = "ACCUMULATED TOTAL GRID SCALE LIQUID PRECIPITATION"
ds_wrf_mono["PSUM_S"].attrs["stagger"] = ""

ds_wrf_mono["PSUM_L"] = ds_wrf["RAINNC"] - ds_wrf_mono["PSUM_S"]
ds_wrf_mono["PSUM_L"].attrs["units"] = "mm"
ds_wrf_mono["PSUM_L"].attrs["FieldType"] = ds_wrf["RAINNC"].attrs["FieldType"]
ds_wrf_mono["PSUM_L"].attrs["MemoryOrder"] = "XY"
ds_wrf_mono["PSUM_L"].attrs["description"] = "ACCUMULATED TOTAL GRID SCALE SOLID PRECIPITATION"
ds_wrf_mono["PSUM_L"].attrs["stagger"] = ""

#ds_wrf_mono["QI"] = ds_wrf["QVAPOR"][:,0,:,:]
#ds_wrf_mono["QI"].attrs["units"] = "kg kg-1"
#ds_wrf_mono["QI"].attrs["FieldType"] = ds_wrf["Q2"].attrs["FieldType"]
#ds_wrf_mono["QI"].attrs["MemoryOrder"] = "XY"
#ds_wrf_mono["QI"].attrs["description"] = "ZERO LEVEL WATER VAPOUR MIXING RATIO"
#ds_wrf_mono["QI"].attrs["stagger"] = ""
#
#ds_wrf_mono["P"] = ds_wrf["P"][:,0,:,:]
#ds_wrf_mono["P"].attrs["units"] = "Pa"
#ds_wrf_mono["P"].attrs["FieldType"] = ds_wrf["P"].attrs["FieldType"]
#ds_wrf_mono["P"].attrs["MemoryOrder"] = "XY"
#ds_wrf_mono["P"].attrs["description"] = "ZERO LEVEL PERTURBATION PRESSURE"
#ds_wrf_mono["P"].attrs["stagger"] = ""
#
#ds_wrf_mono["PB"] = ds_wrf["PB"][:,0,:,:]
#ds_wrf_mono["PB"].attrs["units"] = "Pa"
#ds_wrf_mono["PB"].attrs["FieldType"] = ds_wrf["PB"].attrs["FieldType"]
#ds_wrf_mono["PB"].attrs["MemoryOrder"] = "XY"
#ds_wrf_mono["PB"].attrs["description"] = "ZERO LEVEL BASE STATE PRESSURE"
#ds_wrf_mono["PB"].attrs["stagger"] = ""
#
ds_wrf_mono["TSLB"] = ds_wrf["TG"]
ds_wrf_mono["TSLB"].attrs["units"] = "K"
ds_wrf_mono["TSLB"].attrs["FieldType"] = ds_wrf["TG"].attrs["FieldType"]
ds_wrf_mono["TSLB"].attrs["MemoryOrder"] = "XY"
ds_wrf_mono["TSLB"].attrs["description"] = "ZERO LEVEL SOIL TEMPERATURE"
ds_wrf_mono["TSLB"].attrs["stagger"] = ""

#ds_wrf_mono["TA"] = (ds_wrf["T"][:,0,:,:]+300.) * ((ds_wrf["PB"][:,0,:,:] + ds_wrf["P"][:,0,:,:])/100000.)**0.2854
#ds_wrf_mono["TA"].attrs["units"] = "K"
#ds_wrf_mono["TA"].attrs["FieldType"] = ds_wrf["T2"].attrs["FieldType"]
#ds_wrf_mono["TA"].attrs["MemoryOrder"] = "XY"
#ds_wrf_mono["TA"].attrs["description"] = "ZERO LEVEL AIR TEMPERATURE"
#ds_wrf_mono["TA"].attrs["stagger"] = ""

#ds_wrf_mono["TA"] = tk(ds_wrf_mono["P"]+ds_wrf_mono["PB"], ds_wrf["T"][:,0,:,:]+300.)

#ds_wrf_mono["RH"] = rh(ds_wrf_mono["QI"], ds_wrf_mono["P"]+ds_wrf_mono["PB"], ds_wrf_mono["TA"])
ds_wrf_mono["R2"] = rh(ds_wrf_mono["Q2"], ds_wrf_mono["PSFC"], ds_wrf_mono["T2"])

ds_wrf_mono.to_netcdf(dataset_out, 'w')
