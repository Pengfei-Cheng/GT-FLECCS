"""
Modeling module
Declare DAC-air-related constraints.

Pengfei Cheng

1. state equation
2. continuity of states
3. initial conditions
4. end conditions
5. CO2 capture
6. steam usage
7. power usage
8. mass balance inequalities
"""

from pyomo.environ import Constraint
from ..params import *


def add_DAC_constraints(m, set_hour_0, set_hour, n_hour, set_scenario):

    # 1. STATE EQUATION
    # x_sorbent_A1
    def eq_A1_state(m, i, j, s):
        return m.x_sorbent_A1[i, j + 1, s] == m.x_sorbent_A0[i, j, s]
    m.eq_A1_state = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_A1_state)
    # x_sorbent_F
    def eq_f_state(m, i, j, s):
        return m.x_sorbent_F[i, j + 1, s] == m.x_sorbent_F[i, j, s] - m.x_sorbent_A0[i, j, s] + m.x_sorbent_R[i, j, s]
    m.eq_f_state = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_f_state)
    # x_sorbent_S
    def eq_s_state(m, i, j, s):
        return m.x_sorbent_S[i, j + 1, s] == m.x_sorbent_S[i, j, s] - m.x_sorbent_R[i, j, s] + m.x_sorbent_A1[i, j, s]
    m.eq_s_state = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_s_state)

    # --------------------------------------------------------------------------

    # 2. CONTINUITY OF STATES
    # connect the ending slice with the beginning slice of the next hour

    # x_sorbent_A1
    def eq_A1_cont(m, i, s):
        return m.x_sorbent_A1[i, 0, s] == m.x_sorbent_A1[i - 1, n_slice, s]
    m.eq_A1_cont = Constraint(set_hour, set_scenario, rule=eq_A1_cont)
    # x_sorbent_F
    def eq_F_cont(m, i, s):
        return m.x_sorbent_F[i, 0, s] == m.x_sorbent_F[i - 1, n_slice, s]
    m.eq_F_cont = Constraint(set_hour, set_scenario, rule=eq_F_cont)
    # x_sorbent_S
    def eq_S_cont(m, i, s):
        return m.x_sorbent_S[i, 0, s] == m.x_sorbent_S[i - 1, n_slice, s]
    m.eq_S_cont = Constraint(set_hour, set_scenario, rule=eq_S_cont)

    # --------------------------------------------------------------------------

    # 3. INITIAL CONDITIONS
    def eq_A1_init(m, s):
        return m.x_sorbent_A1[0, 0, s] == 0
    m.eq_A1_init = Constraint(set_scenario, rule=eq_A1_init)
    def eq_F_init(m, s):
        return m.x_sorbent_F[0, 0, s] == m.x_sorbent_total * 3000
    m.eq_F_init = Constraint(set_scenario, rule=eq_F_init)
    def eq_S_init(m, s):
        return m.x_sorbent_S[0, 0, s] == 0
    m.eq_S_init = Constraint(set_scenario, rule=eq_S_init)

    # --------------------------------------------------------------------------

    # 4. END CONDITIONS
    def eq_A1_end(m, s):
        return m.x_sorbent_A1[n_hour, n_slice, s] == 0
    m.eq_A1_end = Constraint(set_scenario, rule=eq_A1_end)
    def eq_f_end(m, s):
        return m.x_sorbent_F[n_hour, n_slice, s] == m.x_sorbent_total * 3000
    m.eq_f_end = Constraint(set_scenario, rule=eq_f_end)
    def eq_s_end(m, s):
        return m.x_sorbent_S[n_hour, n_slice, s] == 0
    m.eq_s_end = Constraint(set_scenario, rule=eq_s_end)

    # --------------------------------------------------------------------------

    # 5. CO2 capture
    def eq_CO2_DAC(m, i, j, s):
        return m.x_CO2_DAC[i, j, s] == sorbent_cap_DAC_air * m.x_sorbent_R[i, j, s]
    m.eq_CO2_DAC = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_CO2_DAC)

    # --------------------------------------------------------------------------

    # 6. STEAM USAGE
    def eq_steam_DAC(m, i, j, s):
        return m.x_steam_DAC[i, j, s] == a_steam_DAC * sorbent_cap_DAC_air * m.x_sorbent_R[i, j, s]
    m.eq_steam_DAC = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_steam_DAC)

    # --------------------------------------------------------------------------

    # 7. POWER USAGE
    def eq_power_DAC(m, i, j, s):
        return m.x_power_DAC[i, j, s] == a_power_DAC * sorbent_cap_DAC_air * (m.x_sorbent_A0[i, j, s] + m.x_sorbent_A1[i, j, s]) / 2
    m.eq_power_DAC = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_power_DAC)

    # --------------------------------------------------------------------------

    # 8. MASS BALANCE INEQUALITIES
    def eq_A0_limit(m, i, j, s):
        return m.x_sorbent_A0[i, j, s] <= m.x_sorbent_F[i, j, s]
    m.eq_A0_limit = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_A0_limit)
    def eq_R_limit(m, i, j, s):
        return m.x_sorbent_R[i, j, s] <= m.x_sorbent_S[i, j, s]
    m.eq_R_limit = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_R_limit)

    return