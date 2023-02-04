"""
Centralized Optimization Module
Pengfei Cheng
"""

import logging
from pathlib import Path
import pandas as pd
from pyomo.environ import *
from .params import *
from .variables import declare_variables
from .constraints import *
from .obj import add_objective_function
from pyomo.environ import RangeSet, ConcreteModel, Var, NonNegativeReals, Binary, Constraint, Objective

import os
from .....main import StochasticModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

def const_model():

    logger.info("*" * 80)
    logger.info("*" * 18 + "   GATECH NGCC-PCC-DAC OPTIMIZATION MODEL   " + "*" * 18)
    logger.info("*" * 28 + "   STOCHASTIC VERSION   " + "*" * 28)
    logger.info("*" * 30 + "   Pengfei Cheng   " + "*" * 31)
    logger.info("*" * 80 + "\n")

    # --------------------------------------------------------------------------

    # PARAMETERS TO ADJUST

    # electricity price signal
    # select from:
    # ["MiNg_150_NYISO", "MiNg_150_PJM-W", "MiNg_150_CAISO", "MiNg_150_ERCOT",
    # "MiNg_100_NYISO", "MiNg_100_PJM-W", "MiNg_100_CAISO", "MiNg_100_ERCOT",
    # "MiNg_150_MISO-W", "BaseCaseTax", "HighWindTax", "HighSolarTax",
    # "WinterNYTax"]
    elec_price_signal = "MiNg_150_NYISO"

    # number of months
    n_month = 1
    # n_month = 12

    # solving time limit
    TIME_LIMIT = 3600
    # solving optimality gap
    GAP = 0.01

    # natural gas price, $/MMBtu
    cost_NG = 3.83
    # cost_NG = 4.5
    # cost_NG = 6.0

    # whether to limit the start-up times to 5
    limit_start_up = True

    # prefix and suffix for solution folder
    PREFIX = "NG-383"
    SUFFIX = ""

    # -----------------------------------------------------------------------------

    # TIME SETUP
    # total hours
    n_hour = 24 * n_month * 30
    # set of hours
    set_hour_0 = list(range(n_hour + 1))
    set_hour = list(range(1, n_hour + 1))

    # --------------------------------------------------------------------------

    # START-UP COST
    # start-up cost, $, scenario dependent
    # CO2 emission during start-up: 100.45 tonne
    # fuel consumption during start-up: 16958.58 MMBtu
    cost_start_up = {k: 100.45 * v + 16958.58 * cost_NG for k, v in unit_CO2_price.items()}

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

    # construct model
    logger.info("Constructing model...")

    m = ConcreteModel()

    declare_variables(m, set_hour_0)
    add_compress_vent_constraints(m, set_hour_0)
    add_DAC_constraints(m, set_hour_0, set_hour, n_hour)
    add_DAC_costing_constraints(m, set_hour_0)
    add_disaggregated_constraints(m, set_hour_0)
    add_OM_costing_constraints(m, set_hour_0)
    add_operation_mode_logic_constraints(m, limit_start_up, set_hour_0, set_hour)
    add_overall_var_constraints(m, set_hour_0)
    add_PCC_constraints(m, set_hour_0)
    add_power_constraints(m, set_hour_0)
    add_steam_split_constraints(m, set_hour_0)

    add_objective_function(m, cost_NG, power_price, cost_start_up, set_hour)

    logger.info("Done.")

    # --------------------------------------------------------------------------
    # print model size

    logger.info(f"# variable: \t{sum(1 for _ in m.component_data_objects(Var))}")
    logger.info(f"# constraint: \t{sum(1 for _ in m.component_data_objects(Constraint))}")

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
                    unit_CO2_price[s] * m.x_CO2_cap_total[i, s] - \
                    a_cost_CO2_TS * m.x_CO2_compress[i, s] + \
                    power_price[i] * m.x_power_net[i, s] - \
                    cost_start_up[s] * m.z0[i, s] - \
                    m.x_cost_NGCC_VOM[i, s] - m.x_cost_PCC_VOM[i, s] - m.x_cost_DAC_VOM[i, s] - m.x_cost_PCC_compr_VOM[i, s] - m.x_cost_DAC_compr_VOM[i, s]
                for i in set_hour)
                - ((a_cost_sorbent * m.x_sorbent_total + a_cost_adsorb * m.x_air_adsorb_max) * 0.05 + 2 * 110000)
            ) * (1 - tax_r) * sum(1 / (1 + int_r) ** j for j in range(2, 21 + 1)) \
            - scenario_prob[s] * (a_cost_sorbent * m.x_sorbent_total + a_cost_adsorb * m.x_air_adsorb_max) * (1 + 0.0311 + 0.0066 + 0.1779) * ( 0.3 + 0.7 / (1 + int_r) - sum(tax_r * depreciate_r * ((1 - depreciate_r) ** j) * ((1 + int_r) ** (- j - 2)) for j in range(19 + 1)) )
    objs = {s: _obj for s in set_scenario}

    mm = StochasticModel()
    mm.build_from_pyomo(m, fs_vars, fs_cons, set_scenario, objs)

    return mm
