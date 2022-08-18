"""
Parameter Module
DAC-related parameters.

Pengfei Cheng
2022

UPDATE:
    01-18-2022: capacity updated from 1 mmol CO2/g sorbent to 0.8 mol CO2/kg
        sorbent (/cycle).
    12-09-2021: x_sorbent_m_DAC_FG and x_sorbent_m were modeled as
        variables.
    01-18-2022: added data from Hannah Holmes: a_contactor, a_adsorb_sys; assign
        a small value to a_desorb_sys.
    04-03-2022: removed the coefficients (2) for the DAC steam usage.
    04-12-2022: removed the coefficients (2) for the DAC power usage.
    06-03-2022: add coefficient (0.5) for a_DAC_air_power as it is used for
        every 15-min calculation.
    07-29-2022: remove 0.5 coefficient from a_DAC_air_power: the coefficient
        is added into the constraint.
"""

# volume ratio of CO2 in air
global CO2_vol_ratio = 0.000415
# volume ratio of CO2 in flue gas
global CO2_vol_ratio_FG = 0.000415 * 2

# molecular weight, g/mol
global CO2_mole_w = 44.0095

# mole volume, m^3/mol
global mole_vol = 0.0224

# unit conversion
global lb_to_tonne = 0.4535924 / 1000
global MMBTu_to_kWh = 293.07
global kWh_to_MMBtu = 1 / MMBTu_to_kWh
global GJ_to_kWh = 277.778
global tonne_to_g = 1e6

# steam requirement for DAC capture to CO2 ratio
# 7 GJ/tonne CO2 for regeneration (from Matthew Realff)
global base_DAC_coef = 7
global a_DAC_air_steam = base_DAC_coef * GJ_to_kWh * kWh_to_MMBtu
global a_DAC_FG_steam = base_DAC_coef * GJ_to_kWh * kWh_to_MMBtu

# power consumption of DAC units, 0.25 MW/tonne CO2
global a_DAC_air_power = 0.25
global a_DAC_FG_power = 0.25

# mass-base sorbent capacity (per mass of sorbent), g CO2/g sorbent
# mole-bass: 0.8 mol CO2/kg sorbent (/cycle), from Matthew Realff
global sorbent_cap = 0.8 * 1e-3 * CO2_mole_w
# captured CO2 mass per mass of sorbent for DAC-FG, g CO2/g Sorbent
global sorbent_cap_DAC_FG = 1 * sorbent_cap
# captured CO2 mass per mass of sorbent for DAC-air, g CO2/g Sorbent
global sorbent_cap_DAC_air = sorbent_cap

# new parameters
# contactor capital cost coefficient, $/tonne sorbent
global a_contactor = 72.72 * 1000
# capital cost coefficient for adsorption system (blower/pump), $/(m^3/s)
global a_adsorb_sys = 491.04