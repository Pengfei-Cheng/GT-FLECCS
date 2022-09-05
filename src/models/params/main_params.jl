"""
Parameter Module
Main Parameters.

Pengfei Cheng
2022
"""

using DataFrames
using CSV

# fuel input rate coefficients, MW/load factor
global a_power_GT = 477 / 100
# natural gas consumption coefficients, MMBtu/load factor
global a_fuel = 6.363 * 727 / 100
# CO2 emission, tonne CO2/load factor
global a_CO2_flue = 0.336 * 740 / 100
# total steam turbine power coefficients, MW/load factor
global a_power_ST = 263 / 100
# auxiliary power coefficients, MW/load factor
global a_power_aux = 14 / 100
