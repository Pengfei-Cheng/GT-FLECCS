"""
Centralized Optimization Module
Pengfei Cheng
"""

import logging
from pathlib import Path
from itertools import product
import pandas as pd
from .params import *
from .variables import declare_variables
from .constraints import *
from .obj import add_objective_function
from pyomo.environ import ConcreteModel, Var, Constraint
from .....main import StochasticModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

# electricity price signal-select from:
# ["MiNg_150_NYISO", "MiNg_150_PJM-W", "MiNg_150_CAISO", "MiNg_150_ERCOT",
# "MiNg_100_NYISO", "MiNg_100_PJM-W", "MiNg_100_CAISO", "MiNg_100_ERCOT",
# "MiNg_150_MISO-W", "BaseCaseTax", "HighWindTax", "HighSolarTax",
# "WinterNYTax"]
def const_model(n_day=2, elec_price_signal="MiNg_150_NYISO", week_diff=1):

    # check if the given arguments are reasonable
    if n_day > week_diff * 7:
        msg = "Provided day number is larger than the interval difference. "
        msg += "This would cause overlaps of electricity signals in consecutive scenarios. "
        msg += f"day number: {n_day}; interval difference: {week_diff * 7}."
        raise ValueError(msg)
    if week_diff < 1:
        msg = "The minimum interval difference should be 1 week. "
        msg += f"Provided argument: {week_diff} week."
        raise ValueError(msg)

    # --------------------------------------------------------------------------

    logger.info("*" * 80)
    logger.info("*" * 18 + "   GATECH NGCC-PCC-DAC OPTIMIZATION MODEL   " + "*" * 18)
    logger.info("*" * 28 + "   STOCHASTIC VERSION   " + "*" * 28)
    logger.info("*" * 30 + "   Pengfei Cheng   " + "*" * 31)
    logger.info("*" * 80 + "\n")

    # --------------------------------------------------------------------------

    # PARAMETERS TO ADJUST

    # natural gas price, $/MMBtu
    cost_NG = 3.83
    # cost_NG = 4.5
    # cost_NG = 6.0

    # whether to limit the start-up times to 5
    limit_start_up = True

    # --------------------------------------------------------------------------

    # TIME SETUP
    # total hours
    n_hour = int(24 * n_day)
    # set of hours
    set_hour_0 = list(range(n_hour + 1))
    set_hour = list(range(1, n_hour + 1))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------


    logger.info("\n" + "-" * 80)
    logger.info("Electricity price signal: " + elec_price_signal)

    # cost parameters
    # power price profile, USD/MWh
    script_path = Path(__file__, '../..').resolve()
    df_power_price = pd.read_csv(str(script_path.joinpath('resources/overall-price-signals.csv')))
    # dropna
    df_power_price = df_power_price.dropna()
    # choose scenario
    power_price = df_power_price.loc[:, elec_price_signal]

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # SCENARIO GENERATION

    # generate list of months for scenarios
    weeks = range(52 // week_diff)
    signals = []

    for w in weeks:
        base = w * week_diff * 7 * 24
        # read the signal during that week
        _signal = power_price[base:base + n_hour].values
        signals.append(_signal)

    # generate scenarios as product of two lists
    scenario_param = list(product(unit_CO2_price, signals))
    set_scenario = list(range(len(scenario_param)))

    # probability of each scenario
    scenario_prob = {i: 1 / len(set_scenario) for i in set_scenario}
    # --------------------------------------------------------------------------

    # START-UP COST
    # start-up cost, $, scenario dependent
    # CO2 emission during start-up: 100.45 tonne
    # fuel consumption during start-up: 16958.58 MMBtu
    cost_start_up = {i: 100.45 * scenario_param[i][0] + 16958.58 * cost_NG for i in set_scenario}


    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # construct model
    logger.info("Constructing model...")

    w = ConcreteModel()

    declare_variables(w, set_hour_0, set_scenario)
    add_compress_vent_constraints(w, set_hour_0, set_scenario)
    add_DAC_constraints(w, set_hour_0, set_hour, n_hour, set_scenario)
    add_DAC_costing_constraints(w, set_hour_0, set_scenario)
    add_disaggregated_constraints(w, set_hour_0, set_scenario)
    add_OM_costing_constraints(w, set_hour_0, set_scenario)
    add_operation_mode_logic_constraints(w, limit_start_up, set_hour_0, set_hour, set_scenario)
    add_overall_var_constraints(w, set_hour_0, set_scenario)
    add_PCC_constraints(w, set_hour_0, set_scenario)
    add_power_constraints(w, set_hour_0, set_scenario)
    add_steam_split_constraints(w, set_hour_0, set_scenario)

    add_objective_function(w, cost_NG, power_price, cost_start_up, set_hour, set_scenario, scenario_prob, scenario_param)

    logger.info("Done.")

    # --------------------------------------------------------------------------
    # print model size

    logger.info(f"# variable: \t{sum(1 for _ in w.component_data_objects(Var))}")
    logger.info(f"# constraint: \t{sum(1 for _ in w.component_data_objects(Constraint))}")

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # model transformation -----------------------------------------------------

    # set_scenario
    fs_vars = ["x_sorbent_total", "x_air_adsorb_max"]
    fs_cons = []

    def _obj(m, s):
        return \
            (
                scenario_prob[s] *
                sum(
                    - cost_NG * m.x_fuel[i, s] + \
                    scenario_param[s][0] * m.x_CO2_cap_total[i, s] - \
                    a_cost_CO2_TS * m.x_CO2_compress[i, s] + \
                    power_price[i] * m.x_power_net[i, s] - \
                    cost_start_up[s] * m.z0[i, s] - \
                    m.x_cost_NGCC_VOM[i, s] - m.x_cost_PCC_VOM[i, s] - m.x_cost_DAC_VOM[i, s] - m.x_cost_PCC_compr_VOM[i, s] - m.x_cost_DAC_compr_VOM[i, s]
                    for i in set_hour
                ) / len(set_hour) * 364 * 24
                - ((a_cost_sorbent * m.x_sorbent_total * 3000 + a_cost_adsorb * m.x_air_adsorb_max * 48000) * 0.05 + 2 * 110000)
            ) * (1 - tax_r) * sum(1 / (1 + int_r) ** j for j in range(2, 21 + 1)) \
            - scenario_prob[s] * (a_cost_sorbent * m.x_sorbent_total * 3000 + a_cost_adsorb * m.x_air_adsorb_max * 48000) * (1 + 0.0311 + 0.0066 + 0.1779) * ( 0.3 + 0.7 / (1 + int_r) - sum(tax_r * depreciate_r * ((1 - depreciate_r) ** j) * ((1 + int_r) ** (- j - 2)) for j in range(19 + 1)) )
    objs = {s: _obj for s in set_scenario}

    mm = StochasticModel()
    mm.build_from_pyomo(w, fs_vars, fs_cons, set_scenario, objs, obj_sense=-1)

    return mm
