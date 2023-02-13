"""
Modeling module
Declare operation model logic constraints.

Pengfei Cheng

1. lam constraint: dispatch only, sum of extreme points is y
2. relationship between y and z0
3. minimum on-hours during start-up
4. z0 and z relationship
5. limitation on start up times

UPDATE:
    06-08-2022: added start-up time limitation constraint
"""

from pyomo.environ import Constraint
from ..params import *


def add_operation_mode_logic_constraints(m, limit_start_up, set_hour_0, set_hour, set_scenario):

    # 1. LAM CONSTRAINT: DISPATCH ONLY, SUM OF EXTREME POINTS IS Y
    # when y = 0, z = 0, sum of lam = 0, x_load_D = 0
    # when y = 1, z = 1, start-up: x_load_D[i, dispatch_idx] = 0
    # when y = 1, z = 0, normal dispatch mode: x_load_D[i, dispatch_idx]
    # is a combination of convex points
    def eq_lam(m, i, s):
        return sum(m.lam[i, k, s] for k in x_range_extreme_points) == m.y[i, s] - m.z[i, s]
    m.eq_lam = Constraint(set_hour_0, set_scenario, rule=eq_lam)

    # --------------------------------------------------------------------------

    # 2. RELATIONSHIP BETWEEN Y AND Z
    def eq_transition(m, i, s):
        return m.z0[i, s] >= m.y[i, s] - m.y[i-1, s]
    m.eq_transition = Constraint(set_hour, set_scenario, rule=eq_transition)

    def eq_transition_init(m, s):
        return m.z0[0, s] == 0
    m.eq_transition_init = Constraint(set_scenario, rule=eq_transition_init)

    # 3. MINIMUM ON-HOURS DURING START-UP
    def eq_min_on_hours(m, i, s):
        return m.y[i, s] >= sum(m.z0[i - k + 1, s] for k in set_start_up_hour if i - k + 1 >= 0)
    m.eq_min_on_hours = Constraint(set_hour_0, set_scenario, rule=eq_min_on_hours)

    # --------------------------------------------------------------------------

    # 4. Z AND Z2 RELATIONSHIP
    def eq_transitioning_states(m, i, s):
        return m.z[i, s] == sum((m.z0[i - k + 1, s]) for k in set_start_up_hour if i - k + 1 >= 0)
    m.eq_transitioning_states = Constraint(set_hour_0, set_scenario, rule=eq_transitioning_states)

    # 5. Limitation on start up times
    if limit_start_up:
        def eq_limit_startup_times(m, s):
            return sum(m.z0[i, s] for i in set_hour_0) <= 5
        m.eq_limit_startup_times = Constraint(set_scenario, rule=eq_limit_startup_times)

    return