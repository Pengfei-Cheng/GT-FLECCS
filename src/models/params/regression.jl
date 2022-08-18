"""
Parameter Module
Import regression results.

Pengfei Cheng
2022

# TODO check if b values are necessary

UPDATE:
    02-02-2022: added a_power_LP_steam, source: regression.ipynb
    03-30-2022: commented out "pieces".
"""

using DataFrames
using CSV

# # the discrete points in each pieces
# pieces = Dict(
#     1 => [1, 0.9, 0.8, 0.7, 0.6],
#     2 => [0.6, 0.5],
#     3 => [0.5, 0.4, 0.3],
#     4 => [0.3, 0.25]
# )

# read CSV files
df_coef = DataFrame(CSV.File("src/regression/coefs.csv"))

# fuel input rate coefficients, MW
df = filter(row -> row.y == "GT_power", df_coef)
df_a_power_GT = df[:, 2] / 1000
df_b_power_GT = df[:, 3] / 1000
# natural gas consumption coefficients, MMBtu/hr
df = filter(row -> row.y == "fuel", df_coef)
df_a_fuel = df[:, 2]
df_b_fuel = df[:, 3]
# CO2 emission, tonne CO2/hr
df = filter(row -> row.y == "CO2_emission", df_coef)
df_a_emission = df[:, 2] 
df_b_emission = df[:, 3]
# HP steam turbine power coefficients, MW
df = filter(row -> row.y == "HP_power", df_coef)
df_a_power_HP = df[:, 2] / 1000  # 1000 to scale the kW to MW
df_b_power_HP = df[:, 3] / 1000
# IP steam turbine power coefficients, MW
df = filter(row -> row.y == "IP_power", df_coef)
df_a_power_IP = df[:, 2] / 1000
df_b_power_IP = df[:, 3] / 1000
# # LP steam turbine power coefficients, MW
# df = filter(row -> row.y == "LP_power", df_coef)
# a_power_LP = df[:, 2] / 1000
# b_power_LP = df[:, 3] / 1000
# auxiliary power coefficients, MW
df = filter(row -> row.y == "auxiliary_power", df_coef)
df_a_aux_power = df[:, 2] / 1000
df_b_aux_power = df[:, 3] / 1000
# base PCC steam/PCC reboiler duty coefficients, MMBtu/hr
df = filter(row -> row.y == "PCC_reboiler_duty", df_coef)
df_a_PCC_reboiler_duty = df[:, 2]
df_b_PCC_reboiler_duty = df[:, 3]
# base DAC steam duty, from "Max Power" spreadsheet, MMBtu/hr
df = filter(row -> row.y == "DAC_base_steam_duty", df_coef)
df_a_DAC_base_steam = df[:, 2]
df_b_DAC_base_steam = df[:, 3]
# side steam (the difference between "Max DAC" and "Max Power")/additional
# energy for the DAC steam generation unit coefficients, MMBtu/hr
df = filter(row -> row.y == "DAC_side_steam_duty", df_coef)
df_a_allocable_steam = df[:, 2]
df_b_allocable_steam = df[:, 3]

# --------------------------------------------------------------------------

# fuel input rate coefficients, MW
global a_power_GT = df_a_power_GT[1]
global b_power_GT = df_b_power_GT[1]
# natural gas consumption coefficients, MMBtu/hr
global a_fuel = df_a_fuel[1]
global b_fuel = df_b_fuel[1]
# CO2 emission, tonne CO2/hr
global a_emission = df_a_emission[1]
global b_emission = df_b_emission[1]
# HP steam turbine power coefficients, MW
global a_power_HP = df_a_power_HP[1]
global b_power_HP = df_b_power_HP[1]
# IP steam turbine power coefficients, MW
global a_power_IP = df_a_power_IP[1]
global b_power_IP = df_b_power_IP[1]
# # LP steam turbine power coefficients, MW
# a_power_LP = a_power_LP[1]
# b_power_LP = b_power_LP[1]
# auxiliary power coefficients, MW
global a_aux_power = df_a_aux_power[1]
global b_aux_power = df_b_aux_power[1]
# base PCC steam/PCC reboiler duty coefficients
global a_PCC_reboiler_duty = df_a_PCC_reboiler_duty[1]
global b_PCC_reboiler_duty = df_b_PCC_reboiler_duty[1]
# base DAC steam duty, from "Max Power" spreadsheet, MMBtu/hr
global a_DAC_base_steam = df_a_DAC_base_steam[1]
global b_DAC_base_steam = df_b_DAC_base_steam[1]
# side steam (the difference between "Max DAC" and "Max Power")/additional
# energy for the DAC steam generation unit coefficients
global a_allocable_steam = df_a_allocable_steam[1]
global b_allocable_steam = df_b_allocable_steam[1]

# ratio of power generated from LP steam turbine by steam amount, MW / (MMBtu/hr)
global a_power_LP_steam = 0.09062