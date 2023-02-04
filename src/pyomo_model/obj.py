"""
Objective Module
Define the objective function.

Pengfei Cheng
2022
"""

from pyomo.environ import *
from .params import *

def add_objective_function(m, cost_NG, power_price, cost_start_up, set_hour):

    def obj_expr(m):
        return \
            ( sum(
                scenario_prob[s] *
                sum(
                 - cost_NG * m.x_fuel[i, s] + \
                    unit_CO2_price[s] * m.x_CO2_cap_total[i, s] - \
                    a_cost_CO2_TS * m.x_CO2_compress[i, s] + \
                    power_price[i] * m.x_power_net[i, s] - \
                    cost_start_up[s] * m.z0[i, s] - \
                    m.x_cost_NGCC_VOM[i, s] - m.x_cost_PCC_VOM[i, s] - m.x_cost_DAC_VOM[i, s] - m.x_cost_PCC_compr_VOM[i, s] - m.x_cost_DAC_compr_VOM[i, s]
                for i in set_hour)
            for s in set_scenario)
            - ((a_cost_sorbent * m.x_sorbent_total * 3000 + a_cost_adsorb * m.x_air_adsorb_max * 48000) * 0.05 + 2 * 110000) ) * (1 - tax_r) * sum(1 / (1 + int_r) ** j for j in range(2, 21 + 1)) \
            - (a_cost_sorbent * m.x_sorbent_total * 3000 + a_cost_adsorb * m.x_air_adsorb_max * 48000) * (1 + 0.0311 + 0.0066 + 0.1779) * ( 0.3 + 0.7 / (1 + int_r) - sum(tax_r * depreciate_r * ((1 - depreciate_r) ** j) * ((1 + int_r) ** (- j - 2)) for j in range(19 + 1)) )
    m.obj = Objective(rule=obj_expr, sense=-1)

    return