###  verificando local de pasta
#pwd
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

from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
######## abrir arquivo nc
#ds = xr.open_dataset('ERA5_wave_200001.nc')
ds = xr.open_dataset('/media/ladsin/IGOR06/MESTRADO/PPGM/PROJETO_PETROBRAS/RENATA/GPM/prec_day2000_2019.nc')
		
#### selecionar um ponto/ou o mais proximo
UEL_VIGÁRIO_CANAL = ds.sel(lon=-43.87306,lat=-22.68278,method='nearest')
#### converter dataset em dataframe
UEL_VIGÁRIO_CANAL = UEL_VIGÁRIO_CANAL.to_dataframe()
########  ou mais direto
#pontoRJ = ds.sel(longitude=-44,latitude=-24,method='nearest').to_dataframe()
#### plotagem teste
UEL_VIGÁRIO_CANAL['precipitationCal'].plot()
##### salvando em planilha excel
UEL_VIGÁRIO_CANAL.to_csv('UEL_VIGÁRIO_CANAL_GPM.csv')
#####  abrir arquivos csv/txt
df = pd.read_csv('/media/ladsin/IGOR06/MESTRADO/PPGM/PROJETO_PETROBRAS/RENATA/UEL_VIGÁRIO_CANAL_GPM.csv')

###caso queira remover alguma coluna:
df = df.drop(columns=['bnds','time'])

df.to_csv('UEL_VIGÁRIO_CANAL_GPM.csv')

df.to_csv('UEL_VIGÁRIO_CANAL_GPM.txt')
