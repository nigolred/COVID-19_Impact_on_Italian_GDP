# -*- coding: utf-8 -*-
'''
REP_CVX - A python module for automating SU-IO calculations and generating reports
==============================================================================

The classes and tools in this module should work with any Supply and Use table following the structure defined in the tutorial.

The main class of the module "C_CUT" :
    
The calss has multiple typical tools for input-output analysis:
    
    1. Calculating all the matrices of flows and coefficients from a given database
    2. Implementing shocks 
    3. Sensitivity Analysis on the shocks
    4. Policy impact assesment
    5. Visualizing results and generating reports
    
Data storage
------------
xlsx files together is used for storing data. In addition,
the "C_SUT" with all data can also be pickled (binary).


----
Dependencies:

- pandas
- matplotlib
- seaborn
- pymrio
- pickle
- numpy

Author:
    Mohammad Amin Tahavori
    
Co-Authors:
    Negar Namazifard
    Nicolo Golinucci
    
:license: 

'''
from REP_CVX.version import __version__
from REP_CVX.functions.core import C_SUT
from REP_CVX.functions.lk_model import LK_model, LK_plot
from REP_CVX.functions.io_calculation import cal_z
from REP_CVX.functions.io_calculation import cal_s
from REP_CVX.functions.io_calculation import cal_l2
from REP_CVX.functions.io_calculation import cal_p
from REP_CVX.functions.io_calculation import cal_coef
from REP_CVX.functions.io_calculation import cal_Z
from REP_CVX.functions.io_calculation import cal_X
from REP_CVX.functions.io_calculation import cal_flows