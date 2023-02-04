"""
Parameter Module
Import regression results.

Pengfei Cheng
2023
"""

import pandas as pd
from pathlib import Path

# read CSV files
script_path = Path(__file__, '../../..').resolve()
df_coef = pd.read_csv(str(script_path.joinpath('regression/coefs.csv')))

# fuel input rate coefficients, MW
tmp_df = df_coef[df_coef["y"] == "GT_power"].iloc[0]
a_power_GT = tmp_df["a"] / 1000
b_power_GT = tmp_df["b"] / 1000
# natural gas consumption coefficients, MMBtu/hr
tmp_df = df_coef[df_coef["y"] == "fuel"].iloc[0]
a_fuel = tmp_df["a"]
b_fuel = tmp_df["b"]
# CO2 emission, tonne CO2/hr
tmp_df = df_coef[df_coef["y"] == "CO2_flue_gas"].iloc[0]
a_CO2_flue = tmp_df["a"]
b_CO2_flue = tmp_df["b"]
# HP steam turbine power coefficients, MW
tmp_df = df_coef[df_coef["y"] == "HP_power"].iloc[0]
a_power_HP = tmp_df["a"] / 1000
b_power_HP = tmp_df["b"] / 1000
# IP steam turbine power coefficients, MW
tmp_df = df_coef[df_coef["y"] == "IP_power"].iloc[0]
a_power_IP = tmp_df["a"] / 1000
b_power_IP = tmp_df["b"] / 1000
# auxiliary power coefficients, MW
tmp_df = df_coef[df_coef["y"] == "auxiliary_load"].iloc[0]
a_power_aux = tmp_df["a"] / 1000
b_power_aux = tmp_df["b"] / 1000
# base DAC steam, MMBtu/hr
tmp_df = df_coef[df_coef["y"] == "DAC_base_steam"].iloc[0]
a_steam_DAC_base = tmp_df["a"]
b_steam_DAC_base = tmp_df["b"]
# allocable steam, MMBtu/hr
tmp_df = df_coef[df_coef["y"] == "allocable_steam"].iloc[0]
a_steam_alloc = tmp_df["a"]
b_steam_alloc = tmp_df["b"]

# ratio of power generated from LP steam turbine by steam amount, MW / (MMBtu/hr)
a_power_LP = 0.09062