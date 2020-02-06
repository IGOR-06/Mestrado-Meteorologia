#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:06:28 2020

@author: igor06
"""
#### importando datetime
import datetime
######  importando xarray
import xarray as xr
######  importando xarray
import pandas as pd
######  importando matplotlib
import matplotlib.pyplot as plt
######  importando numpy
import numpy as np
######  importando cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
###### importando leitor para shape
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

###### importando plotar imagem de satelite
from matplotlib.transforms import offset_copy
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

######  importando geopandas
import geopandas as gpd
######  importando geoplot
import geoplot as gplt
import geoplot.crs as gcrs

from rasterio import features
from affine import Affine
import mapclassify as mc

correlacao=pd.read_csv('/media/ladsin/IGOR06/MESTRADO/PPGM/PROJETO_PETROBRAS/RENATA/correlacoes.csv',
               sep='\t',skiprows=1,header=None,names=['nome','correlações','geometry','lon','lat'])


############## Plotagem de mapa ##########################

# Create a Stamen terrain background instance.
stamen_terrain = cimgt.Stamen('terrain-background')
####### plotagem de figura em branco
fig,ax = plt.subplots(figsize=(15, 10))
###### plotagem de mapa em branco
ax = plt.axes(projection=ccrs.PlateCarree())


##### cortando para area desejada e colocando graus em x e y
ax.set_extent([-44.35,-43.15,-23.05,-22.55],crs=ccrs.PlateCarree()) 
lon_formatter = LongitudeFormatter(number_format='.01f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
lat_formatter = LatitudeFormatter(number_format='.01f',
                                  degree_symbol='')
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

####### Gradeando o mapa
gl=ax.gridlines(crs=ccrs.PlateCarree(),
             draw_labels=True,
             linestyle='--',
             linewidth=1,
             color='gray',
             alpha=0.5)
gl.xlabels_top=False
gl.ylabels_right=False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER


# Add the Stamen data at zoom level 10.
ax.add_image(stamen_terrain, 10)
#######  plotagem shape do rio de janeiro
mapa_amsul = ShapelyFeature(Reader('/media/ladsin/IGOR06/MESTRADO/PPGM/PROJETO_PETROBRAS/CURSO_PYTHON_RONALDO/shapefiles/rj_unidades_da_federacao/33UFE250GC_SIR.shp').geometries(),
                            ccrs.PlateCarree(),
                            edgecolor='black',
                            facecolor='None')
ax.add_feature(mapa_amsul)

#######  plotagem shape dos dutos do rio de janeiro 
mapa_duto = ShapelyFeature(Reader('/media/ladsin/IGOR06/MESTRADO/PPGM/PROJETO_PETROBRAS/CURSO_PYTHON_RONALDO/shapefiles/RJ25_tra_trecho_duto_l/RJ25_tra_trecho_duto_l.shp').geometries(),
                            ccrs.PlateCarree(),
                            edgecolor='red',
                            facecolor='None')
ax.add_feature(mapa_duto)

#######  plotagem shape dos municipios do rio de janeiro
mapa_limites = ShapelyFeature(Reader('/media/ladsin/IGOR06/MESTRADO/PPGM/PROJETO_PETROBRAS/CURSO_PYTHON_RONALDO/shapefiles/T_LM_MUNICIPIOS_2010/T_LM_MUNICIPIOS_2010Polygon.shp').geometries(),
                            ccrs.PlateCarree(),
                            edgecolor='black',
                            facecolor='None')
ax.add_feature(mapa_limites)

##########  plotagem de legenda x e y
#ax.set_ylabel('Latitude')
#ax.set_xlabel('Longitude')

ax.text(-0.07, 0.5, 'Latitude', va='bottom', ha='center', rotation='vertical',
        rotation_mode='anchor',transform=ax.transAxes)
ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',rotation='horizontal',
        rotation_mode='anchor', transform=ax.transAxes)

# Add a marker for the REDUC.
ax.plot(-43.25, -22.71, marker='o', color='red', markersize=10,
        alpha=1.7, transform=ccrs.Geodetic())
    
# Add a marker for the ANGRA.
ax.plot(-44.24, -23.00, marker='o', color='red', markersize=10,
        alpha=1.7, transform=ccrs.Geodetic())

# Use the cartopy interface to create a matplotlib transform object
# translates the text by 25 pixels to the left.
geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
text_transform = offset_copy(geodetic_transform, units='dots', x=-25)

# Add text 25 pixels to the left of the ORBIG.
ax.text(-44.17, -23.03, u'ORBIG',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

plt.plot([-44.24,-44.11],[-23.00, -23.00], color='red', 
         linestyle='-',
         transform=ccrs.PlateCarree(),)
###########################################################################
ax.text(-44.303, -22.9456, u'Angra dos Reis',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-43.867, -22.8744, u'Coroa Grande',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-44.091,	-22.7422, u'Fontes Novas',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-44.030,	-22.9313, u'Ibicuí',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-43.88, -22.73, u'Lajes Barramento',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-43.80, -22.66, u'Pereira Passos',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-44.193, -22.8055, u'Rio Claro',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-43.683, -22.7366, u'Seropédica',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-43.873,	-22.6527, u'Vigários',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))

ax.text(-43.411,	-22.8313, u'Vila Militar',
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform,
        bbox=dict(facecolor='white', alpha=1.5, boxstyle='round'))
        
###################  Plotagem correlação  #######################

ax.scatter(correlacao['lon'],correlacao['lat'],c=correlacao['correlações'],alpha=1,s=90,
           cmap='summer_r',label=correlacao['nome'])

scatter = ax.scatter(correlacao['lon'],correlacao['lat'],s=90,
                     c=correlacao['correlações'],cmap='summer_r')

ax.legend(*scatter.legend_elements(), loc='upper right',)
