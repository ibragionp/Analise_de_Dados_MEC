# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:53:44 2019

@author: isabe
"""

import pandas as pd

diretorio_arquivo = 'C:\\Users\\isabe\\Desktop\\Working On Estrutura de Dados\\MEC\\'

def abre_arquivo(diretorio_arquivo, nome_arquivo):
    df = pd.read_csv(diretorio_arquivo + nome_arquivo, sep=';', encoding='ISO-8859-1')
    df = df.fillna('')
    return df

prouni_2014 = abre_arquivo(diretorio_arquivo, 'pda-prouni-2014.csv')
prouni_2015 = abre_arquivo(diretorio_arquivo, 'pda-prouni-2015.csv')
prouni_2016 = abre_arquivo(diretorio_arquivo, 'pda-prouni-2016.csv')

print((prouni_2014.shape)[0])

nomes_cursos = prouni_2016['NOME_CURSO_BOLSA'].str.upper().str.strip()
nomes_cursos = nomes_cursos.tolist()
nomes_cursos = (list(set(nomes_cursos)))[1:]

dicionario = {}
for i in range(len(nomes_cursos)):
    df = prouni_2016[prouni_2016['NOME_CURSO_BOLSA'].str.upper() == nomes_cursos[i]]
    print((df.shape))
    dicionario[nomes_cursos[i]] = (df.shape)[0]
