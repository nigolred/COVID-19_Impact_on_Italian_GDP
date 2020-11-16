# -*- coding: utf-8 -*-
"""
aggregation Module
==============================================================================
It is used to provide aggregated data frames from unaggregated matrices
"""
def aggregate(X,Y,VA,S,Z,p):
    

    X_agg = X.groupby(level=[0,2] , sort = False).sum()
            
    Y_agg = Y.groupby(level=[0,2], sort=False).sum()
            
    Z_agg = Z.groupby(level = [0,2],sort=False).sum().groupby(axis = 1 , level = [0,2] , sort = False).sum()
            
    VA_agg = VA.groupby(level=1,sort = False).sum().groupby(axis = 1 , level=[0,2],sort = False).sum()
                        
    S_agg = S.groupby(level=[1,2],sort = False).sum().groupby(axis = 1 , level=[0,2],sort = False).sum()
    p_agg = p.groupby(axis=1, level=[0,2], sort=False).mean()
    
    return X_agg,Y_agg,VA_agg,S_agg,Z_agg,p_agg