"""
Output module
Pengfei Cheng

Output DAC operation-related results.
"""

import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *

def gen_operation_cost_df(m, set_hour, power_price, cost_NG):

    cols = [
        "profit_power",
        "credit_CO2",
        "cost_fuel",
        "cost_CO2_TS",
        "cost_NGCC_VOM",
        "cost_PCC_VOM",
        "cost_DAC_VOM",
        "cost_PCC_compr_VOM",
        "cost_DAC_compr_VOM"
    ]

    dfs = {}

    for s in set_scenario:
        df = pd.DataFrame(columns=cols)
        for i in set_hour:
            profit_power = power_price[i] * value(m.x_power_net[i, s])
            credit_CO2 = unit_CO2_price[s] * value(m.x_CO2_cap_total[i, s])
            cost_fuel = cost_NG * value(m.x_fuel[i, s])
            cost_CO2_TS = a_cost_CO2_TS * value(m.x_CO2_compress[i, s])
            cost_NGCC_VOM = value(m.x_cost_NGCC_VOM[i, s])
            cost_PCC_VOM = value(m.x_cost_PCC_VOM[i, s])
            cost_DAC_VOM = value(m.x_cost_DAC_VOM[i, s])
            cost_PCC_compr_VOM = value(m.x_cost_PCC_compr_VOM[i, s])
            cost_DAC_compr_VOM = value(m.x_cost_DAC_compr_VOM[i, s])
            res = [profit_power, credit_CO2, cost_fuel, cost_CO2_TS, cost_NGCC_VOM, cost_PCC_VOM, cost_DAC_VOM, cost_PCC_compr_VOM, cost_DAC_compr_VOM]
            df.loc[len(df)] = res
        dfs[s] = df

    return dfs