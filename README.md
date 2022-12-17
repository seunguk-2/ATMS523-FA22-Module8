# ATMS523-FA22-Module8

SeungUk Kim

### Introduction

This module for ATMS 523 Fall 2022 applies various machine learning technique to investigate the selected problem in the Midwest, droughts. Regarding the atmospheric moisture budget equation, vertically integrated divergence of moisture flux (VIDMF) can determine the amount of precipitation minus evapotranspiration (P-E). The anomalous and persistent low P-E can lead to drought. The idea is to predict VIDMF with information of soil moisture (SM) and evapotranspiration (ET) anomalies in the upwind areas.
Preliminary results from the two-layer dynamic recycling model (2L-DRM) give information of daily back trajectories of air parcels in the Midwest for 41 years. With this, obtain daily SM and ET anomalies of the upwind for ten days during the warm season (April - September). We will use these SM and ET as predictor to estimate target variable (VIDMF) with various machine learning models. Starting with Linear Regression, Random Forest, and Neural Network will be applied to obtain the best model in this module.

### Data
Data used in this module is based on hourly ERA5[(DOI: 10.24381/cds.adbb2d47)](10.24381/cds.adbb2d47), including hourly soil moisture and evaptranspiration. Back-trajectory data from 2L-DRM is available on the department server keeling under `/data/keeling/a/seunguk2/c/2LDRM/pydlmb/`. Produced with these data is `trj_sm_pp.nc` which includes averaged daily SM and ET anomalies in the upwind area for ten days. Daily averaged hourly VIDMF is also obtained from [ERA5](10.24381/cds.adbb2d47) and averaged over the Midwest then stored in `vidmf_mwc.nc`.Processing of the data mentioned here are done with the given codes: `trj_smpp.py` and `functions.py`.

### Tested Machine Learning Models
1. Linear Regression
2. Linear Regression w/ pre-processed data
3. Linear Regression w/ additional pre-processing
4. Random Forest
5. Neural Network

### Summary
**No single machine learning model could properly predict VIDMF with upwind SM and ET anomalies.**