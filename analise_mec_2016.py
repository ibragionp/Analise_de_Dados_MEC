import pandas as pd
import seaborn as sns
import folium
from folium import plugins
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
import os

PROUNI_FILE = 'pda-prouni-2016.csv'
MUNICIPIOS_FILE = 'MunicipiosBrasil.csv'

ENCODING = 'ISO-8859-1'

SEP = ';'

MUN_MUNICIPIO_COL = 'MUNICIPIO'
MUN_UF_COL = 'UF'
MUN_LATITUDE_COL = 'LATITUDE'
MUN_LONGITUDE_COL = 'LONGITUDE'

PRO_MUNICIPIO_BENEFICIARIO_BOLSA_COL = 'MUNICIPIO_BENEFICIARIO_BOLSA'

QUANTIDADE_OCORRENCIAS_CIDADE_COL = 'QUANTIDADE_OCORRENCIAS_CIDADE'

LATITUDE_PAIS = -15.788497
LONGITUDE_PAIS = -47.879873

FILE_PATH = os.getcwd() + "\\"

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

prouni_2016 = pd.read_csv(FILE_PATH + PROUNI_FILE, 
                          sep = SEP, 
                          encoding = ENCODING)

municipios_brasil = pd.read_csv(FILE_PATH + MUNICIPIOS_FILE, 
                                usecols = [MUN_MUNICIPIO_COL, 
                                           MUN_UF_COL, 
                                           MUN_LATITUDE_COL, 
                                           MUN_LONGITUDE_COL], 
                                sep = SEP, 
                                encoding = ENCODING)

prouni_2016 = prouni_2016.fillna('')

municipios_brasil = municipios_brasil.fillna('')

municipios_brasil[MUN_LATITUDE_COL] = municipios_brasil[MUN_LATITUDE_COL].apply(lambda x: (x.replace(',','.'))
    .strip())

municipios_brasil[MUN_LATITUDE_COL] = municipios_brasil[MUN_LATITUDE_COL].astype(float)

municipios_brasil[MUN_LONGITUDE_COL] = municipios_brasil[MUN_LONGITUDE_COL].apply(lambda x: (x.replace(',','.')).strip())

municipios_brasil[MUN_LONGITUDE_COL] = municipios_brasil[MUN_LONGITUDE_COL].astype(float)

prouni_2016[PRO_MUNICIPIO_BENEFICIARIO_BOLSA_COL] = prouni_2016[
    PRO_MUNICIPIO_BENEFICIARIO_BOLSA_COL
].apply(lambda x: remover_acentos(x))

df_gerar_mapa = pd.merge(prouni_2016.drop_duplicates(), 
    municipios_brasil.drop_duplicates(), 
    left_on = ['MUNICIPIO_BENEFICIARIO_BOLSA', 'SIGLA_UF_BENEFICIARIO_BOLSA'], 
    right_on = [MUN_MUNICIPIO_COL, MUN_UF_COL], 
    how = 'left')

df_gerar_mapa = df_gerar_mapa[(~df_gerar_mapa[MUN_LATITUDE_COL].isnull()) 
    | (~df_gerar_mapa[MUN_LONGITUDE_COL].isnull())]

df_municipio_bolsa = df_gerar_mapa.assign(QUANTIDADE_OCORRENCIAS_CIDADE = 
    df_gerar_mapa.groupby(PRO_MUNICIPIO_BENEFICIARIO_BOLSA_COL)
    .MUNICIPIO_BENEFICIARIO_BOLSA.transform('count'))

df_municipio_bolsa = df_municipio_bolsa.sort_values(
    [QUANTIDADE_OCORRENCIAS_CIDADE_COL, 
    PRO_MUNICIPIO_BENEFICIARIO_BOLSA_COL], 
    ascending = [True, False])

coordenadas = []
lat = df_municipio_bolsa[MUN_LATITUDE_COL][:500].values
long = df_municipio_bolsa[MUN_LONGITUDE_COL][:500].values

mapa = folium.Map(
    location = [LATITUDE_PAIS, LONGITUDE_PAIS], 
    tiles = 'Stamen Toner', 
    zoom_start = 4)

for la, lo in zip(lat, long):
    coordenadas.append([la, lo])

mapa.add_child(plugins.HeatMap(coordenadas))

mapa