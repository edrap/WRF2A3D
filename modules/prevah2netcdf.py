import xarray  as xr # NetCDF library
from landuse_utils import getPrevah, getModis, modis2prevah
import sys

dataset_in = str(sys.argv[1])
dataset_out = str(sys.argv[2])
modisversion = int(sys.argv[3])

ds = xr.open_dataset(dataset_in)

prevah_map = getPrevah()
modis_map = getModis(modisversion)
modis2preva_map = modis2prevah(modisversion)

ds["LUS"] = ds["LU_INDEX"].copy(deep=True)
ds["LUS"].attrs["description"] = "Prevah Land Use"

for i in range(0, ds.lat.shape[0]):
    for j in range(0, ds.lon.shape[0]):
        lui_modis = int(ds["LU_INDEX"][0,i,j].values)
        lui_prevah = modis2preva_map[lui_modis]
        ds["LUS"][0, i, j] = lui_prevah
        
ds.to_netcdf(dataset_out, 'w')
