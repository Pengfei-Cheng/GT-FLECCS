"""
Modeling module
Declare disaggregated variable constraints.

Pengfei Cheng

1.  convex combination of lam = x_load_D (at dispatch mode)
2.  load factor during start-up
3.  load big-M

4.  fuel rate at dispatch mode
5.  fuel rate at start-up

6.  CO2 emission rate at dispatch mode
7.  CO2 emission rate at start-up

8.  constraints for other disaggregated variables at each mode (8)
        HP steam turbine power  IP steam turbine power
        DAC base steam          allocable steam
"""

from pyomo.environ import Constraint
from ..params import *


def add_disaggregated_constraints(m, set_hour_0, set_scenario):

    # 1. CONVEX COMBINATION OF lam = X_LOAD_FACTOR_D (AT DISPATCH MODE)
    #    load factor is a convex combination of extreme points
    def eq_lam_load(m, i, s):
        return sum(m.lam[i, k, s] * x_range[k] for k in x_range_extreme_points) == m.x_load_D[i, dispatch_idx, s]
    m.eq_lam_load = Constraint(set_hour_0, set_scenario, rule=eq_lam_load)

    # --------------------------------------------------------------------------

    # 2. LOAD DURING START-UP
    def eq_load_start_up(m, i, s):
        return m.x_load_D[i, start_up_idx, s] == sum((m.z0[i - k + 1, s]) * load_trajectory[k] for k in set_start_up_hour if i - k + 1>= 0)
    m.eq_load_start_up = Constraint(set_hour_0, set_scenario, rule=eq_load_start_up)

    # --------------------------------------------------------------------------

    # 3. LOAD BIG-M
    # for both modes, x_load_D = 0 when y = 0
    def eq_off_mode_load(m, i, j, s):
        return m.x_load_D[i, j, s] <= 100 * m.y[i, s]
    m.eq_off_mode_load = Constraint(set_hour_0, set_mode, set_scenario, rule=eq_off_mode_load)

    # --------------------------------------------------------------------------

    # 4. FUEL RATE AT DISPATCH MODE
    def eq_fuel_dispatch(m, i, s):
        return m.x_fuel_D[i, dispatch_idx, s] == a_fuel * m.x_load_D[i, dispatch_idx, s] + b_fuel * (m.y[i, s] - m.z[i, s])
    m.eq_fuel_dispatch = Constraint(set_hour_0, set_scenario, rule=eq_fuel_dispatch)

    # --------------------------------------------------------------------------

    # 5. FUEL RATE AT START-UP
    def eq_fuel_start_up(m, i, s):
        return m.x_fuel_D[i, start_up_idx, s] == 0
    m.eq_fuel_start_up = Constraint(set_hour_0, set_scenario, rule=eq_fuel_start_up)

    # --------------------------------------------------------------------------

    # 6. CO2 EMISSION RATE AT DISPATCH MODE
    def eq_emission_dispatch(m, i, s):
        return m.x_CO2_D_flue[i, dispatch_idx, s] == a_CO2_flue * m.x_load_D[i, dispatch_idx, s] + b_CO2_flue * (m.y[i, s] - m.z[i, s])
    m.eq_emission_dispatch = Constraint(set_hour_0, set_scenario, rule=eq_emission_dispatch)

    # --------------------------------------------------------------------------

    # 7. CO2 EMISSION RATE AT START-UP
    def eq_emission_start_up(m, i, s):
        return m.x_CO2_D_flue[i, start_up_idx, s] == 0
    m.eq_emission_start_up = Constraint(set_hour_0, set_scenario, rule=eq_emission_start_up)

    # --------------------------------------------------------------------------

    # 13. CONSTRAINTS FOR OTHER DISJUNCTIVE VARIABLES AT EACH MODE

    # HP steam turbine power
    def eq_power_HP_dispatch(m, i, s):
        return m.x_power_D_HP[i, dispatch_idx, s] == a_power_HP * m.x_load_D[i, dispatch_idx, s] + b_power_HP * (m.y[i, s] - m.z[i, s])
    m.eq_power_HP_dispatch = Constraint(set_hour_0, set_scenario, rule=eq_power_HP_dispatch)

    def eq_power_HP_start_up(m, i, s):
        return m.x_power_D_HP[i, start_up_idx, s] == 0
    m.eq_power_HP_start_up = Constraint(set_hour_0, set_scenario, rule=eq_power_HP_start_up)

    # IP steam turbine power
    def eq_power_IP_dispatch(m, i, s):
        return m.x_power_D_IP[i,dispatch_idx, s] == a_power_IP * m.x_load_D[i,dispatch_idx, s] + b_power_IP * (m.y[i, s]-m.z[i, s])
    m.eq_power_IP_dispatch = Constraint(set_hour_0, set_scenario, rule=eq_power_IP_dispatch)
    def eq_power_IP_start_up(m, i, s):
        return m.x_power_D_IP[i,start_up_idx, s] == 0
    m.eq_power_IP_start_up = Constraint(set_hour_0, set_scenario, rule=eq_power_IP_start_up)


    # DAC base steam
    def eq_DAC_base_steam_dispatch(m, i, s):
        return m.x_steam_D_DAC_base[i,dispatch_idx, s] == a_steam_DAC_base * m.x_load_D[i,dispatch_idx, s] + b_steam_DAC_base * (m.y[i, s] - m.z[i, s])
    m.eq_DAC_base_steam_dispatch = Constraint(set_hour_0, set_scenario, rule=eq_DAC_base_steam_dispatch)
    def eq_DAC_base_steam_start_up(m, i, s):
        return m.x_steam_D_DAC_base[i,start_up_idx, s] == 0
    m.eq_DAC_base_steam_start_up = Constraint(set_hour_0, set_scenario, rule=eq_DAC_base_steam_start_up)


    # allocable steam
    def eq_allocable_steam_dispatch(m, i, s):
        return m.x_steam_D_allocable[i,dispatch_idx, s] == a_steam_alloc * m.x_load_D[i,dispatch_idx, s] + b_steam_alloc * (m.y[i, s] - m.z[i, s])
    m.eq_allocable_steam_dispatch = Constraint(set_hour_0, set_scenario, rule=eq_allocable_steam_dispatch)
    def eq_allocable_steam_start_up(m, i, s):
        return m.x_steam_D_allocable[i,start_up_idx, s] == 0
    m.eq_allocable_steam_start_up = Constraint(set_hour_0, set_scenario, rule=eq_allocable_steam_start_up)


    # auxiliary power
    def eq_auxiliary_power_dispatch(m, i, s):
        return m.x_power_D_aux[i,dispatch_idx, s] == a_power_aux * m.x_load_D[i,dispatch_idx, s] + b_power_aux * (m.y[i, s] - m.z[i, s])
    m.eq_auxiliary_power_dispatch = Constraint(set_hour_0, set_scenario, rule=eq_auxiliary_power_dispatch)
    def eq_auxiliary_power_start_up(m, i, s):
        return m.x_power_D_aux[i,start_up_idx, s] == 0
    m.eq_auxiliary_power_start_up = Constraint(set_hour_0, set_scenario, rule=eq_auxiliary_power_start_up)


    return