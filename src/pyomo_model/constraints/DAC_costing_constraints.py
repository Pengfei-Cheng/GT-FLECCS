"""
Modeling module
Constraints related to DAC costing.

Pengfei Cheng
2022
"""

from pyomo.environ import Constraint
from ..params import *


def add_DAC_costing_constraints(m, set_hour_0, set_scenario):

    # volume of blown air
    def eq_adsorb_air_volume(m, i, j, s):
        return m.x_air_adsorb[i, j, s] >= (m.x_sorbent_A0[i, j, s] + m.x_sorbent_A1[i, j, s]) * sorbent_cap_DAC_air / 2 * tonne_to_g / CO2_mole_w * mole_vol / CO2_vol_ratio
    m.eq_adsorb_air_volume = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_adsorb_air_volume)

    # max adsorption air rate
    def eq_adsorb_max_air_rate(m, i, j, s):
        return m.x_air_adsorb_max * 48000 >= m.x_air_adsorb[i, j, s] / 15 / 60  # 1 slice = 15 min = 900 s
    m.eq_adsorb_max_air_rate = Constraint(set_hour_0, set_quarter, set_scenario, rule=eq_adsorb_max_air_rate)

    return