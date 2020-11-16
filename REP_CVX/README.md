# REP_CVX
**R**esearch **E**mpowerment **P**artnership **C**omprehens**IV**e & **I**ntegrated **C**ountry **S**tudy

---
## Description
REP_CVX is a python module developed by REP research group in Fondazione Eni Enrico Mattei for CIVICS Kenya Project with to aim to provide an open-source tool for performing **Input-Output** analysis based on the **Supply and Use Framework**.

The module uses excel files as the input data and the outputs are in form of plots, excel files and binary files.

Main features:

    *Performing the Input-Output Calculations based on the supply and use framework
    *Shock implementation
    *Sensitivity Analysis on every specific shock implementation
    *Policy impact assessment
    *Visualizing results and generating reports
    
    
    
---
### Where to find it
The full source code is available on **[Our Github](https://github.com/FEEM-Africa-REP/CIVICS_Kenya)**:

To use the code, copy it in your site-packages directory: 

    e.g. anaconda3\Lib\site-packages
    
 ---
 ### Quickstart
 ##### Note:
 
 4 examples of the kenya study (refer to paper) are provided in (link bede be file tuye github).
 
To Use it:
#### Reading the database
``` python
import REP_CVX 

case = REP_CVX.C_SUT(path='Path of your Supply and Use Table according to the structure',unit='Representing the unit of measure of the monetary values of the table')
```
#### Implementing a shock: Investment Shock (implemneted on final demand matrix(Y))
``` python

case.shock_calc(path='path of the excel file which defines the shock',Y=True)
```
#### Implementing a shock: Saving Shock (implemneted shocks on technical coefficient matrix(Z),Value added matrix (VA) and satellite account matrix (S))
``` python
case.shock_calc(path='path of the excel file which defines the shock',Z=True,VA=True,S=True)
```
#### Assessing the policy impact 
``` python
case.impact_assess(p_life = 'the project life time',
                   imports=['Import'],
                   w_ext=['Water'], em_ext=['CO2'], land=['Land'], 
                   labour=['Labor - Skilled','Labor - Semi Skilled','Labor - Unskilled'],
                   capital=['Capital - Machines'])

# p_life:  Project lifetime
# imports: Categories of imports in the database
# w_ext:   Categories of Water in the database     (aggregated)
# em_ext:  Categories of emissions in the database (aggregated)
# land:    Categoreis of land in the database      (aggregated)
# labour:  Categories of labour in the database    (aggregated)
# capital: Categories of capital in the database   (aggregated)
```

#### Performing the sensitivity analysis
``` python
case.sensitivity(path='path of the excel file which defines the shock')
```
#### Plotting the sensitivity results
``` python
case.plot_sens(variable='Defines the parameter to be plotted',sc_num='Defines the sensitivity scenario to be plotted')

#variable =
   #'X':  Production 
   #'VA': Value Added
   #'S':  Satellite Account
 ```  
#### Plotting the the changes of a shock and the baseline
``` python
case.plot_dx()             # Plotting the change in the production
case.plot_dv()             # Plotting the change in the value added
case.plot_ds(indicator)    # Plotting the change in the environmental extensions
```
#### Looking at the resuts: All the results are saved in a dictionary named results
``` python
results = case.results
```
#### How to build the shock file? 
``` python
case.get_excel_shock()
# This function provides and excel file which is build based on the imported databsae and the structure of the code:
# Sheets: 
   # 1. main: it contains all the calculation related to the policy which the sensitivity on a specific parameter can be identified too
   # 2. Y: it stores the information of a shock on Y matrix
   # 3. Z: it stores the information of a shock on Z matrix
   # 4. S: it stores the information of a shock on S matrix
   # 5. VA: it stores the information of a shock on VA matrix
```
 
