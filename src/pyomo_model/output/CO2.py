"""
Output module
Pengfei Cheng

Output CO2-related results.
"""

import pandas as pd
from pyomo.environ import value


def gen_CO2_df(m):

    vars = [
        "x_CO2_flue", "x_CO2_PCC", "x_CO2_vent_PCC",
        "x_CO2_DAC", "x_CO2_cap_total"
    ]

    dict_list = []
    for var_name in vars:
        var = getattr(m, var_name)
        if var_name == 'x_CO2_DAC':
            _tmp_dict = {k1: 0 for k1, _ in var}
            for k1, k2 in var:
                _tmp_dict[k1] += value(var[k1, k2])
        else:
            _tmp_dict = {k: value(var[k]) for k in var}
        dict_list.append(_tmp_dict)

    df = pd.DataFrame(dict_list).T
    df.columns = vars

    return df