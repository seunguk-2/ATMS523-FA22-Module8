import numpy as np
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs

# Converting grid from xy-km to degree (Lambert Conformal)
def invlambxy(xx, yy):
    phi1 = 10 * np.pi / 180.
    phi2 = 65 * np.pi / 180.
    lon0 = -105 * np.pi / 180.
    lat0 = 10 * np.pi / 180.
    R = 6.371e6
    
    n = np.log(np.cos(phi1)/np.cos(phi2))/np.log(np.tan(np.pi/4+phi2/2)/np.tan(np.pi/4+phi1/2))
    F = np.cos(phi1)*(np.tan(np.pi/4+phi1/2)**n) / n
    rho0 = R * F / (np.tan(np.pi/4 + lat0/2))**n
    
    # inlon
    inlon = lon0 + np.arctan(-xx/(yy-rho0))/n
    
    # inlat
    rho = np.sqrt(xx**2 + (yy-rho0)**2)
    inlat = 2*(np.arctan((R*F/rho)**(1/n)) - np.pi/4)
    
    inlon = inlon * 180 / np.pi
    inlat = inlat * 180 / np.pi
    
    return inlon, inlat

# For drawing a box on a map
def draw_subr(axes,arr,color):
    """ arr = [west east south north]"""
    axes.plot([arr[0], arr[1]],[arr[2], arr[2]],"--"+color,transform=ccrs.PlateCarree())
    axes.plot([arr[0], arr[1]],[arr[3], arr[3]],"--"+color,transform=ccrs.PlateCarree())
    axes.plot([arr[0], arr[0]],[arr[2], arr[3]],"--"+color,transform=ccrs.PlateCarree())
    axes.plot([arr[1], arr[1]],[arr[2], arr[3]],"--"+color,transform=ccrs.PlateCarree())

# get soil moisture anomaly along the trajectory
def nSMvvc(xx, yy, dayn, yyi, sm, smc):
    lx = np.round(xx/0.25)*0.25
    ly = np.round(yy/0.25)*0.25
    mnxi = (lx-(-170))/0.25
    mnyi = (65-ly)/0.25    
    ynan = np.isnan(mnxi)| (mnxi >= 441) | (mnyi >= 221)
    mnxi[ynan] = 0
    mnyi[ynan] = 0
    mnxi = mnxi.astype('int')
    mnyi = mnyi.astype('int')
    smv = sm.sel(time=slice(str(yyi-1)+'-11-01',str(yyi)+'-10-31'))
    smv = smv.sm_surf.values[dayn,mnyi,mnxi]
    smv = smv - smc.sm_surf.values[dayn-61,mnyi,mnxi]
    smv[ynan] = np.nan
    return smv.squeeze()

# get evapotranspiration anomaly along the trajectory
def nETvvc(xx, yy, dayn, yyi, sm, smc):
    lx = np.round(xx/0.25)*0.25
    ly = np.round(yy/0.25)*0.25
    mnxi = (lx-(-170))/0.25
    mnyi = (65-ly)/0.25    
    ynan = np.isnan(mnxi)| (mnxi >= 521) | (mnyi >= 221)
    mnxi[ynan] = 0
    mnyi[ynan] = 0
    mnxi = mnxi.astype('int')
    mnyi = mnyi.astype('int')
    smv = sm.sel(time=slice(str(yyi-1)+'-11-01',str(yyi)+'-10-31'))
    smv = smv.e.values[dayn,mnyi,mnxi]
    smv = smv - smc.e.values[dayn-61,mnyi,mnxi]
    smv[ynan] = np.nan
    return smv.squeeze()

# Midwest average
def getmwavg2(ds):
    dsmw = ds.sel(longitude=slice(-96.75,-87), latitude=slice(45.75,36))
    dsmw = dsmw.mean(dim=('latitude','longitude'))
    return dsmw