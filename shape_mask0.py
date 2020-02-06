"""
https://stackoverflow.com/questions/51398563/python-mask-netcdf-data-using-shapefile
https://gist.github.com/shoyer/0eb96fa8ab683ef078eb
https://github.com/pydata/xarray/issues/501

Created on Thu Nov 21 20:40:13 2019
@author: igor06
"""
import pandas as pd
import numpy as np
import xarray as xr
import geopandas as gpd


from rasterio import features
from affine import Affine

ds = xr.open_dataset('/home/igor06/MESTRADO/PPGM/PROJETO_PETROBRAS/RENATA/GPM/prec_day_2000_2019.nc')
ds['precipitationCal'].mean(dim="time").plot()
awash = gpd.read_file('/home/igor06/MESTRADO/PPGM/PROJETO_PETROBRAS/CURSO_PYTHON_RONALDO/shapefiles/rj_unidades_da_federacao/33UFE250GC_SIR.shp')
awash.plot()
ax = awash.plot(alpha=0.2, color='black')
ds['precipitationCal'].mean(dim="time").plot(ax=ax,zorder=-1)

def transform_from_latlon(lat, lon):
    """ input 1D array of lat / lon and output an Affine transformation
    """
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    trans = Affine.translation(lon[0], lat[0])
    scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
    return trans * scale

def rasterize(shapes, coords, latitude='latitude', longitude='longitude',
              fill=np.nan, **kwargs):
    transform = transform_from_latlon(coords[latitude], coords[longitude])
    out_shape = (len(coords[latitude]), len(coords[longitude]))
    raster = features.rasterize(shapes, out_shape=out_shape,
                                fill=fill, transform=transform,
                                dtype=float, **kwargs)
    spatial_coords = {latitude: coords[latitude], longitude: coords[longitude]}
    return xr.DataArray(raster, coords=spatial_coords, dims=(latitude, longitude))

def add_shape_coord_from_data_array(xr_da, shp_path, coord_name):
    shp_gpd = gpd.read_file('/home/igor06/MESTRADO/PPGM/PROJETO_PETROBRAS/CURSO_PYTHON_RONALDO/shapefiles/rj_unidades_da_federacao/33UFE250GC_SIR.shp')
    shapes = [(shape,n) for n, shape in enumerate(shp_gpd.geometry)]
    xr_da[coord_name] = rasterize(shapes, xr_da.coords, 
                               longitude='lon', latitude='lat')
    return xr_da

ds['precipitationCal'] = add_shape_coord_from_data_array(ds['precipitationCal'], awash, "awash")
awash_da = ds['precipitationCal'].where(ds['precipitationCal'].awash==0, other=np.nan)
awash_da.mean(dim="time").plot()