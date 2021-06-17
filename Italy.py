# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:01:10 2020

@author: nigolred
"""

import REP_CVX as cvx
import pandas as pd

# Choosing the mode
Case = 'PT'

Cases = {'PT': {'y': 'y_pt', 'code': 'ProjectedTrends', 'title': 'with projected demand trends', 'GDP':'GDP'},
         'NC': {'y': 'y_fx', 'code': 'NoPrefChange', 'title': 'with no change in preferences', 'GDP':'GDP'}
         }

# Importing data
Ita14 = cvx.C_SUT(r'Database\Italy_2014_SUT.xlsx', unit='M EUR')
Ita15 = cvx.C_SUT(r'Database\Italy_2015_SUT.xlsx', unit='M EUR')
Italy = cvx.C_SUT(r'Database\Italy_2016_SUT.xlsx', unit='M EUR')

Preferences = pd.read_excel('Inputs/Inputs.xlsx', sheet_name=Cases[Case]['y'], header=[0,1], index_col=[0])
ExpectedGDP = pd.read_excel('Inputs/Inputs.xlsx', sheet_name=Cases[Case]['GDP'], header=[0], index_col=[0])

#%% Comparing intermediate and final consumption
IntFin = pd.DataFrame()
IntFin['Intermediate Cons'] = Italy.U.sum(axis=1).groupby(level=1, sort=False).sum()
IntFin['Final Cons'] = Italy.Y.loc['Commodities'].groupby(level=1).sum()

IntFin_p = pd.DataFrame(0, index=IntFin.index, columns=IntFin.columns)
for i in range(len(IntFin_p.index)):
    IntFin_p.iloc[i,0] = IntFin.iloc[i,0] / (IntFin.iloc[i,0] + IntFin.iloc[i,1])
    IntFin_p.iloc[i,1] = IntFin.iloc[i,1] / (IntFin.iloc[i,0] + IntFin.iloc[i,1])

#%% Exploring aggregated preferences
Pref = pd.DataFrame(Preferences.values, index=Italy.Z.index, columns=Preferences.columns).loc['Commodities'].groupby(level=1, sort=False).sum().loc[:,'Baseline']
    
#%% Leontief-Kantorovich model
    
# Preparing results 
years = list(range(2014,2014+len(ExpectedGDP.columns)))
scenarios = ['Best','Medium','Worst','Baseline']
GDP_by_sec = pd.DataFrame(index=Italy.X_agg.loc['Activities'].index, columns=Preferences.columns)
GDPw_by_sec = pd.DataFrame(index=Italy.X_agg.loc['Activities'].index, columns=Preferences.columns)

# Runnig the Leontief Kantorovic model for every scenario-year

for s in scenarios:
        for y in years:
            print('\nIn the {} scenario for {}:'.format(s,y))
            if y == 2014:
                cvx.LK_model(Ita14, Preferences.loc[:,(s,y)].to_frame(), ExpectedGDP.loc[s,y])
                GDP_by_sec.loc[:,(s,y)] = Ita14.VA.groupby(level=1, sort=False).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum()
                GDPw_by_sec.loc[:,(s,y)] = Ita14.VA.groupby(level=1, sort=False).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum() / Italy.VA.groupby(level=1).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum().sum()
            if y == 2015:
                cvx.LK_model(Ita15, Preferences.loc[:,(s,y)].to_frame(), ExpectedGDP.loc[s,y])
                GDP_by_sec.loc[:,(s,y)] = Ita15.VA.groupby(level=1, sort=False).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum()
                GDPw_by_sec.loc[:,(s,y)] = Ita15.VA.groupby(level=1, sort=False).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum() / Italy.VA.groupby(level=1).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum().sum()
            else:
                cvx.LK_model(Italy, Preferences.loc[:,(s,y)].to_frame(), ExpectedGDP.loc[s,y])
                GDP_by_sec.loc[:,(s,y)] = Italy.VA.groupby(level=1, sort=False).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum()
                GDPw_by_sec.loc[:,(s,y)] = Italy.VA.groupby(level=1, sort=False).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum() / Italy.VA.groupby(level=1).sum().loc['GDP'].loc['Activities'].groupby(level=1, sort=False).sum().sum()

#%% Exploring results
ref_year = 2030
At_refyear = GDP_by_sec.loc[:,(slice(None),ref_year)]
for i in list(GDP_by_sec.index):
    for j in scenarios:
        At_refyear.loc[i,(j,ref_year)] =  (GDP_by_sec.loc[i,(j,ref_year)] - GDP_by_sec.loc[i,('Baseline',2016)]) / GDP_by_sec.loc[i,('Baseline',2016)] *100


#%% Exporting results

with pd.ExcelWriter('Results/'+Cases[Case]['code']+'.xlsx') as writer:
    GDP_by_sec.unstack().unstack(level=1).T.to_excel(writer, sheet_name='GDP by sector')
    GDPw_by_sec.unstack().unstack(level=1).T.to_excel(writer, sheet_name='Share of GDP by sector')

cvx.LK_plot(GDP_by_sec, file_title='Results/'+Cases[Case]['code']+'_NetGDP', fig_title='Net Italian GDP by sector from 2016 to 2030 in different scenarios with resepect to 2016 baseline '+Cases[Case]['title']+' [M€]', mode='net')
cvx.LK_plot(GDP_by_sec, file_title='Results/'+Cases[Case]['code']+'_NetPercGDP', fig_title='Net Italian percentual GDP change by sector from 2016 to 2030 in different scenarios with resepect to 2016 baseline '+Cases[Case]['title']+' [%]', mode='net_perc')
cvx.LK_plot(GDP_by_sec, file_title='Results/'+Cases[Case]['code']+'_GDP', fig_title='Italian GDP by sector from 2016 to 2030 in different scenarios '+Cases[Case]['title']+' [M€]', mode='abs')
cvx.LK_plot(GDP_by_sec, file_title='Results/'+Cases[Case]['code']+'_NetGDP'+'_paper', fig_title='Net Italian GDP by sector from 2020 to 2030 in different scenarios with resepect to 2016 baseline '+Cases[Case]['title']+' [M€]', mode='paper', shared_yaxes=True, paper=True)

#%% Paper values in section 3.2. Run only if you are using Paper Aggregation

# Measuring best performing sectors in Baseline case
Pos = ['Food, beverages & tobacco','Utilities','Machinery','Transport equipment']
Pos_increase = GDP_by_sec.loc[Pos,('Baseline',2030)].sum()-GDP_by_sec.loc[Pos,('Baseline',2016)].sum()
Pos_increase_GDP2016 = Pos_increase/GDP_by_sec.loc[:,('Baseline',2016)].sum().sum()*100

# Measuring best and worst performing sectors in Medium and Worst case
VeryPos = ['Utilities','Transport equipment']
VeryNeg = ['Textile & leather','Chemicals','Construction']
VeryPos_increase =  pd.DataFrame(index=['Medium','Worst'], columns=['abs','perc'])
VeryNeg_decrease =  pd.DataFrame(index=['Medium','Worst'], columns=['perc'])

for i in ['Medium','Worst']:
    VeryPos_increase.loc[i,'abs'] =  GDP_by_sec.loc[VeryPos,(i,2030)].sum()-GDP_by_sec.loc[VeryPos,(i,2016)].sum()
    VeryPos_increase.loc[i,'perc'] =  (GDP_by_sec.loc[VeryPos,(i,2030)].sum()-GDP_by_sec.loc[VeryPos,(i,2016)].sum())/GDP_by_sec.loc[:,('Baseline',2016)].sum()*100
    VeryNeg_decrease.loc[i,'perc'] =  (GDP_by_sec.loc[VeryNeg,(i,2030)].sum()-GDP_by_sec.loc[VeryNeg,(i,2016)].sum())/GDP_by_sec.loc[VeryNeg,('Baseline',2016)].sum().sum()*100


