#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import warnings
warnings.filterwarnings('ignore')
import xarray  as xr
from landuse_utils import getPrevah, getModis, modis2prevah
import pandas as pd
import numpy as np
from snowpack_utils import sno_gen_soil

dataset_in = str(sys.argv[1])
dataset_soil = str(sys.argv[2])
vir_common_path = str(sys.argv[3])
sno_path = str(sys.argv[4])
sno_prefix = str(sys.argv[5])
modisversion = int(sys.argv[6])

ds = xr.open_dataset(dataset_in)
dss = xr.open_dataset(dataset_soil)

ProfileDate = ds.time[0].values

nSoilLayerData = dss["DZS"].shape[0]

fr1 = open(vir_common_path, "r").read()

prevah_map = getPrevah()
modis_map = getModis(modisversion)
modis2preva_map = modis2prevah(modisversion)

virnum = 1

for i in range(0, ds.lat.shape[0]):
    #print(i)
    for j in range(0, ds.lon.shape[0]):

        if int(ds["LANDMASK"][0,i,j].values) > 0:

            fw1_path = sno_path+"/"+sno_prefix+str(virnum)+".sno"
            open(fw1_path, "w").close()

            sno_gen_soil(ds, dss, ProfileDate, nSoilLayerData, fr1, prevah_map,
                         modis_map, modis2preva_map, i, j, fw1_path, virnum, "VIR"+str(virnum))

            virnum+=1
