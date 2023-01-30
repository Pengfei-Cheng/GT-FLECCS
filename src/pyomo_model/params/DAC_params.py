"""
Parameter Module
DAC-related parameters.

Pengfei Cheng
2023
"""

# volume ratio of CO2 in air
CO2_vol_ratio = 0.000415

# molecular weight, g/mol
CO2_mole_w = 44.0095

# mole volume, m^3/mol
mole_vol = 0.0224

# unit conversion
lb_to_tonne = 0.4535924 / 1000
MMBTu_to_kWh = 293.07
kWh_to_MMBtu = 1 / MMBTu_to_kWh
GJ_to_kWh = 277.778
tonne_to_g = 1e6

# steam requirement for DAC capture to CO2 ratio
# 7 GJ/tonne CO2 for regeneration (from Matthew Realff)
base_DAC_coef = 7
a_steam_DAC = base_DAC_coef * GJ_to_kWh * kWh_to_MMBtu

# power consumption of DAC units, 0.25 MW/tonne CO2
a_power_DAC = 0.25

# mass-base sorbent capacity (per mass of sorbent), g CO2/g sorbent
# mole-bass: 0.8 mol CO2/kg sorbent (/cycle), from Matthew Realff
sorbent_cap = 0.8 * 1e-3 * CO2_mole_w
# captured CO2 mass per mass of sorbent for DAC-air, g CO2/g Sorbent
sorbent_cap_DAC_air = sorbent_cap

# new parameters
# contactor capital cost coefficient, $/tonne sorbent
a_cost_sorbent = 72.72 * 1000
# capital cost coefficient for adsorption system (blower/pump), $/(m^3/s)
a_cost_adsorb = 491.04