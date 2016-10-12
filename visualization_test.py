# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:40:30 2016

@author: utpl
"""

import numpy as np
import matplotlib as p
import pdb
import pandas as pd
import matplotlib.pyplot as plt



data = pd.read_csv('/Users/utpl/Documents/bigdata/Datosperiodosacademicos.csv', encoding = "ISO-8859-1", na_values=['ND'])

data = data.dropna()

## FILTRANDO POR PERIODO ACADEMICO

data_abag2014 = data[data.PERIODO == 'Abr/2014 - Ago/2014']

duniqueabag2014 = data_abag2014.drop_duplicates('IDENTIFICACION')

data_abag2015 = data[data.PERIODO == 'Abr/2015 - Ago/2015']

duniqueabag2015 = data_abag2015.drop_duplicates('IDENTIFICACION')

data_oct14_feb15 = data[data.PERIODO == 'Oct/2014 - Feb/2015']

dunique_oct14_feb15 = data_oct14_feb15.drop_duplicates('IDENTIFICACION')

data_oct15_feb16 = data[data.PERIODO == 'Oct/2015 - Feb/2016']

dunique_oct15_feb16 = data_oct15_feb16.drop_duplicates('IDENTIFICACION')

#### TABLETS COUNT

tabletsCount_abag2014 = pd.crosstab(duniqueabag2014.PERIODO, duniqueabag2014.TABLET)

tabletsCount_abag2015 = pd.crosstab(duniqueabag2015.PERIODO, duniqueabag2015.TABLET)

tabletsCount_oct14_feb15 = pd.crosstab(dunique_oct14_feb15.PERIODO, dunique_oct14_feb15.TABLET)

tabletsCount_oct15_feb16 = pd.crosstab(dunique_oct15_feb16.PERIODO, dunique_oct15_feb16.TABLET)

frames = [tabletsCount_abag2014, tabletsCount_abag2015, tabletsCount_oct14_feb15, tabletsCount_oct15_feb16]

result = pd.concat(frames)

## GRAFICAMOS EL RESULTDAO POR PERIODO 

result.plot(kind='bar', stacked=True, title="Resúmen de los Períodos Académicos").legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

### FILTRAMOS POR CENTRO

### PEERIODO ABRIL AGOSTO 2015

tabletsCount_duniqueabag2015 = pd.crosstab(duniqueabag2015.CENTRO, duniqueabag2015.TABLET)

tabletsCount_duniqueabag2015.plot(kind='barh', stacked=True, title="Período Abril - Agosto 2015").legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

### PEERIODO octubre 2015 febrero 2016

tabletsCount_dunique_oct15_feb16 = pd.crosstab(dunique_oct15_feb16.CENTRO, dunique_oct15_feb16.TABLET)

tabletsCount_dunique_oct15_feb16.plot(kind='barh', stacked=True, title="Período Octubre 2015 - Febrero 2016").legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

## LATITUD Y LONGITUD DE CENTROS

centros = pd.read_csv('/Users/utpl/Documents/bigdata/centros_latlon.csv', encoding = "ISO-8859-1", na_values=['ND'])

centros['name'] = centros['name'].str.upper()
centros['name'] = centros['name'].str.strip()

centros.columns = ['CAMPUS', 'CENTRO', 'provincia', 'localidadDBpedia', 'lat', 'long']

## CENTROS Y DATOS PERIDO ABRIL AGOSTO 2015

#### transformamos el indice a columna 

tabletsCount_duniqueabag2015['CENTRO'] = tabletsCount_duniqueabag2015.index

centros_aa2015 = pd.merge(tabletsCount_duniqueabag2015, centros)

#### exportamos los datos para poder graficar
aux = centros_aa2015

aux['RESUMEN'] = centros_aa2015.apply(lambda x: '<a href="' + (x['CAMPUS']) + '"> CAMPUS ' + x['CENTRO'] +'</a>, <a href="'+x['localidadDBpedia']+'>'+x['CENTRO']+'</a><br/> ' + '<b>Tabletas entregadas: ' + str(x['SI']) + '</b><br/> <b>Tabletas no entregadas: ' + str(x['NO'])+ '</b>', 1)

aux = aux.drop('CENTRO', 1)
aux = aux.drop('provincia', 1)
aux = aux.drop('localidadDBpedia', 1)
aux = aux.drop('SI', 1)
aux = aux.drop('NO', 1)
aux = aux.drop('CAMPUS', 1)
aux['icon'] = 'logo.png'

## ordenar las columnas para graficar
aux = aux.reindex_axis(['lat','long','icon','RESUMEN'], axis=1)
aux.columns = ['lat', 'lng', 'icon', 'RESUMEN']
##exportar
aux = aux.reindex_axis(['CENTRO','CAMPUS','provincia','localidadDBpedia', 'lat', 'long','RESUMEN'], axis=1)
aux.to_csv('/Users/utpl/Documents/bigdata/centros_aa2015.csv', sep=';', encoding='utf-8')

## CENTROS Y DATOS PERIDO octubre 2015 febrero 2016

tabletsCount_dunique_oct15_feb16['CENTRO'] = tabletsCount_dunique_oct15_feb16.index

centros_oct15_feb16 = pd.merge(tabletsCount_dunique_oct15_feb16, centros)

#### exportamos los datos para poder graficar
aux2 = centros_oct15_feb16
aux2 = aux2.reindex_axis(['CENTRO','CAMPUS','provincia','localidadDBpedia', 'lat', 'long','RESUMEN'], axis=1)

aux2.to_csv('/Users/utpl/Documents/bigdata/centros_oct15_feb16.csv', sep=';', encoding='utf-8')




