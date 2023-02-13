"""
Modeling module
Declare overall variable constraints (as sum of unit variables).

Pengfei Cheng

1. constraints for overall variables (8)
        load factor             fuel rate               CO2 emission rate
        HP steam turbine power  IP steam turbine power  DAC base steam
        allocable steam
"""

from pyomo.environ import Constraint
from ..params import *


def add_overall_var_constraints(m, set_hour_0, set_scenario):

    # 1. CONSTRAINTS FOR OVERALL VARIABLES

    # load factor
    def eq_total_load_factor(m, i, s):
        return m.x_load[i, s] == sum(m.x_load_D[i, mode, s] for mode in set_mode)
    m.eq_total_load_factor = Constraint(set_hour_0, set_scenario, rule=eq_total_load_factor)

    # fuel consumption
    def eq_total_fuel_rate(m, i, s):
        return m.x_fuel[i, s] == sum(m.x_fuel_D[i, mode, s] for mode in set_mode)
    m.eq_total_fuel_rate = Constraint(set_hour_0, set_scenario, rule=eq_total_fuel_rate)

    # CO2 emission rate
    def eq_total_CO2_emission_rate(m, i, s):
        return m.x_CO2_flue[i, s] == sum(m.x_CO2_D_flue[i, mode, s] for mode in set_mode)
    m.eq_total_CO2_emission_rate = Constraint(set_hour_0, set_scenario, rule=eq_total_CO2_emission_rate)

    # HP steam turbine power
    def eq_total_power_HP(m, i, s):
        return m.x_power_HP[i, s] == sum(m.x_power_D_HP[i, mode, s] for mode in set_mode)
    m.eq_total_power_HP = Constraint(set_hour_0, set_scenario, rule=eq_total_power_HP)

    # IP steam turbine power
    def eq_total_power_IP(m, i, s):
        return m.x_power_IP[i, s] == sum(m.x_power_D_IP[i, mode, s] for mode in set_mode)
    m.eq_total_power_IP = Constraint(set_hour_0, set_scenario, rule=eq_total_power_IP)

    # DAC base steam
    def eq_total_DAC_base_duty(m, i, s):
        return m.x_steam_DAC_base[i, s] == sum(m.x_steam_D_DAC_base[i, mode, s] for mode in set_mode)
    m.eq_total_DAC_base_duty = Constraint(set_hour_0, set_scenario, rule=eq_total_DAC_base_duty)

    # allocable steam
    def eq_total_steam_allocable(m, i, s):
        return m.x_steam_allocable[i, s] == sum(m.x_steam_D_allocable[i, mode, s] for mode in set_mode)
    m.eq_total_steam_allocable = Constraint(set_hour_0, set_scenario, rule=eq_total_steam_allocable)

    # auxiliary power
    def eq_total_power_aux(m, i, s):
        return m.x_power_aux[i, s] == sum(m.x_power_D_aux[i, mode, s] for mode in set_mode)
    m.eq_total_power_aux = Constraint(set_hour_0, set_scenario, rule=eq_total_power_aux)

    return