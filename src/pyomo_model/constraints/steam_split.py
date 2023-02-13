"""
Modeling module
Declare steam split constraints.

Pengfei Cheng

1. steam allocation
2. total DAC steam
3. DAC steam slack
4. steam rate limit

UPDATE:
    01-21-2022: added steam rate limit constraint.
"""

from pyomo.environ import Constraint
from ..params import *


def add_steam_split_constraints(m, set_hour_0, set_scenario):

    # 1. STEAM ALLOCATION
    def eq_steam_allocation(m, i, s):
        return m.x_steam_allocable[i, s] == m.x_steam_DAC_extra[i, s] + m.x_steam_LP[i, s]
    m.eq_steam_allocation = Constraint(set_hour_0, set_scenario, rule=eq_steam_allocation)

    # --------------------------------------------------------------------------

    # 2. TOTAL DAC STEAM
    def eq_DAC_total_duty(m, i, s):
        return m.x_steam_DAC_total[i, s] == m.x_steam_DAC_base[i, s] + m.x_steam_DAC_extra[i, s]
    m.eq_DAC_total_duty = Constraint(set_hour_0, set_scenario, rule=eq_DAC_total_duty)

    # --------------------------------------------------------------------------

    # 3. DAC STEAM SLACK
    # integral over all slices within each hour
    def eq_DAC_steam_slack_int(m, i, s):
        return m.x_steam_DAC_total[i, s] >= sum(m.x_steam_DAC[i, j, s] for j in set_quarter)
    m.eq_DAC_steam_slack_int = Constraint(set_hour_0, set_scenario, rule=eq_DAC_steam_slack_int)

    # --------------------------------------------------------------------------

    # 4. STEAM RATE LIMIT
    # 15-min steam into DACs cannot exceed 1/4 of 1-hour available steam
    def eq_DAC_steam_rate_limit(m, i, j, s):
        return m.x_steam_DAC_total[i, s] / 4 >= m.x_steam_DAC[i, j, s]
    m.eq_DAC_steam_rate_limit = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_DAC_steam_rate_limit)

    return