"""
Output module
Pengfei Cheng

Create the DataFrame for the binary variables.
"""

import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *


def gen_binary_df(m):

    dfs = {}

    vars = [
        "y", "z", "z0",
    ]

    for s in set_scenario:
        dict_list = []
        for var_name in vars:
            var = getattr(m, var_name)
            _tmp_dict = {i: value(var[i, _s]) for i, _s in var if _s == s}
            dict_list.append(_tmp_dict)

        df = pd.DataFrame(dict_list).T
        df.columns = vars

        dfs[s] = df

    return dfs