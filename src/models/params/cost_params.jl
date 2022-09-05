"""
Parameter Module
Cost and prices.

Pengfei Cheng
2022
"""

# interest rate, for NPV calculation
global int_r = 0.0294

# depreciation rate, for NPV calculation
global depreciate_r = 0.075

# tax rate, for NPV calculation
global tax_r = 0.2574

# VOMs
# NGCC, $/load factor
# 1.70517 is for $/MWh
global a_cost_NGCC_VOM = 1.70517 * 727 / 100