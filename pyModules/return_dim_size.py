import sys
import warnings
warnings.filterwarnings('ignore')
import xarray  as xr

var = sys.argv[1]
dataset_in = str(sys.argv[2])

ds = xr.open_dataset(dataset_in)

print(ds.Time.values.shape[0])
