# -*- coding: utf-8 -*-
'''
utility Module
==============================================================================

A module for providing some useful functions

Functions
----------
indeces:        Provides a dict of the indeces that can be used for different purposes

dict_maker:     Stores the given information in a dictionary.
'''
import xlsxwriter
import pandas as pd
import os

        
def indeces (S,Z,VA,X):

    return {'Z_ind': Z.index , 'VA_ind':VA.index , 'S_ind': S.index , 
            'X_ind': X.index ,'Z_col': Z.columns , 'VA_col':VA.columns , 
            'S_col': S.columns , 'X_col':X.columns}

def dict_maker(Z=None,X=None,VA=None,p=None,Y=None,va=None,z=None,s=None,
               Z_agg=None,X_agg=None,VA_agg=None,Y_agg=None,S_agg=None,p_agg=None):
    
    inputs =  [Z,X,VA,p,Y,va,z,s,Z_agg,X_agg,VA_agg,Y_agg,S_agg,p_agg]
    outputs = ['Z','X','VA','p','Y','va','z','s','Z_agg','X_agg','VA_agg','Y_agg','S_agg','p_agg']
    
    dictionary = {}
    
    for i  in range(len(inputs)):
        if inputs[i] is not None:
            dictionary[outputs[i]]=inputs[i]
               
    return dictionary

def unit_taker(S):
    
    return pd.DataFrame(S.index.get_level_values(2).to_list(),index=S.index.get_level_values(1).to_list(),columns=['Units'])

def value_from_excel(path):
    
    import xlwings as xl
    app = xl.App(visible=False)
    book = app.books.open(path)
    book.save()
    app.kill()

def file_exist(directory):
    
    # This function checks if a given directory exists or not
    
    dir = directory
    return os.path.exists(dir)
        
def sh_excel(num_shock,indeces):
    
    # Defining the headers

    level = ['Activities','Commodities']
    rc    = indeces['X_ind'].get_level_values(1).to_list()
    va    = indeces['VA_ind'].get_level_values(0).to_list()
    types = ['Percentage','Absolute']
    yn = ['Yes','No']
    
    
    # Building the excel file
    file = 'excel_shock.xlsx'
    workbook = xlsxwriter.Workbook(file)
    
        # Add a format for the header cells.
    header_format = workbook.add_format({
        'border': 1,
        'bg_color': '#C6EFCE',
        'bold': True,
        'text_wrap': False,
        'valign': 'vcenter',
        'indent': 1,
    })
    
    # Filling the index indeces sheet
    indeces = workbook.add_worksheet('indeces')  
    for i in range(len(rc)):
        indeces.write('A{}'.format(i+1),rc[i])
    for i in range(len(va)):
        indeces.write('B{}'.format(i+1),va[i])

    act_com_ref = '=indeces!$A$1:$A${}'.format(len(rc))
    va_ref      = '=indeces!$B$1:$B${}'.format(len(va))
    
    # Building the main sheet
    main = workbook.add_worksheet('main')
    
    main.write('A1', 'Legend', header_format)
    main.write('B1', 'Description', header_format)
    main.write('C1', 'Value', header_format)
    main.write('D1', 'Unit of measure', header_format)
    main.write('E1', 'Sensitivity', header_format)
    main.write('F1', 'Min', header_format)
    main.write('G1', 'Max', header_format)
    main.write('H1', 'Step', header_format)  
    main.write('I1', 'Affected Parameter', header_format)    
    main.write('J1', 'Notes', header_format)    
    main.write('K1', 'References', header_format)    
    
    for i in range(num_shock):
        
        main.data_validation('E{}'.format(i+2), {'validate': 'list',
                                      'source': yn})    
    # Building the Y sheet
    Y = workbook.add_worksheet('Y')
    Y.write('A1','Number',header_format)
    Y.write('B1','row',header_format)
    Y.write('C1','value',header_format)

    for i in range(num_shock):
        
        Y.write('A{}'.format(i+2), str(i))
        
        Y.data_validation('B{}'.format(i+2), {'validate': 'list',
                                      'source': act_com_ref})
     

    # Builidng the VA sheet
    VA = workbook.add_worksheet('VA')

    VA.write('A1','Number',header_format)
    VA.write('B1','row',header_format)
    VA.write('C1','level_col',header_format)
    VA.write('D1','col',header_format)
    VA.write('E1','type',header_format)  
    VA.write('F1','value',header_format)
    VA.write('G1','aggregated',header_format) 
     
    for i in range(num_shock):
        
        VA.write('A{}'.format(i+2), str(i))
        
        VA.data_validation('B{}'.format(i+2), {'validate': 'list',
                                      'source': va_ref})
        VA.data_validation('C{}'.format(i+2), {'validate': 'list',
                                      'source': level})  
        VA.data_validation('D{}'.format(i+2), {'validate': 'list',
                                      'source': act_com_ref})
        VA.data_validation('E{}'.format(i+2), {'validate': 'list',
                                      'source':  types})
        VA.data_validation('G{}'.format(i+2), {'validate': 'list',
                                      'source': yn})
        
    # Building the Z sheet
    Z = workbook.add_worksheet('Z')
    

    
    # Write the header cells and some data that will be used in the examples.
    heading1 = 'Number'
    heading2 = 'level_row'
    heading3 = 'row'
    heading4 = 'level_col'
    heading5 = 'col'
    heading6 = 'type'
    heading7 = 'value'
    heading8 = 'aggregated'

    
    
    
    Z.write('A1', heading1, header_format)
    Z.write('B1', heading2, header_format)
    Z.write('C1', heading3, header_format)
    Z.write('D1', heading4, header_format)
    Z.write('E1', heading5, header_format)
    Z.write('F1', heading6, header_format)
    Z.write('G1', heading7, header_format)
    Z.write('H1', heading8, header_format)

    
    sheet_reference_str = '=indeces!$A$1:$A$1{}'.format(len(rc))
    
    for i in range(num_shock):
        
        Z.write('A{}'.format(i+2), str(i))
        
        Z.data_validation('B{}'.format(i+2), {'validate': 'list',
                                      'source': level})
        Z.data_validation('C{}'.format(i+2), {'validate': 'list',
                                      'source': act_com_ref})  
        Z.data_validation('D{}'.format(i+2), {'validate': 'list',
                                      'source': level})
        Z.data_validation('E{}'.format(i+2), {'validate': 'list',
                                      'source':  act_com_ref})
        Z.data_validation('F{}'.format(i+2), {'validate': 'list',
                                      'source': types})  
        Z.data_validation('H{}'.format(i+2), {'validate': 'list',
                                      'source': yn})

    workbook.close()

    
    
    
    