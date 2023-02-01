"""
Output module
Pengfei Cheng

Output steam-related results.
"""

import pandas as pd
from pyomo.environ import value


def gen_steam_df(m):

    vars = [
        "x_steam_PCC",
        "x_steam_DAC_total", "x_steam_DAC",
        "x_steam_allocable", "x_steam_DAC_base",
        "x_steam_DAC_extra", "x_steam_LP"
    ]

    dict_list = []
    for var_name in vars:
        var = getattr(m, var_name)
        if var_name == 'x_steam_DAC':
            _tmp_dict = {k1: 0 for k1, _ in var}
            for k1, k2 in var:
                _tmp_dict[k1] += value(var[k1, k2])
        else:
            _tmp_dict = {k: value(var[k]) for k in var}
        dict_list.append(_tmp_dict)

    df = pd.DataFrame(dict_list).T
    df.columns = vars
    return df