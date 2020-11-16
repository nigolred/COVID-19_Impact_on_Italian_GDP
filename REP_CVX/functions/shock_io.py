# -*- coding: utf-8 -*-

import pandas as pd
from REP_CVX.functions.io_calculation import cal_z
from REP_CVX.functions.io_calculation import cal_s
"""
shock_io Module
==============================================================================
All the functions in this module are used to read the data related to the shocks
from the excel files and implement the shock on the specific matrix.
----------
Y_shock  :  Final demand shock implementation

Z_shock  :  Technical change shock implementation

VA_shock :  economic factor shock implementation

S_shock  :  satellite account shock implementation


    Parameters
    ----------
    path : string
        Specifies the path of the shock excel file.

    Returns
    -------
    DataFrame
        shocked coefficient matrices or final demand.

"""
def Y_shock (path,Y):
    
    # Reading the final demand shock page
    Y_sh = pd.read_excel(path, sheet_name = 'Y', index_col = [0] , header = [0])
    
    # reading the information
    rows   = list(Y_sh['row'].values)
    values = list(Y_sh['value'].values)
    # Impelenting the changes
    Y.loc[('Commodities',rows),'Total final demand'] = \
        Y.loc[('Commodities',rows),'Total final demand'].values + values
        
    return Y
            
def Z_shock (path,z,Z,X):
    
    # Reading the excel file of the shock
    Z_sh = pd.read_excel(path, sheet_name = 'Z', index_col = [0] , header = [0])
    
    # Taking the information to be impelemented in z
    rows        = list(Z_sh['row'].values)          # specific name of row
    level_rows  = list(Z_sh['level_row'].values)    # Level of row: Activity or Commodity
    cols        = list(Z_sh['col'].values)          # specific name of column 
    level_cols  = list(Z_sh['level_col'].values)    # Level of columns: Activity or Commodity
    types       = list(Z_sh['type'].values)         # Absolute or Percentage
    values      = list(Z_sh['value'].values)        # Value of the change
    aggreg      = list(Z_sh['aggregated'].values)   # Aggregated level or not
    
    #--------------------------- NOTE -----------------------------------------
    # To impelent all the changes, a loop on the rows is used in which.
    
    # Every row represents a change with multiple possibilities. 
    #       1. if the change is in percentage:
    #           In this case the change will be implemented in z:
        
    #       2. If the change is in absolute values
    #           In this case, the change should be implemented on Z. Then z:
    #           should be calculated from cal_z(Z,X) which returns z.
    
    # Besides that, there are two other situation as below:
    #       A. Aggregated level shock:
    #           In this case, the shock should be implemented in the aggregated level
    
    #       B. Non-Aggregated level shock:
    #           Shock on the normal level
    
    #--------------------------------------------------------------------------  
    
    for i in range (len(rows)):
        if types[i] == 'Percentage':
            if aggreg[i] == 'No':
                z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])] = \
                    z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])].values * (1+values[i])
            elif aggreg[i] == 'Yes':
                z.loc[(level_rows[i],slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    z.loc[(level_rows[i],slice(None),rows[i]),(level_cols[i],cols[i])].values * (1+values[i])      
            else: 
                raise ValueError('Aggregation could be \'Yes\' or \'No\'. Please check shock excel file.') 
                
        elif types[i] == 'Absolute':
            if aggreg[i] == 'No':
                
                Z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])] = \
                    Z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])].values + values[i]
                
                new_z = cal_z(Z,X)
                
                z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])] = \
                    new_z.loc[(level_rows[i],rows[i]),(level_cols[i],cols[i])].values 
                
            elif aggreg[i] == 'Yes':
                Z.loc[(level_rows[i],slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    Z.loc[(level_rows[i],slice(None),rows[i]),level_cols[i],cols[i]].values + values[i]
                
                new_z = cal_z(Z,X)
                
                z.loc[(level_rows[i],slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    new_z.loc[(level_rows[i],slice(None),rows[i]),level_cols[i],cols[i]].values    
            else: 
                raise ValueError('Aggregation could be \'Yes\' or \'No\'. Please check shock excel file.')  
                
        else:
            raise ValueError('Type of the shock can be \'Absolute\' or \'Percentage\'. Please check shock excel file.')
            
    return z

def VA_shock(path,va,VA,X):
    
    # Reading the excel file of the shock     
    VA_sh = pd.read_excel(path, sheet_name = 'VA', index_col = [0] , header = [0])   
    
    
    # Taking the information to be impelemented in va  
    rows        = list(VA_sh['row'].values)         # specific name of row
    cols        = list(VA_sh['col'].values)         # specific name of column
    level_cols  = list(VA_sh['level_col'].values)   # Level of columns: Activity or Commodity
    types       = list(VA_sh['type'].values)        # Absolute or Percentage
    values      = list(VA_sh['value'].values)       # Value of the change
    aggreg      = list(VA_sh['aggregated'].values)  # Aggregated level or not
    
    #--------------------------- NOTE -----------------------------------------
    # To impelent all the changes, a loop on the rows is used in which.
    
    # Every row represents a change with multiple possibilities. 
    #       1. if the change is in percentage:
    #           In this case the change will be implemented in z:
        
    #       2. If the change is in absolute values
    #           In this case, the change should be implemented on Z. Then z:
    #           should be calculated from cal_z(Z,X) which returns z.
    
    # Besides that, there are two other situation as below:
    #       A. Aggregated level shock:
    #           In this case, the shock should be implemented in the aggregated level
    
    #       B. Non-Aggregated level shock:
    #           Shock on the normal level
    
    #-------------------------------------------------------------------------- 
    
    for i in range (len(rows)):
        if types[i] == 'Percentage':
            if aggreg[i] == 'No':
                va.loc[rows[i],(level_cols[i],cols[i])] = \
                    va.loc[rows[i],(level_cols[i],cols[i])].values * (1+values[i])
            elif aggreg[i] == 'Yes':

                va.loc[(slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    va.loc[(slice(None),rows[i]),(level_cols[i],cols[i])].values * (1+values[i])      
            else: 
                raise ValueError('Aggregation could be \'Yes\' or \'No\'. Please check shock excel file.') 
                
        elif types[i] == 'Absolute':
            if aggreg[i] == 'No':
                
                VA.loc[rows[i],(level_cols[i],cols[i])] = \
                    VA.loc[rows[i],(level_cols[i],cols[i])].values + values[i]
                
                new_va = cal_s(VA,X)
                
                va.loc[rows[i],(level_cols[i],cols[i])] = \
                    new_va.loc[rows[i],(level_cols[i],cols[i])].values
                
            elif aggreg[i] == 'Yes':
                VA.loc[(slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    VA.loc[(slice(None),rows[i]),level_cols[i],cols[i]].values + values[i]
                
                new_va = cal_s(VA,X)
                
                va.loc[(slice(None),rows[i]),(level_cols[i],cols[i])] = \
                    new_va.loc[(slice(None),rows[i]),level_cols[i],cols[i]].values   
                    
            else: 
                raise ValueError('Aggregation could be \'Yes\' or \'No\'. Please check shock excel file.')  
                
        else:
            raise ValueError('Type of the shock can be \'Absolute\' or \'Percentage\'. Please check shock excel file.')

    return va


def S_shock(path,s,S,X):
    
    # Reading the excel file of the shock
    S_sh = pd.read_excel(path, sheet_name = 'S', index_col = [0] , header = [0])
    
    # Taking the information to be impelemented in s
    rows        = list(S_sh['row'].values)          # specific name of row
    cols        = list(S_sh['col'].values)          # specific name of column
    types       = list(S_sh['type'].values)         # Absolute or Percentage
    values      = list(S_sh['value'].values)        # Value of the change
    level_cols  = 'Activities'
    
    #--------------------------- NOTE -----------------------------------------
    # To impelent all the changes, a loop on the rows is used in which.
    
    # Every row represents a change with multiple possibilities. 
    #       1. if the change is in percentage:
    #           In this case the change will be implemented in z:
        
    #       2. If the change is in absolute values
    #           In this case, the change should be implemented on Z. Then z:
    #           should be calculated from cal_z(Z,X) which returns z.
    
    #-------------------------------------------------------------------------- 
    
    for i in range (len(rows)):
        if types[i] == 'Percentage':
            s.loc[rows[i],(level_cols,cols[i])] = \
                    s.loc[rows[i],(level_cols,cols[i])].values * (1+values[i])
            
        elif types[i] == 'Absolute':
            S.loc[rows[i],(level_cols,cols[i])] = \
                    S.loc[rows[i],(level_cols,cols[i])].values + values[i]
            new_s = cal_s(S,X)
            
            s.loc[rows[i],(level_cols,cols[i])] = \
                new_s.loc[rows[i],(level_cols,cols[i])] .values
            
    return s
































