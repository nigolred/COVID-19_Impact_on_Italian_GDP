# -*- coding: utf-8 -*-

import pymrio
import numpy as np
import pandas as pd

"""
io_calculation Module
==============================================================================
All the functions in this module are used to calculate the input-output
flows or coefficients.

In most of the cases, pymrio library is used.
"""

def cal_z(Z,X):
    # Calculating the z coefficient matrix
    
    
    return pymrio.calc_A (Z,X)

def cal_s(S,X):
    # can be used for both s and va coefficients
    
    return pymrio.calc_S (S,X)

def cal_l(z):
    # Calculating leontief coefficient from z
    
    return pymrio.calc_L(z)

def cal_l2(z):
    # Calculating leontief coefficient from z
    
    return pd.DataFrame(np.linalg.inv(np.identity(len(z)) - z),index=z.index,columns=z.columns)

def cal_p(va,l):
    # calculating the price index
    
    return pd.DataFrame(va.sum().values.reshape(1,len(va.columns)) @ l.values, index=['Price'], columns=va.columns)

def cal_coef (Z,S,VA,X):
    
    # calculating all the coefficients together
    z  = pymrio.calc_A (Z,X)
    s  = pymrio.calc_S (S,X)
    va = pymrio.calc_S (VA,X)
    l  = pymrio.calc_L(z)
    p  = cal_p(va,l)
    
    return z,s,va,l,p

def cal_Z (z,X):
    
    # Calculating Z flow matrix
    
    return pymrio.calc_Z(z, X)
    
def cal_X(l,Y,index):
    
    # Calculating X from l and Y
    
    return pd.DataFrame(l.values @ Y.values , index = index['X_ind'] , columns =  index['X_col'])
    
def  cal_X_from_L(L, y): 
    
    # Calculating X from l and Y by pymrio
    
    return pymrio.calc_x_from_L(L, y)
    
def cal_flows(z,Y,va,s,index):
    
    # Calculating all the flows together
    
    l  = cal_l2(z)
    X  = cal_X(l,Y,index)
    VA = pymrio.calc_F(va, X)
    S  = pymrio.calc_F(s, X)
    Z  = pymrio.calc_Z(z, X)
    p  = cal_p(va,l)
    
    return l,X,VA,S,Z,p
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    