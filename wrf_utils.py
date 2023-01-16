import numpy as np
import pandas as pd
import xarray as xr

def find_nearest(array, value):
    #array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def find_nearest_idx(array, value):
    #array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def find_nearest_couple_idx(xlat, xlon, vlat, vlon):
    #array = np.asarray(array)
    idx = np.unravel_index((np.abs(xlat-vlat)+np.abs(xlon-vlon)).argmin(), xlat.shape)
    return idx#, matrix[idx]

def interpBil(ds, vlat, vlon, latname, lonname):

    # ds: variabile di interesse estratta da dataframe netcdf
    # vlat: latitudine di interesse
    # vlon: longitudine di interesse
    # latname: nome variabile latitudine nel dataframe netcdf
    # lonname: nome variabile longitudine nel dataframe netcdf

    # construzione array latitudine e longitudine
    ds_lon = ds[lonname].values
    ds_lat = ds[latname].values

    # estremi del dominio del netcdf
    ds_lon_min = ds_lon.min()
    ds_lat_min = ds_lat.min()
    ds_lon_max = ds_lon.max()
    ds_lat_max = ds_lat.max()

    # condizione di appartenenza di vlat e vlon al dominio del netcdf
    if  vlon > ds_lon_min and vlon < ds_lon_max and vlat > ds_lat_min and vlat < ds_lat_max:

        # calcolo del passo di griglia (necessaria griglia a passo costante)
        delta_lon = ds_lon[1] - ds_lon[0]
        delta_lat = ds_lat[1] - ds_lat[0]

        #### algoritmo di interpolazione ####

        # calcolo degli indici dei punti griglia con latitudine e longitudine più prossime (inferiori o uguali) alle coordinate vlat e vlon
        lonIdx = int((vlon - ds_lon_min)/delta_lon)
        latIdx = int((vlat - ds_lat_min)/delta_lat)

        x = vlon
        y = vlat

        # calcolo coordinate dei 4 punti contenenti il punto di coordinate vlat e vlon
        x1 = ds_lon[lonIdx]
        x2 = ds_lon[lonIdx+1]
        y1 = ds_lat[latIdx]
        y2 = ds_lat[latIdx+1]

        a  =  (x2-x1)*(y2-y1)

        # fq** sono serie temporali della variabile di interesse estratte alle coordinate x* ed y*
        if len(ds.dims) == 3:
            fq11 = ds.loc[:, y1, x1]
            fq21 = ds.loc[:, y1, x2]
            fq12 = ds.loc[:, y2, x1]
            fq22 = ds.loc[:, y2, x2]
            
        elif len(ds.dims) == 2:
            fq11 = ds.loc[y1, x1]
            fq21 = ds.loc[y1, x2]
            fq12 = ds.loc[y2, x1]
            fq22 = ds.loc[y2, x2]
            
        b = fq11*(x2-x)*(y2-y) + fq21*(x-x1)*(y2-y) + fq12*(x2-x)*(y-y1) + fq22*(x-x1)*(y-y1)

        ts = (b/a).to_pandas() # converte una serie temporale netcdf in pandas

        #### fine algoritmo di interpolazione ####

    # condizione di non appartenenza di vlat e vlon al dominio del netcdf
    else:

        ts = np.nan

    return ts

def interpNear(ds, vlat, vlon, latname, lonname):

    # ds: variabile di interesse estratta da dataframe netcdf
    # vlat: latitudine di interesse
    # vlon: longitudine di interesse
    # latname: nome variabile latitudine nel dataframe netcdf
    # lonname: nome variabile longitudine nel dataframe netcdf

    # construzione array latitudine e longitudine
    ds_lon = ds[lonname].values
    ds_lat = ds[latname].values

    # estremi del dominio del netcdf
    ds_lon_min = ds_lon.min()
    ds_lat_min = ds_lat.min()
    ds_lon_max = ds_lon.max()
    ds_lat_max = ds_lat.max()

    # condizione di appartenenza di vlat e vlon al dominio del netcdf
    if  vlon > ds_lon_min and vlon < ds_lon_max and vlat > ds_lat_min and vlat < ds_lat_max:
        
        # trova gli indici della cella più vicina al punto desiderato
        lonIdx = int((vlon - ds_lon_min)/delta_lon)
        latIdx = int((vlat - ds_lat_min)/delta_lat)
        #print(idx)
        #print(ds)
        
        # converte una serie temporale netcdf in pandas
        if len(ds.dims) == 3:
            ts = ds[:, latIdx, lonIdx].to_pandas()
        elif len(ds.dims) == 2:
            ts = ds[latIdx, lonIdx].to_pandas()

        #### fine algoritmo di interpolazione ####

    # condizione di non appartenenza di vlat e vlon al dominio del netcdf
    else:

        ts = np.nan

    return ts

def interpIDWCurv(ds, vlat, vlon, latname, lonname):

    # ds: variabile di interesse estratta da dataframe netcdf
    # vlat: latitudine di interesse
    # vlon: longitudine di interesse
    # latname: nome variabile latitudine nel dataframe netcdf
    # lonname: nome variabile longitudine nel dataframe netcdf

    # construzione array latitudine e longitudine
    ds_lon = ds[lonname].values
    ds_lat = ds[latname].values

    # estremi del dominio del netcdf
    ds_lon_min = ds_lon.min()
    ds_lat_min = ds_lat.min()
    ds_lon_max = ds_lon.max()
    ds_lat_max = ds_lat.max()

    # condizione di appartenenza di vlat e vlon al dominio del netcdf
    if  vlon > ds_lon_min and vlon < ds_lon_max and vlat > ds_lat_min and vlat < ds_lat_max:

        #### algoritmo di interpolazione ####

        # calcolo degli indici dei punti griglia con latitudine e longitudine più prossime (inferiori o uguali) alle coordinate vlat e vlon
        idx = find_nearest_couple_idx(ds_lat, ds_lon, vlat, vlon)
        idx0 = idx[0]
        idx1 = idx[1]
        
        x = vlon
        y = vlat

        if ds_lat[idx0, idx1] == vlat and ds_lon[idx0, idx1] == vlon:
            if len(ds.dims) == 3:
                ts = ds[:, idx0, idx1].to_pandas()

            elif len(ds.dims) == 2:
                ts = ds[idx0, idx1].to_pandas()
        
        else:
            # calcolo coordinate dei 4 punti contenenti il punto di coordinate vlat e vlon
            if ds_lat[idx0, idx1] <= vlat and ds_lon[idx0, idx1] < vlon:
                x1 = idx1
                x2 = idx1+1
                y1 = idx0
                y2 = idx0+1

            if ds_lat[idx0, idx1] <= vlat and ds_lon[idx0, idx1] > vlon:
                x1 = idx1-1
                x2 = idx1
                y1 = idx0
                y2 = idx0+1

            if ds_lat[idx0, idx1] > vlat and ds_lon[idx0, idx1] <= vlon:
                x1 = idx1
                x2 = idx1+1
                y1 = idx0-1
                y2 = idx0

            if ds_lat[idx0, idx1] > vlat and ds_lon[idx0, idx1] >= vlon:
                x1 = idx1-1
                x2 = idx1
                y1 = idx0-1
                y2 = idx0            

            # fq** sono serie temporali della variabile di interesse estratte alle coordinate x* ed y*
            if len(ds.dims) == 3:
                fq11 = ds[:, y1, x1]
                fq21 = ds[:, y1, x2]
                fq12 = ds[:, y2, x1]
                fq22 = ds[:, y2, x2]

            elif len(ds.dims) == 2:
                fq11 = ds[y1, x1]
                fq21 = ds[y1, x2]
                fq12 = ds[y2, x1]
                fq22 = ds[y2, x2]

            w11 = 1./np.sqrt((ds_lat[y1, x1] - y)**2 + (ds_lon[y1, x1] - x)**2)
            w21 = 1./np.sqrt((ds_lat[y1, x2] - y)**2 + (ds_lon[y1, x2] - x)**2)
            w12 = 1./np.sqrt((ds_lat[y2, x1] - y)**2 + (ds_lon[y2, x1] - x)**2)
            w22 = 1./np.sqrt((ds_lat[y2, x2] - y)**2 + (ds_lon[y2, x2] - x)**2)

            a = w11 + w21 + w12 + w22
            b = fq11*w11 + fq21*w21 + fq12*w12 + fq22*w22

            ts = (b/a).to_pandas() # converte una serie temporale netcdf in pandas
        
        #### fine algoritmo di interpolazione ####

    # condizione di non appartenenza di vlat e vlon al dominio del netcdf
    else:

        ts = np.nan

    return ts

def interpNearCurv(ds, vlat, vlon, latname, lonname):

    # ds: variabile di interesse estratta da dataframe netcdf
    # vlat: latitudine di interesse
    # vlon: longitudine di interesse
    # latname: nome variabile latitudine nel dataframe netcdf
    # lonname: nome variabile longitudine nel dataframe netcdf

    # construzione array latitudine e longitudine
    ds_lon = ds[lonname].values
    ds_lat = ds[latname].values

    # estremi del dominio del netcdf
    ds_lon_min = ds_lon.min()
    ds_lat_min = ds_lat.min()
    ds_lon_max = ds_lon.max()
    ds_lat_max = ds_lat.max()

    # condizione di appartenenza di vlat e vlon al dominio del netcdf
    if  vlon > ds_lon_min and vlon < ds_lon_max and vlat > ds_lat_min and vlat < ds_lat_max:
        
        # trova gli indici della cella più vicina al punto desiderato
        idx = find_nearest_couple_idx(ds_lat, ds_lon, vlat, vlon)
        #print(idx)
        #print(ds)
        
        # converte una serie temporale netcdf in pandas
        if len(ds.dims) == 3:
            ts = ds[:, idx[0], idx[1]].to_pandas()
        elif len(ds.dims) == 2:
            ts = ds[idx[0], idx[1]].to_pandas()

        #### fine algoritmo di interpolazione ####

    # condizione di non appartenenza di vlat e vlon al dominio del netcdf
    else:

        ts = np.nan

    return ts
