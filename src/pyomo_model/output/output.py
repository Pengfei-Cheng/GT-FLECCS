"""
Output module
Pengfei Cheng

Centralized output module.
"""

import os
import pandas as pd
from pyomo.environ import value
from .binary import gen_binary_df
from .CO2 import gen_CO2_df
from .DAC_air import gen_DAC_air_df
from .DAC_costing import gen_DAC_cost_df
from .disaggregated_vars import gen_disaggregated_var_df
from .operation_cost import gen_operation_cost_df
from .power import gen_power_df
from .steam import gen_steam_df
from .NPV import gen_NPV_df
from datetime import datetime
from src.pyomo_model.params import *


def write_results(m, output_prefix, output_suffix, set_hour, cost_NG, power_price, n_month, cost_start_up, elec_price_signal, results):

    df_CO2 = gen_CO2_df(m)
    df_power = gen_power_df(m)
    df_steam = gen_steam_df(m)
    df_cost = gen_operation_cost_df(m, set_hour, power_price, cost_NG)
    df_DAC_air = gen_DAC_air_df(m, set_hour)
    df_disaggregated_vars = gen_disaggregated_var_df(m, set_hour)
    df_binary = gen_binary_df(m)
    df_DAC_costing = gen_DAC_cost_df(m)
    df_NPV, df_overall_profit_cost = gen_NPV_df(m, df_cost, df_binary, n_month, cost_start_up)

    # set output path
    rel_path = elec_price_signal + "-" 
    if n_month == 1:
        rel_path += str(n_month) + "-month"
    else:
        rel_path += str(n_month) + "-months"
    if output_prefix != "":
        rel_path = output_prefix + "-" + rel_path
    if output_suffix != "":
        rel_path = rel_path + "-" + output_suffix

    # create results folder if it doesn't exist
    if not os.path.isdir('SP_results'):
        os.mkdir("SP_results")

    rel_path = "SP_results/" + rel_path
    # create subfolder when it does not exist
    if not os.path.isdir(rel_path):
        os.mkdir(rel_path)

    # output the DAC costing results (not indexed by scenarios)
    output_name = str("results_DAC_costing") + ".csv"
    df_DAC_costing.to_csv(os.path.join(rel_path, output_name))

    # sub-subfolder for scenarios
    for s in set_scenario:
        _rel_path = rel_path + "/" + str(unit_CO2_price[s])
        # create sub-subfolder when it does not exist
        if not os.path.isdir(_rel_path):
            os.mkdir(_rel_path)

        # write CSV
        dfs = dict([
            ("results_CO2", df_CO2[s]),
            ("results_power", df_power[s]),
            ("results_steam", df_steam[s]),
            ("results_DAC_air", df_DAC_air[s]),
            ("results_operation_cost", df_cost[s]),
            ("results_binary_vars", df_binary[s]),
            ("results_disaggregated", df_disaggregated_vars[s]),
            # ("results_DAC_costing", df_DAC_costing[s]),
            ("NPV", df_NPV[s]),
            ("overall_profit_cost", df_overall_profit_cost[s])
            ])
        for idx, df in dfs.items():
            output_name = str(idx) + ".csv"
            df.to_csv(os.path.join(_rel_path, output_name))

        # --------------------------------------------------------------------------

        # output meta data
        df_meta = pd.DataFrame(columns=["date", "scenario_name", "solve_time", "sorbent_amount", "gap"])
        lbd = results['Problem'][0]['Lower bound']
        ubd = results['Problem'][0]['Upper bound']
        gap = (ubd - lbd) / lbd
        df_meta.loc[0, :] = [
            datetime.now(),
            elec_price_signal,
            results.solver.time,
            value(m.x_sorbent_total * 3000),
            gap
        ]

        # write to csv
        meta_file_name = "meta"
        if output_prefix != "":
            meta_file_name = output_prefix + "_" + meta_file_name
        if output_suffix != "":
            meta_file_name = meta_file_name + "-" + output_suffix

        meta_file = "SP_results/" + meta_file_name + ".csv"
        if os.path.isfile(meta_file):
            df_meta.to_csv(meta_file, mode='a')
        else:
            df_meta.to_csv(meta_file)