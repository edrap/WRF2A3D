import warnings
warnings.filterwarnings('ignore')
import xarray  as xr
import sys

dataset_in = str(sys.argv[1])
prevah_cond = str(sys.argv[2])

ds_wrf = xr.open_dataset(dataset_in)

ds_wrf = ds_wrf.where(ds_wrf["LANDLAKEMASK"] > 0).fillna(-999)

ds_wrf.to_netcdf(dataset_in[0:-3]+"_no_sea.nc", "w")
