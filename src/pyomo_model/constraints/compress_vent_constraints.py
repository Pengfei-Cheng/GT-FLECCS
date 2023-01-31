"""
Modeling module
Declare compressor and vented CO2-related constraints.

Pengfei Cheng

1. CO2 compression amount
2. power usage of CO2 compression
3. total CO2 captured
"""


from pyomo.environ import *
from ..params import *

def add_compress_vent_constraints(m, set_hour_0):

    # 1. CO2 compression amount
    # integral over all slices within each hour
    def eq_compress_CO2(m, i):
        return m.x_CO2_compress[i] == m.x_CO2_PCC[i] + sum(m.x_CO2_DAC[i, j] for j in set_quarter)
    m.eq_compress_CO2 = Constraint(set_hour_0, rule=eq_compress_CO2)

    # --------------------------------------------------------------------------

    # 2. power usage of CO2 compression
    def eq_compress_CO2_power(m, i):
        return m.x_power_compress[i] == a_power_compr_PCC * m.x_CO2_PCC[i] + a_power_compr_DAC * sum(m.x_CO2_DAC[i, j] for j in set_quarter)
    m.eq_compress_CO2_power = Constraint(set_hour_0, rule=eq_compress_CO2_power)

    # --------------------------------------------------------------------------

    # 2. power usage of CO2 compression
    def eq_CO2_cap_total(m, i):
        return m.x_CO2_cap_total[i] == - m.x_CO2_vent_PCC[i] + (1 - a_CO2_vent_DAC) * sum(m.x_CO2_DAC[i, j] for j in set_quarter)
    m.eq_CO2_cap_total = Constraint(set_hour_0, rule=eq_CO2_cap_total)

    return