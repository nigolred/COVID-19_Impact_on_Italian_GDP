# -*- coding: utf-8 -*-

from REP_CVX.version import info
from REP_CVX.functions.data_read import database
from REP_CVX.functions.check import unit_check
from REP_CVX.functions.io_calculation import cal_coef
from REP_CVX.functions.utility import indeces
from REP_CVX.functions.aggregation import aggregate
from REP_CVX.functions.utility import dict_maker
from REP_CVX.functions.utility import unit_taker
from REP_CVX.functions.io_calculation import cal_flows
from REP_CVX.functions.plots import delta_xv
from REP_CVX.functions.plots import delta_s
from REP_CVX.functions.plots import delta_p
from REP_CVX.functions.plots import ptl_sensitivity
from REP_CVX.functions.impact import impact_assessment
from REP_CVX.functions.data_read import sens_info
from REP_CVX.functions.utility import value_from_excel
from REP_CVX.functions.check import var_check
from REP_CVX.functions.data_read import sensitivity_take
from REP_CVX.functions.utility import sh_excel
from warnings import filterwarnings


import shutil
import glob
import pickle
import REP_CVX.functions.shock_io as sh



class C_SUT():
    
    ''' C_SUT Class

    The class reads the given database in form of an excel file and built all 
    pandas DataFrames of the flows and coefficients of the IO system. 
    
    Arguments
    ----------
    path :  the path of the database excel file.
    
    unit :  represepnts the main unit of the flows in the table. This will be 
            used for the unit conversions.  
            
    Notes
    -----
        1. The attributes and extension dictionary entries are pandas.DataFrame
        with an MultiIndex.  This index must have the specified level names.
        
        2. Capital letters represent the flows and the same letter in small case
        represents the coefficients.
        
        3. Every variable with "_c" represents the values after the last shock 
        implemented.
        
        4. Every variable with "_agg" represents the aggregated variable with
        the same name.

    Attributes
    ----------
    Z : pandas.DataFrame
        Supply and Use flows of activities and commodities
        MultiIndex with levels and aggregatedn and disaggregated names
      
    U,V : pandas.DataFrame
        Use and Supply Matrices
        MultiIndex with levels and aggregatedn and disaggregated names   
        for U: [index=Commodities,columns=Activities]
        for V: [index=Activities,columns=Commodities]
        
    Y : pandas.DataFrame
        final demand with MultiIndex similar to Z matrix
        
    S : pandas.DataFrame
        satellite account
        MultiIndex with levels and aggregatedn and disaggregated names

    VA : pandas.DataFrame
        Economic factor flows
        MultiIndex with levels and aggregatedn and disaggregated names
        
    X : pandas.DataFrame
        Total production of Activities and Commodities
        MultiIndex with levels and aggregatedn and disaggregated names 
        
    l : pandas.DataFrame
        Leontief, MultiTndex as Z

    p : pandas.DataFrame
        price index  

    ''' 
    
    def __init__(self,path,unit,name='intervention'):
        
        '''  
        path :  string
            the path of the database excel file.
                
        unit :  string
            represepnts the main unit of the flows in the table. This will be 
                used for the unit conversions. 
                
        name: string
            represents the name of the intervention for better representation
            of the results.
        '''                          

        # Printing the version and the information of the module
        print(info)
        
        # Check if the unit is correct or not
        self.__m_unit = unit_check(unit)
        
        # Globlizing the name of the intervention
        self.__name = name
        
        # Ignoring the warnings 
        filterwarnings("ignore") 
        
        # Reading the Database
        self.SUT,self.U,self.V,self.Z,self.S,self.Y,self.VA,self.X = database (path)
        
        self.__Units =  unit_taker(self.S)
        
        # Calculating the baseline coefficients
        self.z,self.s,self.va,self.l,self.p = cal_coef (self.Z,self.S,self.VA,self.X)
        
        # Building aggregated results for the baseline
        self.X_agg,self.Y_agg,self.VA_agg,self.S_agg,self.Z_agg,self.p_agg = aggregate(self.X,self.Y,self.VA,self.S,self.Z,self.p)
        
        # Getting indeces
        self.__indeces = indeces (self.S,self.Z,self.VA,self.X)
        
        # All the information needs to be stored in every step because it will be used in some other functions
        self.results = {}
        self.results['baseline']= dict_maker(self.Z,self.X,self.VA,self.p,self.Y,self.va,
                                                self.z,self.s,self.Z_agg,self.X_agg,self.VA_agg,self.Y_agg,self.S_agg,self.p_agg)
        
        
        # A counter for saving the results in a dictionary
        self.__counter   = 1      # Shock Counter
        self.__s_counter = 1      # Sensitivity Counter
        self.__i_counter = 1      # Impact Assessment Couter
        
        
    def shock_calc (self,path,Y=False, VA=False, Z=False, S=False,save=True):
        

        '''  
        shock_calc:
            This function is used to implement a shock
            The shock should be defined through an excel file which is described
            in detail in the tutorial.
            
        As a shock can be implemented in different steps or on differnet matrices
        the user should identify that which matrix of shock excel file should
        be implemented by calling the function.
            
        Arguments
        ----------
        path :  string
            the path of the shock excel file.
                
        Y  :  boolean
            True: Final demand shock
            
        Z  :  boolean  
            True: Technical change shock
             
        VA :  boolean
            True: Economic factor change shock

        S  :  boolean
            True: Satellite account shock  
        
        save: boolean
            True: Saving the results in a dictionary. 
        
        -----------------------------------------------------------------------
        Note: It is suggested to keep "save" always "True". In this way, all the
                information can be stored and used easily.
        -----------------------------------------------------------------------
        
        '''            

    
        # There should be at least one shock!
        if not Y and not VA and not Z and not S:
            raise ValueError('At lest one of the arguments should be \'True\' ')
            
        # Taking a copy of all matrices to have both changed and unchanged ones
        self.Y_c   = self.Y.copy()
        self.va_c  = self.va.copy()
        self.s_c   = self.s.copy()
        self.z_c   = self.z.copy()
        
        # check the type of the shock
        if Y:   self.Y_c  = sh.Y_shock  (path,self.Y_c.copy())                      
        if Z:   self.z_c  = sh.Z_shock  (path,self.z_c.copy(),self.Z.copy(),self.X.copy())
        if VA:  self.va_c = sh.VA_shock (path,self.va_c.copy(),self.VA.copy(),self.X.copy())
        if S:   self.s_c  = sh.S_shock  (path,self.s_c.copy(),self.S.copy(),self.X.copy())
        
        # Calculating the shock result
        self.l_c,self.X_c,self.VA_c,self.S_c,self.Z_c,self.p_c = cal_flows(self.z_c,self.Y_c,self.va_c,self.s_c,self.__indeces)        
        
        
        # Aggregation of the results
        self.X_c_agg,self.Y_c_agg,self.VA_c_agg,self.S_c_agg,self.Z_c_agg,self.p_c_agg = aggregate(self.X_c,self.Y_c,self.VA_c,self.S_c,self.Z_c,self.p_c)
        
        # Saving all the new matrices in the results dictionary.
        if save:
            self.results['shock_{}'.format(self.__counter)]= dict_maker(self.Z_c,self.X_c,self.VA_c,self.p_c,self.Y_c,self.va_c,
                                                self.z_c,self.s_c,self.Z_c_agg,self.X_c_agg,self.VA_c_agg,self.Y_c_agg,self.S_c_agg,self.p_c_agg)
            self.__counter += 1
            
        
    def plot_dx (self,aggregated=True,unit='default',level=None,kind='Absolute',
                fig_format='png',title_font=15,style='ggplot',figsize=(10, 6),
                directory='Charts',ranshow=(0,0),title='default',color = 'rainbow', drop=None,save_excel=True):
        

        
        '''  
        plot_dx:
            This function is used to plot delta_x between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        aggregated  :  boolean
            True: Showing aggregated results of production
            
        unit  :  string
            default: the unit will be equal the the main unit in the database
            or the user can choose the unit among the acceptable units.
             
        level :  string
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level

        kind  :  string
            Absolute: Absolute change
            Percentage: Relative change
            
        title:  string
            The user can choose a specific title otherwise the default title
            will be used.
            
        fig_format: string
            To save the plot
                    'png','svg'
        
        title_font:  float
            size of title font
        
        style: string
            Plot style
        
        figsize: tuple
            Figure size
        
        directory: string
            the directory to save the results
        
        ranshow: tuple
            it represents the range of the values to be shown:
                    (Max value,Min value)
                    
        color: colormap:string  , colors:list 
            could be colormap or a list of colors
        
        drop: list
            To drop specific categories from the data
               
        save_excel: boolean
                    If True, the results will be saved also in form of excel file
                    in the same directory
             
        ''' 
        
        directory='{}\{}'.format(self.__name,directory)

        # Check if the shock result exist or not
        if not hasattr(self, 'X_c'):raise ValueError('To run the plot function, there should be an implemented shock.')

        
        # To check the input to the plot function in the aggregated level or disaggregated
        if aggregated:
            X_c,X = self.X_c_agg,self.X_agg    
        else:
            X_c,X = self.X_c,self.X
            
        delta_xv(X_c,X,style,unit,self.__m_unit,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,'X',drop,save_excel)


    def plot_dv(self,aggregated=True,unit='default',level=None,kind='Absolute',
                fig_format='png',title_font=15,style='ggplot',figsize=(10, 6),
                directory='Charts',ranshow=(0,0),title='default',color = 'terrain'
                , drop= None,save_excel=True):
        
        '''  
        plot_dv:
            This function is used to plot delta_VA between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        aggregated  :  boolean
            True: Showing aggregated results of production
            
        unit  :  string
            default: the unit will be equal the the main unit in the database
            or the user can choose the unit among the acceptable units.
             
        level :  string
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level

        kind  :  string
            Absolute: Absolute change
            Percentage: Relative change
            
        title: string
            The user can choose a specific title otherwise the default title
            will be used.
            
        fig_format: string
            To save the plot
                    'png','svg'
        
        title_font: float
            size of title font
        
        style: string
            Plot style
        
        figsize: tuple
            Figure size
        
        directory: string
            the directory to save the results
        
        ranshow: tuple
            it represents the range of the values to be shown:
                    (Max value,Min value)
                    
        color: colormap:string  , colors:list 
            could be colormap or a list of colors
        
        drop: list
            To drop specific categories from the data
               
        save_excel: booelan
                    If True, the results will be saved also in form of excel file
                    in the same directory     
        '''        

        directory='{}\{}'.format(self.__name,directory)
        
        # Check if the shock result exist or not
        if not hasattr(self, 'X_c'):raise ValueError('To run the plot function, there should be an implemented shock.')

        # To check the input to the plot function in the aggregated level or disaggregated
        if aggregated:   VA_c,VA = self.VA_c_agg,self.VA_agg    
        else:            VA_c,VA = self.VA_c,self.VA
            
        delta_xv(VA_c,VA,style,unit,self.__m_unit,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,'VA',drop,save_excel)        
        
        
    def plot_ds(self,indicator,aggregated=True,detail=True,unit='default',
                level='Activities',kind='Absolute',fig_format='png',title_font=15,
                style='ggplot',figsize=(10, 6),directory='Charts',ranshow=(0,0)
                ,title='default',color = 'terrain', drop= None,save_excel=True):
        
        '''  
        plot_ds:
            This function is used to plot delta_S between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        indicator: string
            defines the specfic indicator to be ploted such as:
                water consumption, CO2 and ....
                
                NOTE: the indicator name should be the corresponding name of 
                the imported database
                
        aggregated  :  booelan
            True: Showing aggregated results of economic factor use
        
        detail: boolean
            True: shows different levels of the a specific indicator if
            presents in the database
            
        unit  :  string
            default: the unit will be equal the the main unit in the database
            or the user can choose the unit among the acceptable units.
             
        level :  string
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level

        kind  :  string
            Absolute: Absolute change
            Percentage: Relative change
            
        
        fig_format: string
            To save the plot
                    'png','svg'
        
        title_font: float
            size of title font
        
        style: string
            Plot style
        
        figsize: tuple
            Figure size
        
        directory: string
            the directory to save the results
        
        ranshow: tuple
            it represents the range of the values to be shown:
                    (Max value,Min value)
                    
        color: colormap:string  , colors:list 
            could be colormap or a list of colors
        
        drop: list
            To drop specific categories from the data
               
        save_excel: boolean
                    If True, the results will be saved also in form of excel file
                    in the same directory     
        '''         
        
        directory='{}\{}'.format(self.__name,directory)
        # Check if the shock result exist or not
        if not hasattr(self, 'X_c'):raise ValueError('To run the plot function, there should be an implemented shock.')

        # To check the input to the plot function in the aggregated level or disaggregated
        
        if aggregated and not detail: S_c,S = self.S_c_agg,self.S_agg 
        else: S_c,S = self.S_c,self.S
        
        delta_s(S_c,S,style,level,kind,title,ranshow,title_font,figsize,directory,fig_format,color,indicator,detail,self.__indeces,save_excel,self.__Units)        
        

    def plot_dp(self,unit='default',level=None,fig_format='png',title_font=15,
                style='ggplot',figsize=(10, 6),directory='Charts',title='default'
                ,color = 'terrain',aggregated=False,save_excel=True):
        
        '''  
        plot_dp:
            This function is used to plot change in the price ratio between the baseline and the
            last shock implemented
            
        Arguments
        ----------
        aggregated  :  
            True: Showing aggregated results of price index as the average between the aggregated invoices
             
        level :  
            None: Both Activities and Commodities will be represented
            Activities: Activities level
            Commodities: Commodities level
            
        title:
            The user can choose a specific title otherwise the default title
            will be used.
            
        fig_format: 
            To save the plot
                    'png','svg'
        
        title_font: 
            size of title font
        
        style: 
            Plot style
        
        figsize:
            Figure size
        
        directory: 
            the directory to save the results
                    
        color: 
            could be colormap or a list of colors
               
        save_excel: 
                    If True, the results will be saved also in form of excel file
                    in the same directory     
        '''          
        
        directory='{}\{}'.format(self.__name,directory)
        # Check if the shock result exist or not
        if not hasattr(self, 'X_c'):raise ValueError('To run the plot function, there should be an implemented shock.')
   
        if aggregated: 
            p_c,p = self.p_c_agg,self.p_agg, 
            print('For the aggregated results, the mean of the price of aggregated invoices are represented')
        else: p_c,p = self.p_c,self.p
        
        delta_p(p_c,p,style,level,title,title_font,figsize,directory,fig_format,color,save_excel)



    def multi_shock(self,path,Y=False,VA=False,Z=False,S=False,save=True):
        
        '''
        multi_shock:
            This function can be used to implement multiple shocks at the same time
        Arguments
        ----------
        path:
            Defines the folder in which all the shocks exist not a single shock
            excel file.
        
        Y  :  boolean
            True: Final demand shock
            
        Z  :  boolean
            True: Technical change shock
             
        VA :  boolean
            True: Economic factor change shock

        S  :  boolean
            True: Satellite account shock  
        
        save: boolean
            True: Saving the results in a dictionary. 
        
        -----------------------------------------------------------------------
        Note: It is suggested to keep "save" always "True". In this way, all the
                information can be stored and used easily.
        -----------------------------------------------------------------------
        '''       
       
        # There should be at least one shock to be implemented!
        if not Y and not VA and not Z and not S:
            raise ValueError('At lest one of the arguments should be \'True\' ')
        
        # Taking all the excel files in the given path and store the directory
        files = [f for f in glob.glob(path + "**/*.xlsx", recursive=True)]
    
        # taking all the excel files detected in loop and implement the shock    
        for i in files:
            # Calling the shock_calc for every excel file
            self.shock_calc(path=r'{}'.format(i),Y=Y,VA=VA,Z=Z,S=S,save=False)
            
            # Saving all the results in the results dictionary
            if save:
                self.results['shock_{}'.format(self.__counter)]= dict_maker(self.Z_c,self.X_c,self.VA_c,self.p_c,self.Y_c,self.va_c,
                                                    self.z_c,self.s_c,self.Z_c_agg,self.X_c_agg,self.VA_c_agg,self.Y_c_agg,self.S_c_agg,self.p_c_agg)
                self.__counter += 1
                
        print("Warning: \n all the shock variables are equal to the last sensitivity file: \'{}\' ".format(i))
        
    def sensitivity(self,path):

        
        '''
        sensitivity:
            This function can be used for sensitivity analysis on a parameter
            
        Arguments
        ----------
        path:  string
            Defines the path of an excel file, in which the shock is identified
            according to the example in the tutorial.
            
        Logic
        -----
        Accorign to the structure of the defined example for implementing a shock
        there is a sheet named 'main' in which contains all the information and
        calculations of the shock. The user needs to identifiy the parameter
        in which a senstivity analysis should be done as below:
            
            Sensitivity     = Yes 
            Min             = Minimum value
            Max             = Maximum value
            Step            = Step of every sensitivity
            Affected param  = The affected matrix [Y,VA,S,Z]
          
        After reading all the information, the function startes to build excel 
        files with the sensitivity ranges in a new folder in the same directory
        with the name of the parmeter and the value of the parmeter for every
        excel file. At the next step, in a loop, it starts to read the files 
        and impelement the shocks and stores the results in the 'results' dict.
        '''    
        
        # Given the path, sens_info is called to take all the information of
        # sensitivity such as the directory, paramaters, type of the shock and so on.
        directs,sensitivity_info = sens_info (path)
        
        i=0     # Counter for the number of sensitivities in every shock

        # For every set of sensitivities, a folder is created by the code 
        # Which contains all the whole shock related to the specific sensitivity
        
        for file in directs:
            
            # In every folder all the excels should be taken
            excels = [f for f in glob.glob(file + "**/*.xlsx", recursive=True)]
            
            # Storing the main information of the sensitivity in the results dictionary
            self.results['sensitivity_{}'.format(self.__s_counter)]={'information':sensitivity_info[str(i)]}
            
            # Check the affected matrices in every shock inserted in the excel file
            mat_list = sensitivity_info[str(i)]['matrices']
            
            # Printing the information related to the every set of sensitivities
            print('Sensitivity {}. Affected Matrices: {}'.format(i+1,mat_list))
            i+=1
            
            # Implementing all the excel files taken in the previous step for
            # every set of sensitivities
            
            for excel in excels:
                
                value_from_excel(excel)
                # Taking a copy of all matrices to have both changed and unchanged ones
                Y_c   = self.Y.copy()
                va_c  = self.va.copy()
                s_c   = self.s.copy()
                z_c   = self.z.copy()
                
                # check the type of the shock and calling the function
                if 'Y' in mat_list  : Y_c  = sh.Y_shock  (excel,Y_c.copy())                      
                if 'Z' in mat_list  : z_c  = sh.Z_shock  (excel,z_c.copy(),self.Z.copy(),self.X.copy())
                if 'VA' in mat_list : va_c = sh.VA_shock (excel,va_c.copy(),self.VA.copy(),self.X.copy())
                if 'S' in mat_list  : s_c  = sh.S_shock  (excel,s_c.copy(),self.S.copy(),self.X.copy())
                

                # Calculating the shock result
                l_c,X_c,VA_c,S_c,Z_c,p_c = cal_flows(z_c,Y_c,va_c,s_c,self.__indeces)        

                # Aggregation of the results
                X_c_agg,Y_c_agg,VA_c_agg,S_c_agg,Z_c_agg,p_c_agg = aggregate(X_c,Y_c,VA_c,S_c,Z_c,p_c)
                
                # Taking the name of excel file and removing .xlsx to use it 
                # for indexing the stored data related to sensitivities in
                # results dictionaries
                value = str(excel).replace(".xlsx","").replace('{}\case_'.format(file), "")
                
                # Storing the data in results dictionary
                self.results['sensitivity_{}'.format(self.__s_counter)][value]=\
                    dict_maker(Z_c,X_c,VA_c,p_c,Y_c,va_c,
                               z_c,s_c,Z_c_agg,X_c_agg,VA_c_agg,
                               Y_c_agg,S_c_agg,p_c_agg)
                    

            shutil.rmtree(file)
            
            self.__s_counter+=1
                                                                   
        
    def impact_assess (self,p_life,saving_sce,invest_sce,imports=['Import'],
                       w_ext=['Water'], em_ext=['CO2'], land=['Land'], 
                       labour=['Labor - Skilled','Labor - Semi Skilled','Labor - Unskilled'],
                       capital=['Capital - Machines'],save_excel=True):
        '''
        impact:
            This function can be used for the impact assessment analysis of an
            implemented policy and store the results in 'results' dict.
         
         Arguments   
        ----------
        p_life: float
            Project lifetime in terms of Years
        
        saving_sce  : list
            it represents the non-investment steps of the project
            [number of the scneario,type of scenario]
            example:
                saving_sce = [1,'se']
                
                'se': represnets that the information should be taken from sensitivites
                  1 : shows that the first sensitivity should be taken
            Note: 'se' == sensitivity , 'sh' == shock
        
        invest_sce: list
            it represents the investment steps of the project
            similar to saving_sce
            
        imports  :  list
            Represents the category of 'imports' in the imported database
             
        w_ext :  list
            Represents the category of 'water use' in the imported database

        em_ext  :  list
            Represents the category of 'emissions' in the imported database
             
        land :  list
            Represents the category of 'land' use in the imported database
            
        labour  :  list
            Represents the category of 'labour' in the imported database
             
        capital :  list
            Represents the category of 'capital' use in the imported database            
        
        
        -----------------------------------------------------------------------
        Note: To add new indicators, the user can modify the indicators
        through functions.impact.impact_assessment accoring to the function
        guide
        -----------------------------------------------------------------------
        '''
        
        if saving_sce[0] == 'sh' and invest_sce[0] == 'sh':
            directory = self.__name+'\Baseline Results'
        else:
            directory = self.__name+'\Sensitivity Results'
        
        
        # calculating the impacts using the impact_assessment function
        self.impact = impact_assessment(invest_sce,saving_sce,self.results,
                                        p_life,w_ext,em_ext,land,labour,capital,
                                        imports,directory,save_excel,self.__i_counter
                                        ,self.__m_unit,self.__Units,self.__name)
        
        # Saving the results of impcat assessment
        self.results['impact_{}'.format(self.__i_counter)]=self.impact
        self.__i_counter += 1
        
        
        
    def obj_save(cls,file_name):
        
        '''
        obj_save:
            This function can be used to save the whole object in a binary file
         
         Arguments   
        ----------
        file_name: string
            Specifies the name of the file to store the object.
        ''' 
        
        with open(file_name, 'wb') as config_dictionary_file:
            pickle.dump(cls,config_dictionary_file)
        
        
    def plot_sens(self,variable,sc_num,indicator=None,unit='default',level='Activities',
                  title='default',aggregation=True,
                  box={'color':'black','facecolor':'dodgerblue','linewidth' : 1},
                  whiskers={'color':'black','linewidth' : 1},
                  caps={'color':'black','linewidth' : 1},
                  medians={'color':'black','linewidth' : 1},
                  fliers={'marker':'o', 'color':'black', 'alpha':0.5},figsize=(9,6)
                  ,title_font=20,rational=0,directory='Charts',fig_format='png'):
        
        '''
        Parameters
        ----------
        variable : string
            Defines the variable to be plotted. ['VA','X','S']
            
        sc_num : int
            Defines the number of the specific scenario to be plotted according
            to the stored scenarios in 'results' dict.
            
        indicator : string
            Defined the name of the indicator in case of plotting S.
 
             
        unit : string, optional
            The unit of plot in the case of monetary values. The default is 
            'default' which takes the major unit.
            
        level : String, optional
            Takes the level of the plot. The default is 'Activities'.
            
        title : String, optional
            Defines the title of the graph. The default is 'default' which the
            title will be chosen by default.
            
        aggregation : boolean, optional
            Defines if the aggregated results should be plotted or disaggregated 
            results. The default is True, in which the aggregated results will
            be plotted.
            
        box : Dictionary, optional
            Defines the properties of the box in the plot. The default is 
            {'color':'black','facecolor':'dodgerblue','linewidth' : 1}.
            
        whiskers : Dictionary, optional
            Defines the properties of the whiskers in the plot. The default is
            {'color':'black','linewidth' : 1}.
        
        caps : Dictionary, optional
            Defines the properties of the caps in the plot. The default is 
            {'color':'black','linewidth' : 1}.
        
        medians : Dictionary, optional
             Defines the properties of the medians in the plot. The default is
             {'color':'black','linewidth' : 1}.
        
        fliers : Dictionary, optional
            Defines the properties of the fliers in the plot. The default is 
            {'marker':'o', 'color':'black', 'alpha':0.5}.
        
        figsize : tuple, optional
            Specifies the size of the figures. The default is (9,6).
        
        title_font : float, optional
            Defines the size of the title font. The default is 20.
       
        rational : int, optional
            Defines if the higher level of details should be plotted or the
            levels such as Activities or Commodities. Used for VA and S plots.
            The default is 0.
            
            expamle:
                1. level = 'Activities' , rational = 0 , variable=VA:
                
                        x_axis :: Activities  
                        y_axis :: Value added change
                        
                2. level = 'Activities' , rational = 1 , variable=VA:
                
                        x_axis :: detailed levels of VA  
                        y_axis :: Value added change
            fig_format: 
                To save the plot
                        'png','svg'

            
            directory: 
                the directory to save the results

                   
            save_excel: 
                        If True, the results will be saved also in form of excel file
                        in the same directory                           

        '''
        directory='{}\{}'.format(self.__name,directory)
        # Check if the given varibale is among the acceptable ones or not!
        variable = var_check(variable)
        
        # Reshaping the data and index to plot
        data,index,title,legend,unit = sensitivity_take(variable,sc_num,self.results,aggregation,level,indicator,self.__m_unit,unit,title,rational,self.__indeces)

        ptl_sensitivity(data,index,title,box,whiskers,caps,medians,fliers,figsize,legend,unit,title_font,directory,fig_format)
        
    

    def get_excel_shock(self,num_index=30):
        sh_excel(num_index,self.__indeces)
  