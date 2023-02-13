"""
Modeling module
Constraints related to costing.

Pengfei Cheng
2023
"""

from pyomo.environ import Constraint
from ..params import *


def add_OM_costing_constraints(m, set_hour_0, set_scenario):

    # # FOM of DAC
    # def eq_FOM_DAC(m):
    #     return m.x_cost_DAC_FOM == (a_cost_sorbent * m.x_sorbent_total * 3000 + a_cost_adsorb * m.x_air_adsorb_max * 48000) * 0.05 + 2 * 110000
    # m.eq_FOM_DAC = Constraint(rule=eq_FOM_DAC)

    # VOM of NGCC
    def eq_VOM_NGCC(m, i, s):
        return m.x_cost_NGCC_VOM[i, s] == a_cost_NGCC_VOM * m.x_load[i, s]
    m.eq_VOM_NGCC = Constraint(set_hour_0, set_scenario, rule=eq_VOM_NGCC)

    # VOM of PCC
    def eq_cost_PCC_VOM(m, i, s):
        return m.x_cost_PCC_VOM[i, s] == a_cost_PCC_VOM * m.x_load[i, s]
    m.eq_cost_PCC_VOM = Constraint(set_hour_0, set_scenario, rule=eq_cost_PCC_VOM)

    # VOM of DAC
    def eq_cost_DAC_VOM(m, i, s):
        return m.x_cost_DAC_VOM[i, s] == a_cost_DAC_VOM * sum(m.x_CO2_DAC[i, j, s] for j in set_quarter)
    m.eq_cost_DAC_VOM = Constraint(set_hour_0, set_scenario, rule=eq_cost_DAC_VOM)

    # VOM of PCC compressor
    def eq_cost_PCC_compr_VOM(m, i, s):
        return m.x_cost_PCC_compr_VOM[i, s] == a_cost_PCC_compr_VOM * m.x_load[i, s]
    m.eq_cost_PCC_compr_VOM = Constraint(set_hour_0, set_scenario, rule=eq_cost_PCC_compr_VOM)

    # VOM of DAC compressor
    def eq_VOM_DAC_compressor(m, i, s):
        return m.x_cost_DAC_compr_VOM[i, s] == a_cost_DAC_compr_VOM * sum(m.x_CO2_DAC[i, j, s] for j in set_quarter)
    m.eq_VOM_DAC_compressor = Constraint(set_hour_0, set_scenario, rule=eq_VOM_DAC_compressor)

    return