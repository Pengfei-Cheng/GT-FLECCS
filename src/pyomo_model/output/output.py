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


def write_results(m, output_prefix, output_suffix, set_hour, CO2_CREDIT, cost_NG, power_price, n_month, cost_start_up, SCENARIO_NAME, results):

    df_CO2 = gen_CO2_df(m)
    df_power = gen_power_df(m)
    df_steam = gen_steam_df(m)
    df_cost = gen_operation_cost_df(m, set_hour, power_price, CO2_CREDIT, cost_NG)
    df_DAC_air = gen_DAC_air_df(m, set_hour)
    df_disaggregated_vars = gen_disaggregated_var_df(m, set_hour)
    df_binary = gen_binary_df(m)
    df_DAC_costing = gen_DAC_cost_df(m)
    df_NPV, df_overall_profit_cost = gen_NPV_df(m, df_cost, df_binary, n_month, cost_start_up)

    # set output path
    rel_path = str(CO2_CREDIT) + "-" + SCENARIO_NAME
    if output_prefix != "":
        rel_path = output_prefix + "-" + rel_path
    if output_suffix != "":
        rel_path = rel_path + "-" + output_suffix

    # create results folder if it doesn't exist
    if not os.path.isdir('results'):
        os.mkdir("results")

    rel_path = "results/" + rel_path
    # create subfolder when it does not exist
    if not os.path.isdir(rel_path):
        os.mkdir(rel_path)

    # write CSV
    dfs = dict([
        ("results_CO2", df_CO2),
        ("results_power", df_power),
        ("results_steam", df_steam),
        ("results_DAC_air", df_DAC_air),
        ("results_operation_cost", df_cost),
        ("results_binary_vars", df_binary),
        ("results_disaggregated", df_disaggregated_vars),
        ("results_DAC_costing", df_DAC_costing),
        ("NPV", df_NPV),
        ("overall_profit_cost", df_overall_profit_cost)
        ])
    for idx, df in dfs.items():
        output_name = str(idx) + ".csv"
        df.to_csv(os.path.join(rel_path, output_name))

    # --------------------------------------------------------------------------

    # output meta data
    df_meta = pd.DataFrame(columns=["date", "CO2_credit", "scenario_name", "solve_time", "sorbent_amount", "gap"])
    lbd = results['Problem'][0]['Lower bound']
    ubd = results['Problem'][0]['Upper bound']
    gap = (ubd - lbd) / lbd
    df_meta.loc[0, :] = [
            datetime.now(),
            CO2_CREDIT,
            SCENARIO_NAME,
            results.solver.time,
            value(m.x_sorbent_total),
            gap
        ]

    # write to csv
    meta_file_name = "meta"
    if output_prefix != "":
        meta_file_name = output_prefix + "_" + meta_file_name
    if output_suffix != "":
        meta_file_name = meta_file_name + "-" + output_suffix

    meta_file = "results/" + meta_file_name + ".csv"
    if os.path.isfile(meta_file):
        df_meta.to_csv(meta_file, mode='a')
    else:
        df_meta.to_csv(meta_file)

    return