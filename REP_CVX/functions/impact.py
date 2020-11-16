# -*- coding: utf-8 -*-
'''
impact Module
==============================================================================

A module for impact assessment calculations

Functions
----------
impact_check:   Taking the information from the user and find and reform 
                the appropriate sets of information and check the errors in the
                input to provide the appropriate ValueError

impact_assessment:  calculating the impacts of the policy
'''
def impact_check(inv,sav,results):
    '''
    

    Parameters
    ----------
    inv : list
        a list of the information of the inv step as specified in the class 
        document.
    sav : list
        a list of the information of the saving step as specified in the class 
        document.
    results : dictionary
        results dictionary of the main object.

    Raises
    ------
    ValueError
        1. Wrong format of the inputs
        2. sav and inv sensitivity impact assessment. IT IS NOT POSSIBLE!

    Returns
    -------
    save_out : dict
        reshaped information of the sav scenario compatible with inv_out.
    inv_out : dict
        reshaped information of the inv scenario compatible with save_out.
    sav_list : list
        returns the information of the sensitivities for multiple impact assessment
        for every sensitivity case.

    '''
    # Acceptable inputs
    list1 = {'sh':'shock','se':'sensitivity'}
    sav_list,inv_list = [],[]
    save_out,inv_out  = {},{}
    
    # This parameter will be used for taking the sensitivity parameter
    # for better representation of the impact analysis
    s_par = None
    
    # Check if the shape of the input list is correct
    if len(inv)!=2 or len(sav) != 2:
        raise ValueError('Wrong input for invest_sce and saving_sce. \n Two valuse should be given as follow:\
                          \n [type of the input,the number of the specifict input] ')
     
    # Check if the input is acceptable or not
    if  inv[0] not in list1 or sav[0] not in list1:
        raise ValueError('The first argument can be one of the followings: {}'.format(list1))       
    
    # both inv and sav cant be based on sensitivity
    if inv[0]  == 'se' and sav[0] == 'se':
        raise ValueError('both \'saving_sce\' and \'invest_sce\' cannot be based on \'sensitivity\' level.')
        
    # Check if the entered information exists or not. Then fill the list
    try: 
        results['{}_{}'.format(list1[inv[0]],inv[1])]
        if inv[0]=='se':
            for key, value in results['{}_{}'.format(list1[inv[0]],inv[1])].items(): 
               if key != 'information':
                   inv_list.append(key)
               elif key == 'information':
                   # Returning the the name of the sensitivity parameter
                   s_par = results['{}_{}'.format(list1[inv[0]],inv[1])][key]['parameter']
    except: 
        raise ValueError('{}_{} does not exists in results dictionary'.format(list1[inv[0]],inv[1]))
      
    # Check if the entered information exists or not. Then fill the list
    try: 
        results['{}_{}'.format(list1[sav[0]],sav[1])]
        if sav[0]=='se':
            for key, value in results['{}_{}'.format(list1[sav[0]],sav[1])].items(): 
               if key != 'information':
                   sav_list.append(key)    
               elif key == 'information':
                   # Returning the the name of the sensitivity parameter
                   s_par = results['{}_{}'.format(list1[sav[0]],sav[1])][key]['parameter']                   
    except: raise ValueError('{}_{} does not exists in results dictionary'.format(list1[sav[0]],sav[1]))
    
    
    #--------------------------- NOTE ---------------------------
    # There are 3 different cases that can be happen based on the type of the
    # input: 1. both shock, 2. sav shock and inv sensitivty or 3. inv shock and 
    # sav sensitivity. In the cases that a sensitivity exists, we need to have
    # the same value of the shock matrix repeated by the len of the sensitivity
    # to ease the calculations
    #------------------------------------------------------------
    
    
    # Making the dictionaries for outout
    
    # The case that sav is based on sensitivity
    if len(sav_list)>len(inv_list):
        for i in sav_list:
            save_out[i]= results['{}_{}'.format(list1[sav[0]],sav[1])][i]
            inv_out [i]= results['{}_{}'.format(list1[inv[0]],inv[1])] # Just repeat it
            
    # The case that inv is based on sensitivity      
    elif len(sav_list)<len(inv_list):
        for i in inv_list:
            save_out[i]= results['{}_{}'.format(list1[sav[0]],sav[1])] # just repeat it
            inv_out [i]= results['{}_{}'.format(list1[inv[0]],inv[1])][i] 
            sav_list = inv_list
            
    # The case that both are based on shock     
    else: 
        sav_list = ['baseline']
        save_out['baseline'] = results['{}_{}'.format(list1[sav[0]],sav[1])]
        inv_out ['baseline'] = results['{}_{}'.format(list1[inv[0]],inv[1])]
        
        
    return save_out,inv_out,sav_list,s_par

def impact_assessment(invest_sce,saving_sce,results,p_life,w_ext,em_ext,land,
                      labour,capital,imports,directory,save_excel,im_num,
                      monetary_unit,extensions_units,name):
    
    '''
    Parameters
    ----------
    As described in the main class


    Returns
    -------
    Imp : Dataframe
        Contains all the indicators of the impact assessment
        
    Introducing A New Indicator
    ----------------------------
    
    To introduce an indicator the following steps should be done:
        1. Add the name of the indicator to the list named : "columns"
        2. In the loop, the way that the indicator is caluclated should be 
        represented as the follwoing form:
            Imp.loc[i,'name of the indicator as added in the columns'] = calculation
            
    **************************************************************************            
    NOTE: the parameters results,save_out,inv_out are dict in which contains
    all the information related to saving scenario,investment scenario, and baseline 
    scenario to calculate the impact. So, in case that new indicators are added,
    please take care of that fact, and follow the existing indicators codes.
    **************************************************************************
    '''
    
    import pandas as pd
    save_out,inv_out,sav_list,s_par = impact_check(invest_sce,saving_sce,results)
    
    columns = ['Investment','Saving','PROI','PPBT','Water Saving','Emission Saving','Land Saving','Import Saving',
               'Capital Saving','Workforce Saving','Water Investment','Emission Investment',
               'Land Investment','Import Investment','Workforce Investment','Capital Investment',
               'Water Total Impact','Emission Total Impact','Land Total Impact','Import Total Impact',	
               'Workforce Total Impact','Capital Total Impact']


    Imp = pd.DataFrame(index=sav_list,columns=columns)
    Imp.fillna(0)


    for i in sav_list:
        
        Imp.loc[i,'Investment'] = inv_out[i]['VA'].values.sum().sum() - results['baseline']['VA'].sum().sum()
        Imp.loc[i,'Saving'] = + results['baseline']['VA'].sum().sum()-save_out[i]['VA'].values.sum().sum()
        
        Imp.loc[i,'Water Investment'] =  inv_out[i]['S_agg'].loc[w_ext].sum().sum() - results['baseline']['S_agg'].loc[w_ext].sum().sum()
        Imp.loc[i,'Water Saving'] =  -save_out[i]['S_agg'].loc[w_ext].sum().sum() + results['baseline']['S_agg'].loc[w_ext].sum().sum()
            
        Imp.loc[i,'Emission Investment'] =  inv_out[i]['S_agg' ].loc[em_ext].sum().sum() - results['baseline']['S_agg'].loc[em_ext].sum().sum()
        Imp.loc[i,'Emission Saving'] = -save_out[i]['S_agg'].loc[em_ext].sum().sum() + results['baseline']['S_agg'].loc[em_ext].sum().sum()    
            
        Imp.loc[i,'Land Investment'] =  inv_out[i]['S_agg'].loc[land].sum().sum() - results['baseline']['S_agg'].loc[land].sum().sum()
        Imp.loc[i,'Land Saving'] = -save_out[i]['S_agg'].loc[land].sum().sum() + results['baseline']['S_agg'].loc[land].sum().sum()    


        Imp.loc[i,'Workforce Investment'] = inv_out[i]['VA'].groupby(level=1).sum().loc[labour].sum().sum() - results['baseline']['VA'].groupby(level=1).sum().loc[labour].sum().sum()   
        Imp.loc[i,'Workforce Saving'] = -save_out[i]['VA'].groupby(level=1).sum().loc[labour].sum().sum() + results['baseline']['VA'].groupby(level=1).sum().loc[labour].sum().sum() 
            
        Imp.loc[i,'Capital Investment'] = inv_out[i]['VA'].groupby(level=1).sum().loc[capital].sum().sum() - results['baseline']['VA'].groupby(level=1).sum().loc[capital].sum().sum()   
        Imp.loc[i,'Capital Saving'] = -save_out[i]['VA'].groupby(level=1).sum().loc[capital].sum().sum() + results['baseline']['VA'].groupby(level=1).sum().loc[capital].sum().sum() 
            
        Imp.loc[i,'Import Investment'] = inv_out[i]['VA'].groupby(level=1).sum().loc[imports].sum().sum() - results['baseline']['VA'].groupby(level=1).sum().loc[imports].sum().sum()
        Imp.loc[i,'Import Saving'] = -save_out[i]['VA'].groupby(level=1).sum().loc[imports].sum().sum() + results['baseline']['VA'].groupby(level=1).sum().loc[imports].sum().sum()    

        
        Imp.loc[i,'PROI'] = Imp.loc[i,'Saving'] / Imp.loc[i,'Investment']
        Imp.loc[i,'PPBT'] = 1 / Imp.loc[i,'PROI'] 
    
    
        # Total Impacts
        Imp.loc[i,'Water Total Impact']         = Imp.loc[i,'Water Investment'] - p_life * Imp.loc[i,'Water Saving']
        Imp.loc[i,'Emission Total Impact']      = Imp.loc[i,'Emission Investment'] - p_life * Imp.loc[i,'Emission Saving']
        Imp.loc[i,'Land Total Impact']          = Imp.loc[i,'Land Investment'] - p_life * Imp.loc[i,'Land Saving']
        Imp.loc[i,'Import Total Impact']        = Imp.loc[i,'Import Investment'] - p_life * Imp.loc[i,'Import Saving']
        Imp.loc[i,'Workforce Total Impact']     = Imp.loc[i,'Workforce Investment'] - p_life * Imp.loc[i,'Workforce Saving']
        Imp.loc[i,'Capital Total Impact']       = Imp.loc[i,'Capital Investment'] - p_life * Imp.loc[i,'Capital Saving']  

    # Reindexing the dataframe for better representation
    units = [monetary_unit,monetary_unit,'1/years','years',extensions_units.loc['Water'].iloc[0,0],extensions_units.loc['CO2'].iloc[0,0],
             extensions_units.loc['Land'].iloc[0],monetary_unit, monetary_unit,monetary_unit,extensions_units.loc['Water'].iloc[0,0],
             extensions_units.loc['CO2'].iloc[0,0], extensions_units.loc['Land'].iloc[0],monetary_unit,monetary_unit,monetary_unit,
             extensions_units.loc['Water'].iloc[0,0],extensions_units.loc['CO2'].iloc[0,0],extensions_units.loc['Land'].iloc[0],monetary_unit,	
             monetary_unit,monetary_unit]
    
    index_0 = [name] * len(sav_list)
    if len(sav_list) == 1:
        index = [index_0,['baseline']]
        s_par = 'baseline'
    else:
        index_1 = [s_par]*len(sav_list)
        index = [index_0,index_1,sav_list]

    Imp.index = index
    Imp.columns = [columns,units]
    if save_excel:
        with pd.ExcelWriter(r'{}/{} - {}.xlsx'.format(directory,name,s_par)) as writer:
            Imp.to_excel(writer)
            
    return Imp
    
    
    
    
    
    
    
    
    
    
    
    
    
