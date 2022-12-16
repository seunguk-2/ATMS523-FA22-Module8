#!/usr/bin/env python

import xarray as xr
import numpy as np
import pandas as pd
from functions import *

# Load daily soil moisture data and its climatology
smd = xr.open_dataset('~/b/2LDRM/jupyter/era5_sm_daily.nc')
smdc = xr.open_dataset('~/b/2LDRM/jupyter/era5_sm_daily_clim.nc')

# Load daily evapotranspiration data and its climatology
eed = xr.open_dataset('~/b/2LDRM/jupyter/era5_daily_e.nc')
eedc = xr.open_dataset('~/b/2LDRM/jupyter/era5_daily_clim_e.nc')

for yyi in np.arange(1980, 2020):
    ndd = 365 + int(np.mod(yyi,4) == 0)
    aprs = 90 + int(np.mod(yyi,4) == 0)  # Numeric day of April 1st
    spte = aprs + 183  # September 30th
    dom = 123  # Number of grid points in the Midwest (from 2L-DRM result)

    pth = '/data/keeling/a/seunguk2/c/2LDRM/pydlmb/'
    fd = np.fromfile(pth + str(yyi) + '_trj_L_DK.dat',dtype=np.single)  # back trajectory data from 2L-DRM
    fd[np.abs(fd)<1e-7] = np.nan
    fd = np.reshape(fd,(ndd,dom,2,-1))
    np.shape(fd)

    # trajectories at the first ten dates
    fd = fd[:,:,:,1:481:48]

    # re-arrange grid points for easier extraction of SM, ET anomalies
    # It's like changing the following raw data 
    # 123456...
    # 012345...
    # to
    # N123456...
    # 012345....
    fd_new = np.zeros(fd.shape)
    for i in range(ndd-9):
        for j in range(10):
            fd_new[i,:,:,j] = fd[i+j,:,:,j]

    # Initialize SM and ET anomaly data array
    ttta2 = np.zeros((183,10)) # 183 days within Apr01 and Sep30. 10 days of back trajectory
    ttea2 = np.zeros((183,10))

    for k in np.arange(aprs,spte):
        dn = k

        px = np.zeros(fd_new[dn,:,0,:].shape)  # 0 for x
        py = np.zeros(fd_new[dn,:,1,:].shape)  # 1 for y
        for i in range(dom):
            px[i,:] = fd_new[dn,i,0,:]
            py[i,:] = fd_new[dn,i,1,:]

        pxg, pyg = invlambxy(px-75000*61, py)  # converting grid info from km to degree
        ttta = nSMvvc(pxg, pyg, dn, yyi, smd, smdc)  # SM anomaly
        ttea = nETvvc(pxg, pyg, dn, yyi, eed, eedc)  # ET anomaly

        # Set of anomalies per day for the warm season
        ttta2[dn-aprs,:] = np.nanmean(ttta, axis=0)
        ttea2[dn-aprs,:] = np.nanmean(ttea, axis=0)

    ttea2[ttea2 == 0] = np.nan
    ttta2[ttta2 == 0] = np.nan
        
    # Make anomalies as xarray dataset
    ano_tmp_ds = xr.Dataset(data_vars=dict(sm_ano = (["time","day_back"],ttta2), 
                                           et_ano = (["time","day_back"],ttea2)),
                            coords=dict(time= smd.time.sel(time=slice(str(yyi)+'-04-01',str(yyi)+'-09-30')).values,
                                        day_back=np.arange(1,11))
                   )

    # Merge anomalies as a single file               
    if yyi == 1980:
        ano_ds = ano_tmp_ds
    else:
        ano_ds = xr.concat((ano_ds,ano_tmp_ds), dim="time")

    print(yyi)  # check year

# save output
ano_ds.to_netcdf('./trj_sm_pp.nc')
