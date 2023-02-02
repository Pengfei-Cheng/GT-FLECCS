"""
Output module
Pengfei Cheng

Output DAC operation-related results.
"""

import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *

def gen_DAC_air_df(m, set_hour):

    vars = [
        "time",
        "x_sorbent_F", "x_sorbent_S", "x_sorbent_A0", "x_sorbent_A1", "x_sorbent_R"
    ]

    dfs = {}

    for s in set_scenario:
        _dict = {}
        for var_name in vars:
            _tmp_list = []
            for i in set_hour:
                for j in set_quarter:
                    if var_name == "time":
                        _tmp_list.append(i + j * 1 / n_slice)
                    else:
                        var = getattr(m, var_name)
                        _tmp_list.append(value(var[i, j, s]))
            _dict[var_name] = _tmp_list

        dfs[s] = pd.DataFrame.from_dict(_dict)

    return dfs