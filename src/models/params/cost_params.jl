"""
Parameter Module
Cost and prices.

Pengfei Cheng
2022

UPDATE:
    04-17-2022: moved start-up cost to model.jl to allow update.
"""

using DataFrames
using CSV

# CO2 transportation price, USD/tonne CO2
global a_cost_CO2_TS = 10

# interest rate, for NPV calculation
global int_r = 0.0294

# depreciation rate, for NPV calculation
global depreciate_r = 0.075

# tax rate, for NPV calculation
global tax_r = 0.2574

# VOMs
# NGCC, $/load factor
global a_VOM_NGCC = 8751461 / 0.85 / 24 / 365 / 100
# PCC, $/load factor
global a_VOM_PCC = 18527935 / 24 / 365 / 100
# DAC, $/tonne CO2 captured
global a_cost_DAC_VOM = 9
# PCC compressor, $/load factor
global a_cost_PCC_compr_VOM = 1745198 / 24 / 365 / 100
# DAC compressor, $/tonne CO2 captured
global a_cost_DAC_compr_VOM = 861964 / 24 / 365 / 140