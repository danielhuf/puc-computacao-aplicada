# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 21:09:48 2020

@author: Daniel
"""
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

dfPib2018=pd.read_excel('dadosMundo.xlsx',decimal=',',sheet_name='PIB_2018',header=0,index_col=0)
dfPib2010=pd.read_excel('dadosMundo.xlsx',decimal=',',sheet_name='PIB_2010',header=0,index_col=0)
dfIdh=pd.read_excel('dadosMundo.xlsx',decimal=',',sheet_name='IDH',header=0,index_col=0)
dfCont=pd.read_excel('dadosMundo.xlsx',decimal=',',sheet_name='Cont',header=0,index_col=0)

print('\n---------------------------------------------------------------')
print('\n1.a) - Exibindo dfPib2018: \n')
print(dfPib2018)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n1.b) - Exibindo dfPib2010: \n')
print(dfPib2010)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n1.c) - Exibindo dfIdh: \n')
print(dfIdh)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n1.d) - Exibindo dfCont: \n')
print(dfCont)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n2.a) - Renomeando coluna "PIB" de df2018 e exibindo: \n')
dfPib2018.rename(columns={'PIB':'PIB2018'},inplace=True)
print(dfPib2018)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n2.b) - Renomeando coluna "PIB" de df2010 e exibindo: \n')
dfPib2010.rename(columns={'PIB':'PIB2010'},inplace=True)
print(dfPib2010)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n3) - Exibindo graficamente rela????o percentual entre os setores da economia brasileira: \n')
dfPib2018.loc['Brazil'][['Agricultura','Ind??stria','Manufatura','Servi??os']].plot.pie(autopct='%.1f',figsize=(5,5),title='Rela????o percentual entre os setores da economia brasileira')
plt.show()
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n4) - N??mero de pa??ses listados por continente: \n')
print(dfCont['Continente'].value_counts())
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n5) - Criando e exibindo dfPibIdh: \n')
dfPibIdh=pd.concat([dfPib2010['PIB2010'],dfPib2018[['PIB2018','C??digo']],dfIdh],axis=1)
dfPibIdh.index.name='Pa??s'
print(dfPibIdh)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n6) - Exibindo dfPibIdh com os c??digos errados substitu??dos devidamente: \n')
def detCod(pais):
    if pais['C??digo']!=pais['C??digo'].upper():
        return pais['Pa??s'][:3].upper()
    return pais['C??digo']
dfPibIdh.reset_index(inplace=True)
dfPibIdh['C??digo']=dfPibIdh.apply(detCod,axis=1)
dfPibIdh.set_index('Pa??s',inplace=True)
print(dfPibIdh)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n7) - Exibindo dfPibIdh com os valores ausentes do PIB de 2010 e de 2018 substitu??dos pelos valores m??nimos: \n')
dfPibIdh['PIB2018'].fillna(dfPibIdh['PIB2018'].min(),inplace=True)
dfPibIdh['PIB2010'].fillna(dfPibIdh['PIB2010'].min(),inplace=True)
print(dfPibIdh)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n8) - Resumo estat??stico do PIB de 2010: \n')
print(dfPib2010['PIB2010'].describe())
print('Pa??s de maior PIB de 2010:',dfPib2010['PIB2010'].idxmax())
print('Pa??s de menor PIB de 2010:',dfPib2010['PIB2010'].idxmin())
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n9) - N??mero de pa??ses com decrescimento do PIB de 2010 para 2018: \n')
f1=dfPibIdh.query('PIB2018<PIB2010')
print(f1.index.size)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n10) - Exibindo dfPibIdh com coluna de continentes e valores ausentes substitu??dos: \n')
dfPibIdh['Continente']=dfCont
gCont=dfPibIdh.groupby('Continente')
def preencheAusCont(g):
    medgrupo=g[['IDH','Expectativa de vida','Anos de estudo','PIB per capita']].mean()
    g.fillna(medgrupo,inplace=True)
    return g
dfPibIdh=gCont.apply(preencheAusCont)
print(dfPibIdh)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n11.a) - 10 pa??ses com maiores PIB??s per capita em ordem decrescente e respectivos valores: \n')
print(dfPibIdh['PIB per capita'].sort_values(ascending=False).head(10))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n11.b) - 10 pa??ses com menores PIB??s per capita em ordem crescente e respectivos valores: \n')
print(dfPibIdh['PIB per capita'].sort_values().head(10))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n12) - Exibindo o resumo estat??stico dos anos de estudo por continente: \n')
dfResEstCont=gCont.agg(['max','min','mean','median'])['Anos de estudo']
dfResEstCont.columns.name='Anos de estudo'
dfResEstCont.rename(columns={'max':'M??ximo','min':'M??nimo',
                             'mean':'M??dio','median':'Mediano'},
                    inplace=True)
print(dfResEstCont)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n13) - Exibindo os pa??ses cuja expectativa de vida possui, no m??ximo, 1 ano de diferen??a da m??dia: \n')
f2=abs(dfPibIdh['Expectativa de vida']-dfPibIdh['Expectativa de vida'].mean())<=1
print(list(dfPibIdh['Expectativa de vida'].loc[f2].index))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n14) - Exibindo a rela????o gr??fica (scatter) entre o PIB per capita e o IDH dos pa??ses de dfPibIdh: \n')
dfPibIdh.plot.scatter(x='IDH',y='PIB per capita',figsize=(10,4),title='Rela????o IDH x PIB per capita')
plt.show()
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n15) - Criando as categorias de IDH e exibindo dfPibIdh com os valores substitu??dos pelas categorias: \n')
cIdh=pd.cut(dfPibIdh['IDH'],bins=[0.350,0.555,0.700,0.800,1.00],labels=['baixo','medio','alto','muito alto'],include_lowest=True)
dfPibIdh['IDH']=cIdh
print(dfPibIdh)
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n16) - Criando e exibindo a tabela de frequ??ncia por IDH e mostrando no gr??fico de barras: \n')
tabFreqIdh=dfPibIdh['IDH'].value_counts()
print(tabFreqIdh)
tabFreqIdh.plot.bar(figsize=(7,5),title='N??mero de pa??ses por cada categoria de IDH: \n')
plt.show()
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n17) - Exibindo o c??digo dos pa??ses com o PIB de 2018 acima da m??dia e categoria de IDH que n??o seja a mais alta: \n')
f3=(dfPibIdh['PIB2018']>dfPibIdh['PIB2018'].mean()) & (dfPibIdh['IDH']!='muito alto')
print(list(dfPibIdh.loc[f3]['C??digo'].values))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n18) - Exibindo o PIB per capita m??ximo, m??nimo, m??dio, mediano e a soma por continente e por faixa de IDH: \n')
gContIdh=dfPibIdh.groupby(['Continente','IDH'])
print(gContIdh['PIB per capita'].agg(['max','min','mean','median','sum']))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n19.a) - Exibindo quantidades de pa??ses por faixa de IDH x continente: \n')
print(pd.crosstab(index=cIdh,columns=dfPibIdh['Continente']))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n19.b) - Exibindo quantidades de pa??ses por faixa de IDH x expectativa de vida acima (ou igual) e abaixo da m??dia: \n')
cExpec=pd.cut(dfPibIdh['Expectativa de vida'],bins=[0,dfPibIdh['Expectativa de vida'].mean(),dfPibIdh['Expectativa de vida'].max()],labels=['Abaixo da m??dia','Acima da m??dia'])
print(pd.crosstab(index=cIdh,columns=cExpec))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n19.c) - Exibindo quantidades de pa??ses por faixa de IDH x continente/expectativa de vida acima (ou igual) e abaixo da m??dia: \n')
print(pd.crosstab(index=cIdh,columns=[dfPibIdh['Continente'],cExpec]))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n20) - Exibindo maiores PIB??s de 2018 por faixa de IDH x continente: \n')
print(pd.crosstab(index=cIdh,columns=dfPibIdh['Continente'],values=dfPibIdh['PIB2018'],aggfunc='max'))
print('\n---------------------------------------------------------------')

print('\n---------------------------------------------------------------')
print('\n21) - Exibindo continentes mais comuns por faixa de IDH: \n')
def maisFreqPorGrupo(faixa):
    f=faixa.value_counts()
    m=f.max()
    sMaisFreq=f.loc[f==m]
    return list(sMaisFreq.index)
gIdh=dfPibIdh.groupby('IDH')
print(gIdh['Continente'].apply(maisFreqPorGrupo))
print('\n---------------------------------------------------------------')
