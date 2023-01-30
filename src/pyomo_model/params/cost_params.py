"""
Parameter Module
Cost and prices.

Pengfei Cheng
2023

UPDATE:
    04-17-2022: moved start-up cost to the main model module to allow update.
"""

# CO2 transportation price, USD/tonne CO2
a_cost_CO2_TS = 10

# interest rate, for NPV calculation
int_r = 0.0294

# depreciation rate, for NPV calculation
depreciate_r = 0.075

# tax rate, for NPV calculation
tax_r = 0.2574

# VOMs
# NGCC, $/load factor
a_cost_NGCC_VOM = 8751461 / 0.85 / 24 / 365 / 100
# PCC, $/load factor
a_cost_PCC_VOM = 18527935 / 24 / 365 / 100
# DAC, $/tonne CO2 captured
a_cost_DAC_VOM = 9
# PCC compressor, $/load factor
a_cost_PCC_compr_VOM = 1745198 / 24 / 365 / 100
# DAC compressor, $/tonne CO2 captured
a_cost_DAC_compr_VOM = 861964 / 24 / 365 / 140