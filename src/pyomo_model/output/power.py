"""
Output module
Pengfei Cheng

Output power-related results.
"""

import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *


def gen_power_df(m):

    vars = [
        "x_load", "x_power_GT", "x_power_ST", "x_power_HP", "x_power_IP",
        "x_power_LP", "x_power_PCC", "x_power_DAC",
        "x_power_compress", "x_power_aux", "x_power_total", "x_power_net"
    ]

    dfs = {}

    for s in set_scenario:
        dict_list = []
        for var_name in vars:
            var = getattr(m, var_name)
            if var_name == 'x_power_DAC':
                _tmp_dict = {k1: 0 for k1, _, _ in var}
                for k1, k2, _s in var:
                    if _s == s:
                        _tmp_dict[k1] += value(var[k1, k2, _s])
            else:
                _tmp_dict = {k: value(var[k, _s]) for k, _s in var if _s == s}
            dict_list.append(_tmp_dict)

        df = pd.DataFrame(dict_list).T
        df.columns = vars

        dfs[s] = df

    return dfs