"""
Output module
Pengfei Cheng

Output DAC operation-related results.
"""

import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *

def gen_operation_cost_df(m, set_hour, power_price, CO2_CREDIT, cost_NG):

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

    df = pd.DataFrame(columns=cols)

    for i in set_hour:
        profit_power = power_price[i] * value(m.x_power_net[i])
        credit_CO2 = CO2_CREDIT * value(m.x_CO2_cap_total[i])
        cost_fuel = cost_NG * value(m.x_fuel[i])
        cost_CO2_TS = a_cost_CO2_TS * value(m.x_CO2_compress[i])
        cost_NGCC_VOM = value(m.x_cost_NGCC_VOM[i])
        cost_PCC_VOM = value(m.x_cost_PCC_VOM[i])
        cost_DAC_VOM = value(m.x_cost_DAC_VOM[i])
        cost_PCC_compr_VOM = value(m.x_cost_PCC_compr_VOM[i])
        cost_DAC_compr_VOM = value(m.x_cost_DAC_compr_VOM[i])
        res = [profit_power, credit_CO2, cost_fuel, cost_CO2_TS, cost_NGCC_VOM, cost_PCC_VOM, cost_DAC_VOM, cost_PCC_compr_VOM, cost_DAC_compr_VOM]
        df.loc[len(df)] = res

    return df