"""
Modeling module
Declare PCC-related constraints.

Pengfei Cheng

1. PCC CO2 capture
2. PCC CO2 outlet concentration
3. PCC steam usage
4. PCC power usage
"""

from pyomo.environ import Constraint
from ..params import *


def add_PCC_constraints(m, set_hour_0, set_scenario):

    # 1. PCC CO2 CAPTURE
    def eq_PCC_CO2_cap(m, i, s):
        return m.x_CO2_PCC[i, s] == a_CO2_PCC * m.x_CO2_flue[i, s]
    m.eq_PCC_CO2_cap = Constraint(set_hour_0, set_scenario, rule=eq_PCC_CO2_cap)

    # --------------------------------------------------------------------------

    # 2. PCC CO2 OUTLET CONCENTRATION
    def eq_PCC_CO2_out(m, i, s):
        return m.x_CO2_vent_PCC[i, s] == m.x_CO2_flue[i, s] - m.x_CO2_PCC[i, s]
    m.eq_PCC_CO2_out = Constraint(set_hour_0, set_scenario, rule=eq_PCC_CO2_out)

    # --------------------------------------------------------------------------

    # 3. PCC STEAM USAGE
    def eq_PCC_steam(m, i, s):
        return m.x_steam_PCC[i, s] == a_steam_PCC * m.x_CO2_PCC[i, s]
    m.eq_PCC_steam = Constraint(set_hour_0, set_scenario, rule=eq_PCC_steam)

    # --------------------------------------------------------------------------

    # 4. PCC POWER USAGE
    def eq_PCC_power(m, i, s):
        return m.x_power_PCC[i, s] == a_power_PCC * m.x_CO2_PCC[i, s]
    m.eq_PCC_power = Constraint(set_hour_0, set_scenario, rule=eq_PCC_power)

    return