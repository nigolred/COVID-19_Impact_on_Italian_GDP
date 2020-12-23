# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 18:05:38 2020

@author: nigolred
"""
def LK_model(SUT,y,GDP):
    import pandas as pd
    import cvxpy as cv
    import numpy as np
    import pymrio
    
    # optimization model
    # variables definition
    nPI = len(SUT.Z) # number of products-industries
    YY = cv.Variable((1,1),nonneg=True)         # total final demand
    SUT.X = cv.Variable((nPI,1),nonneg=True)    # total production
    
    # objective function definition
    # maximization of the overall final consumptions + investment + exports (scalar)
    obj = cv.Minimize(-YY)

    # constraints definition
    #1 final demand is satisfied according to a given basket of final consumption preferences 
    #2 consumption of economic exogenous factors (labor) cannot exceed endowments (constraint on overall GDP)
    const = [   cv.matmul(np.eye(nPI)-SUT.z.values,SUT.X) >= cv.sum(cv.multiply(y,YY),1,keepdims=True),            
                cv.sum(cv.matmul(SUT.va,SUT.X)) <= GDP   ]

    # problem solution
    prob = cv.Problem(obj,const)
    prob.solve(solver=cv.GUROBI) # add "verbose=True" to get insigths
    print("Optimal value of aggregated Final Demand for Italy is ", -round(prob.value, 0)," M€")
    
    SUT.X = pd.DataFrame(SUT.X.value, index=SUT.Z.index)
    SUT.Y = pd.DataFrame(cv.multiply(y,YY).value, index=SUT.Y.index, columns=SUT.Y.columns)
    SUT.VA = pymrio.calc_F(SUT.va,SUT.X)

def LK_plot (GDP_by_sec, mode='abs', file_title='GDP', fig_title='', shared_yaxes=False, print_svg=False, ref_year=2016):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    activities = list(GDP_by_sec.index)
    years = list(dict.fromkeys(GDP_by_sec.columns.get_level_values(level=1)))
    years_paper = [2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030]
    scenarios = list(dict.fromkeys(GDP_by_sec.columns.get_level_values(level=0)))
    GDP_paper = GDP_by_sec.loc[:,(slice(None),years_paper)]

    if shared_yaxes==True:
        horizontal_spacing = 0.01
    else:
        horizontal_spacing = None
  
    fig = make_subplots(rows=1, cols=4, subplot_titles=scenarios, shared_yaxes=shared_yaxes, horizontal_spacing=horizontal_spacing)
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=25)
        
    color = {'Chemicals':'limegreen',
     'Construction':'dimgrey',
     'Food, beverages & tobacco':'goldenrod',
     'Machinery':'darkslategrey',
     'Metals':'silver',
     'Mining & quarrying':'gold',
     'Non-metallic minerals':'mediumslateblue',
     'Other industry':'ivory',
     'Other sectors':'crimson',
     'Paper, pulp & printing':'turquoise',
     'Textile & leather': 'mediumblue',
     'Transport equipment':'mediumorchid',
     'Wood & wood products':'sienna'}
    
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
    
    
    k = 1
    
    for s in scenarios:
        for a in activities:
            if mode=='net':
                data = GDP_by_sec.loc[a,s].T-GDP_by_sec.loc[a].iloc[2].T
            if mode=='paper':
                data = GDP_paper.loc[a,s].T-GDP_by_sec.loc[a].iloc[2].T
                years = years_paper
            if mode=='net_perc':
                data = 100*(GDP_by_sec.loc[a,s].T-GDP_by_sec.loc[a].iloc[2].T)/GDP_by_sec.loc[a].iloc[2].T
            if mode=='abs':
                data = GDP_by_sec.loc[a,s].T
            
            if len(activities) == len(color):
                colormap = color[a]
            else:
                colormap = colors[activities.index(a)]

            if k == 1:
                first = True
            else:
                first = False
            fig.add_trace(go.Bar(name=a, x=years, y=data, showlegend=first, legendgroup=a, marker_color=colormap), row=1, col=k)

        k = k+1
    fig.update_layout(barmode='relative', title=fig_title, showlegend=True, font_family='Palatino Linotype', font_size=20)
    fig.write_html(file_title+'.html')



