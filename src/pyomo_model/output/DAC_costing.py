"""
Output module
Pengfei Cheng

Output DAC operation-related results.
"""

import pandas as pd
from pyomo.environ import value

def gen_DAC_cost_df(m):

    vars = [
        "x_sorbent_total",
        "x_air_adsorb_max",
    ]

    dict_list = []
    for var_name in vars:
        var = getattr(m, var_name)
        _tmp_dict = {k: value(var[k]) for k in var}
        dict_list.append(_tmp_dict)

    df = pd.DataFrame(dict_list).T
    df.columns = vars

    return df