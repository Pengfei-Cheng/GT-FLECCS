"""
Parameter Module
Import regression results.

Pengfei Cheng
2022
"""

using DataFrames
using CSV

# read CSV files
df_coef = DataFrame(CSV.File("src/regression/coefs.csv"))

# fuel input rate coefficients, MW
df = filter(row -> row.y == "GT_power", df_coef)
global a_power_GT = df[1, "a"] / 1000
global b_power_GT = df[1, "b"] / 1000
# natural gas consumption coefficients, MMBtu/hr
df = filter(row -> row.y == "fuel", df_coef)
global a_fuel = df[1, "a"]
global b_fuel = df[1, "b"]
# CO2 emission, tonne CO2/hr
df = filter(row -> row.y == "CO2_flue_gas", df_coef)
global a_CO2_flue = df[1, "a"]
global b_CO2_flue = df[1, "b"]
# HP steam turbine power coefficients, MW
df = filter(row -> row.y == "HP_power", df_coef)
global a_power_HP = df[1, "a"] / 1000
global b_power_HP = df[1, "b"] / 1000
# IP steam turbine power coefficients, MW
df = filter(row -> row.y == "IP_power", df_coef)
global a_power_IP = df[1, "a"] / 1000
global b_power_IP = df[1, "b"] / 1000
# auxiliary power coefficients, MW
df = filter(row -> row.y == "auxiliary_load", df_coef)
global a_power_aux = df[1, "a"] / 1000
global b_power_aux = df[1, "b"] / 1000
# base DAC steam, MMBtu/hr
df = filter(row -> row.y == "DAC_base_steam", df_coef)
global a_steam_DAC_base = df[1, "a"]
global b_steam_DAC_base = df[1, "b"]
# allocable steam, MMBtu/hr
df = filter(row -> row.y == "allocable_steam", df_coef)
global a_steam_alloc = df[1, "a"]
global b_steam_alloc = df[1, "b"]

# ratio of power generated from LP steam turbine by steam amount, MW / (MMBtu/hr)
global a_power_LP = 0.09062