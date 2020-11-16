# -*- coding: utf-8 -*-
"""
check Module
==============================================================================
All the functions in this module are used to check the possible errors in the 
inputs of the different functions by the user
"""

def unit_check(unit):
    '''
    This function checks if a given Unit is listed in the acceptable units
    '''
    unit_list = ['M USD','M EUR', 'M KSH','K KSH','K USD','K EUR','M GHC']
    
    if unit not in unit_list:
        raise ValueError('Unit should be one of the followings: {}. To add more units, the user can use REP_CVX.functions.check module'.format(unit_list))
        
    return unit

def unit_converter(unit1,unit2):
    '''
    This function converts the units between the listed units
    '''
    # For now, we use following simple script for the conversion. In the next step, a library will be added to the code.
    convert_list = {'M KSH_M USD': 0.00939548 ,'M KSH_M EUR': 0.00833961, 'M KSH_K USD': 0.00939548*1000 ,'M KSH_K EUR': 0.00833961*1000, 'M KSH_K KSH': 1000,
                    'M GHC_M USD': 0.0000171550, 'M GHC_M EUR': 0.0000145311, 'M GHC_K USD': 0.0000171550*1000, 'M GHC_K EUR': 0.0000145311*1000, 'M GHC_K GHC': 1000}
    
    if unit1 == unit2: conversion = 1
    else: conversion = convert_list['{}_{}'.format(unit1,unit2)]

    
    return conversion

def style_check(style):
    
    '''
    This function check if the plot style is valid or not.
    '''
    
    styles = ['default','classic','Solarize_Light2','_classic_test','bmh',
              'dark_background','fast','fivethirtyeight','ggplot','grayscale',
              'seaborn','seaborn-bright','seaborn-colorblind','seaborn-dark',
              'seaborn-dark-palette','seaborn-darkgrid','seaborn-deep',
              'seaborn-muted','seaborn-notebook','seaborn-paper',
              'seaborn-pastel','seaborn-poster','seaborn-talk','seaborn-ticks',
              'seaborn-white','seaborn-whitegrid','tableau-colorblind10']
    
    if style not in styles:
        
        raise ValueError ('{} is not correct. Acceptable styles are : \n {} \n For more information: https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html'.format(style,styles))
        
    return style

def level_check(level):
    '''
    This function check if the given level is correct or not and provide the
    title for completing the graph titles by default:
        
        If level='Activities'  --> title = ' by Activities'
        If level='Commodities' --> title = ' by Commodities'
    '''
    # Acceptable levels
    levels = ['Activities' , 'Commodities']
    
    # if level is not None
    if level != None :
        # Check if it is not in the acceptable levels, raise an error
        if level not in levels: raise ValueError('\'level\' can be: \n 1. \'Activities\' \n 2. \'Commodities\' \n 3. \'None\' ')
        # If it is, take the level and retrun the title as described before
        else: title , level = ' by {}'.format(level) , [level]
    # if level is None, retrun both levels and nothing for the title
    else: title , level = '' , levels
        
    return title,level

def kind_check (kind):
    
    '''
    This function check if the given plot kind is correct or not.
    '''
        
    kinds = ['Absolute','Percentage']
    if kind not in kinds:
        raise ValueError('\'kind\' can be: \n 1. \'Absolute\' /n 2. \'Percentage\'')
    
    return kind
    
def indic_check (indicator,indicators):
    
    '''
    This function check if the given indicator for plot_ds exists in the database
    or not.
    '''
    
    indicators = list(dict.fromkeys(indicators))

    if indicator not in indicators:
        raise ValueError('\'{}\' not found in {}'.format(indicator, indicators))
        
    return indicator
    
def var_check(var):
    
    '''
    This function check if the given variable is an acceptable one or not.
    '''    
    vars = ['VA','X','S','p']
    
    if var not in vars:
        raise ValueError('Acceptable variables are {}'.format(vars))
        
    return var
        

    
    
        
    
    
    
    
    
    