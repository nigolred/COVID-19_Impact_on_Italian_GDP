# Meso-Economic model for allocating sectoral GDP

## Description
This step of the work is taking advantage of REP_CVX, a python module developed by REP research group in Fondazione Eni Enrico Mattei with the aim to provide an open-source tool for performing **Input-Output** analysis based on the **Supply and Use Framework**. The approach is therefore grounded on the use of Supply and Use Framework as described by Lenzen and Rueda-Cantuche in _A note on the use of supply-use tables in impact analyses_.
The repository is complementing what is described in the paper _A multi-disciplinary approach to estimate the medium-term impact of COVID-19 on the energy system: a case study for Italy_ for what concerns the meso-economic modelling. The repository is organised in the following way:

    *Database: in this folder the EUROSTAT Supply and Use Table (SUT) for Italy are reported in row format (in 'Database/EUROSTAT' where also the consumption_trend.py module for extrapolating trends in final demand shares on the basis of 2010-2016 values) and CVX_SUT format (the excel files in 'Database' for 2014, 2015 and 2016 which are used for feeding the Leontief Kantorovich optimiztion model) are present. In this folder on can also find the Aggregation.xlsx file, which can be used for aggregating the results on the basis of any aggregation choice. Here two aggregation are used for presenting results, one based on the sectors adopted in the Energy Model (Integration), one for analysing the results (Analysis).
    *Results: in this folder the results are stored. Each run generates 4 htlm charts and 1 excel files. For each aggregation a dedicated folder can be found.
    *Inputs: in this folder an excel file for managing the non-database exogenous parameters for the Leontief model is present. In the README sheet a detailed presentation of the sheets is presented.
    *REP_CVX: in this folder the module for managing input-output model can be found. A dedicated readme can be found in the folder.
    *Visualizing results and generating reports
