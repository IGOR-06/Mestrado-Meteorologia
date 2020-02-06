
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

######## abrir arquivo nc
ds = xr.open_dataset('/media/ladsin/IGOR06/MESTRADO/PPGM/PROJETO_PETROBRAS/RENATA/GPM/prec1_day2000_2019.nc')

##### definindo campo com duas dimensões escolhendo um index
#i=4975
i=0
#campo2D = ds.isel(time=i)
campo2D = ds.sel(time= '2001-03-29 11:45:00')

# Modificando usando xr.where() na região
mask = (ds.coords['lat']>=-23.05)&(ds.coords['lat']<=-23.00)&(ds.coords['lon']>=-44.05)&(ds.coords['lon']<=-43.70)
#mask = (ds.coords['lat']!=-23.05)&(ds.coords['lon']!=-44.05))
campo2D['precipitationCal'] = xr.where(mask, 0, campo2D['precipitationCal'])

####### plotagem teste
#plt.contourf(campo2D['precipitationCal'])
    
#### definindo lat lon em grade pelo numpy
lons,lats = np.meshgrid(ds.lon,ds.lat)
#### fazendo matrizes tranversa pq vinha errado
#lons=lons.T
#lats=lats.T

# Create a Stamen terrain background instance.
stamen_terrain = cimgt.Stamen('terrain')
####### plotagem de figura em branco
fig,ax = plt.subplots(figsize=(17, 12))
###### plotagem de mapa em branco
ax = plt.axes(projection=ccrs.PlateCarree())

#maximos e minimos de lon e lat, respectivamente)
#a=ds['lat'].values
#ax.set_xticks(a, crs=ccrs.PlateCarree()) #variacao da lon
#ax.set_xticks([-44.45, -44.35, -44.25, -44.15, -44.05, -43.95, -43.85, -43.75,
#-43.65, -43.55, -43.45, -43.35, -43.25, -43.15,-23.25, -23.15, -23.05,-22.95,
# -22.85, -22.75, -22.65, -22.55], crs=ccrs.PlateCarree()) #variacao da lon

#b=ds['lon'].values
#ax.set_yticks(b, crs=ccrs.PlateCarree()) #variacao da lat
#ax.set_yticks([-44.45, -44.35, -44.25, -44.15, -44.05, -43.95, -43.85, -43.75,
#-43.65, -43.55, -43.45, -43.35, -43.25, -43.15,-23.25,-23.15, -23.05,-22.95,
#-22.85, -22.75, -22.65, -22.55], crs=ccrs.PlateCarree()) #variacao da lat

##### cortando para area desejada e colocando graus em x e y
ax.set_extent([-44.35,-43.15,-23.05,-22.55],crs=ccrs.PlateCarree()) 
lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)

lat_formatter = LatitudeFormatter(number_format='.1f',
                                  degree_symbol='')

ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

# Add the Stamen data at zoom level 10.
ax.add_image(stamen_terrain, 10)
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
#cf = plt.contourf(lons,lats,campo2D['swh'],cmap='RdBu_r',levels=[1,2,3,4])
#np.arange(0,14,1)
#np.linspace(0,14,15)

######## plotagem de chuva e sua escala de cor

cf = plt.contourf(lons,lats,campo2D['precipitationCal'],cmap='GnBu',
                  levels=np.arange(20,420,20))

####### plotagem de linha com cor preta
cs = plt.contour(lons,lats,campo2D['precipitationCal'],colors='black',
                 levels=np.arange(20,420,40))

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
ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')

########## de linha de contorno
ax.clabel(cs, inline=1,fontsize=10)

#ax.set_title('Prec -GPM {}'.format(pd.to_datetime(ds.time[i].values)))
ax.set_title('Prec -GPM 2001-03-29 11:45:00')
cbar = plt.colorbar(cf, orientation='horizontal', pad=0.05, aspect=50) #colocando o cbar 
cbar.set_label('mm/dia') #titulo do colorbar

#plt.savefig('Prec -GPM 2001-03-29.png', dpi=100)