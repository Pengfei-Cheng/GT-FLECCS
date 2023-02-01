"""
Output module
Pengfei Cheng

Create the DataFrame for the binary variables.
"""

import pandas as pd
from pyomo.environ import value


def gen_binary_df(m):

    vars = [
        "y", "z", "z0",
    ]

    dict_list = []
    for var_name in vars:
        var = getattr(m, var_name)
        _tmp_dict = {k: value(var[k]) for k in var}
        dict_list.append(_tmp_dict)

    df = pd.DataFrame(dict_list).T
    df.columns = vars

    return df