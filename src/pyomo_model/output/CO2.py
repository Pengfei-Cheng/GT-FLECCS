"""
Output module
Pengfei Cheng

Output CO2-related results.
"""

import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *


def gen_CO2_df(m):

    dfs = {}

    vars = [
        "x_CO2_flue", "x_CO2_PCC", "x_CO2_vent_PCC",
        "x_CO2_DAC", "x_CO2_cap_total"
    ]

    for s in set_scenario:
        dict_list = []
        for var_name in vars:
            var = getattr(m, var_name)
            if var_name == 'x_CO2_DAC':
                _tmp_dict = {k1: 0 for k1, _, _ in var}
                for k1, k2, _s in var:
                    if _s == s:
                        _tmp_dict[k1] += value(var[k1, k2, _s])
            else:
                _tmp_dict = {i: value(var[i, _s]) for i, _s in var if _s == s}
            dict_list.append(_tmp_dict)

        df = pd.DataFrame(dict_list).T
        df.columns = vars
        dfs[s] = df

    return dfs