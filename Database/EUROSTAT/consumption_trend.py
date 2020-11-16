# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:18:07 2020

@author: nigolred
"""
import pandas as pd

years = list(range(2010,2031))
past_years = list(range(2010,2017))
future_years = list(range(2017,2031))
year_map = {2010: '',
          2011: '2',
          2012: '3',
          2013: '4',
          2014: '5',
          2015: '6',
          2016: '7'}
#%%

products = list(pd.read_excel('ITA_Use_basic.xls', skiprows=10, header=[1], index_col=[0]).iloc[0:65].index)
cathegories = ['Total final use']

Trend = pd.DataFrame(index=products, columns=pd.MultiIndex.from_product([years, cathegories]))

for y in past_years:
    Y = pd.read_excel('ITA_Use_basic.xls', sheet_name='Data'+year_map[y], skiprows=10, header=[1], index_col=[0]).iloc[0:65].loc[:,cathegories]
    for p in products:
        for c in cathegories:
            Trend.loc[p,(y,c)] = Y.loc[p,c]

Trend = Trend.stack()

#%% Projecting final demand by product

from scipy import interpolate

for p in products:
    for c in cathegories:
        f = interpolate.interp1d(list(range(1,len(past_years)+1)), Trend.loc[p,c].iloc[0:len(past_years)], fill_value="extrapolate")
        for y in future_years:
            Trend.loc[(p,c),y] = f(y-2010)

Trend[Trend < 0] = 0
Trend_pref = Trend
Trend_pref = Trend / Trend.sum(axis=0)           
#%%
TrendY = Trend.loc[(slice(None),'Total final use'),:].stack()

