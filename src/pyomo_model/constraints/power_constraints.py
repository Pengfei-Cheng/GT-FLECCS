"""
Modeling module
Declare power-related constraints.

Pengfei Cheng

1. power from LP steam turbine
2. total power from all steam turbines
3. total power generation
4. GT power
5. net power output
"""

from pyomo.environ import Constraint
from ..params import *


def add_power_constraints(m, set_hour_0, set_scenario):

    # 1. POWER FROM LP STEAM TURBINE
    def eq_power_LP(m, i, s):
        return m.x_power_LP[i, s] == m.x_steam_LP[i, s] * a_power_LP
    m.eq_power_LP = Constraint(set_hour_0, set_scenario, rule=eq_power_LP)

    # --------------------------------------------------------------------------

    # 2. TOTAL POWER FROM ALL STEAM TURBINES
    def eq_total_power_ST(m, i, s):
        return m.x_power_ST[i, s] == m.x_power_HP[i, s] + m.x_power_IP[i, s] + m.x_power_LP[i, s]
    m.eq_total_power_ST = Constraint(set_hour_0, set_scenario, rule=eq_total_power_ST)

    # --------------------------------------------------------------------------

    # 3. TOTAL POWER GENERATION
    def eq_power_total(m, i, s):
        return m.x_power_total[i, s] == m.x_power_GT[i, s] + m.x_power_ST[i, s]
    m.eq_power_total = Constraint(set_hour_0, set_scenario, rule=eq_power_total)

    # --------------------------------------------------------------------------

    # 4. GT POWER
    def eq_total_power_GT(m, i, s):
        return m.x_power_GT[i, s] == a_power_GT * m.x_load[i, s] + b_power_GT * m.y[i, s]
    m.eq_total_power_GT = Constraint(set_hour_0, set_scenario, rule=eq_total_power_GT)

    # --------------------------------------------------------------------------

    # 5. NET POWER OUTPUT
    def eq_power_out(m, i, s):
        return m.x_power_net[i, s] == m.x_power_total[i, s] - m.x_power_PCC[i, s] - \
            sum(m.x_power_DAC[i, j, s] for j in set_quarter) - \
            m.x_power_compress[i, s] - m.x_power_aux[i, s]
    m.eq_power_out = Constraint(set_hour_0, set_scenario, rule=eq_power_out)

    return