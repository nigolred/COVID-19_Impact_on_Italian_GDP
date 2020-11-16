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

def LK_plot (GDP_by_sec, net=False, file_title='GDP', fig_title='Net Italian GDP by sector from 2016 to 2030 in different scenarios with resepect to 2014 baseline [M€]'):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    activities = list(GDP_by_sec.index)
    years = list(dict.fromkeys(GDP_by_sec.columns.get_level_values(level=1)))
    scenarios = list(dict.fromkeys(GDP_by_sec.columns.get_level_values(level=0)))
    
    fig = make_subplots(rows=1, cols=4, subplot_titles=scenarios)

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
    
    k = 1
    
    for s in scenarios:
        for a in activities:
            if net:
                data = GDP_by_sec.loc[a,s].T-GDP_by_sec.loc[a].iloc[0].T
            else:
                data = GDP_by_sec.loc[a,s].T
            if k == 1:
                first = True
            else:
                first = False
            fig.add_trace(go.Bar(name=a, x=years, y=data, showlegend=first, legendgroup=a, marker_color=color[a]), row=1, col=k)

        k = k+1
    fig.update_layout(barmode='relative', title=fig_title, showlegend=True)
    fig.write_html(file_title+'.html')
