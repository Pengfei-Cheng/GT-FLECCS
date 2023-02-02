"""
Output module
Pengfei Cheng

Output disaggregated variable-related results.
"""

import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *


def gen_disaggregated_var_df(m, set_hour):

    vars = [
        "x_load_D", "x_fuel_D", "x_CO2_D_flue",
        "x_power_D_HP", "x_power_D_IP", "x_power_D_aux",
        "x_steam_D_DAC_base", "x_steam_D_allocable"
    ]

    dfs = {}

    for s in set_scenario:
        _dict = {}
        for var_name in vars:
            _tmp_dict = {}
            for i in set_hour:
                for j in set_mode:
                    var = getattr(m, var_name)
                    _tmp_dict[i, j] = value(var[i, j, s])
            _dict[var_name] = _tmp_dict

        dfs[s] = pd.DataFrame.from_dict(_dict)

    return dfs