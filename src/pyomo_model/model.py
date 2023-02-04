"""
Centralized Optimization Module
Pengfei Cheng
"""

import logging
from pathlib import Path
import pandas as pd
from pyomo.environ import *
from itertools import product
from .variables import declare_variables
from .constraints import *
from .output import write_results
from .obj import add_objective_function

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

logger.info("*" * 80)
logger.info("*" * 18 + "   GATECH NGCC-PCC-DAC OPTIMIZATION MODEL   " + "*" * 18)
logger.info("*" * 30 + "   Pengfei Cheng   " + "*" * 31)
logger.info("*" * 80 + "\n")

# ------------------------------------------------------------------------------

# PARAMETERS TO ADJUST

# number of months
# n_month = 1
n_month = 12

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

# how many scenarios to run
# all 36 scenarios
# SCENARIOS = "ALL"
# A single scenario (for testing)
SCENARIOS = "ONE"

# prefix and suffix for solution folder
PREFIX = "NG-383"
SUFFIX = ""

# ------------------------------------------------------------------------------

# TIME SETUP
# total hours
n_hour = 24 * n_month * 30
# set of hours
set_hour_0 = list(range(n_hour + 1))
set_hour = list(range(1, n_hour + 1))

# ------------------------------------------------------------------------------

# SCENARIO GENERATION
# CO2 price + electricity price signal

CO2_credits = [150, 225, 300]
scenario_names = [
    "MiNg_150_NYISO",
    "MiNg_150_PJM-W",
    "MiNg_150_CAISO",
    "MiNg_150_ERCOT",
    "MiNg_150_MISO-W",
    "BaseCaseTax",
    "HighWindTax",
    "HighSolarTax",
    "WinterNYTax",
]
scenarios_1 = product(CO2_credits, scenario_names)

CO2_credits = [100]
scenario_names = [
    "MiNg_100_NYISO",
    "MiNg_100_PJM-W",
    "MiNg_100_CAISO",
    "MiNg_100_ERCOT",
    "MiNg_100_MISO-W",
    "BaseCaseTax",
    "HighWindTax",
    "HighSolarTax",
    "WinterNYTax",
]
scenarios_2 = product(CO2_credits, scenario_names)

full_scenarios = list(scenarios_1) + list(scenarios_2)

# single scenario array for test
test_scenarios = [(300, "MiNg_150_NYISO")]

if SCENARIOS == "ALL":
    scenarios = full_scenarios
else:
    scenarios = test_scenarios

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

for (CO2_credit, scenario_name) in scenarios:

    # refer to global variables
    SCENARIO_NAME = scenario_name
    CO2_CREDIT = CO2_credit

    logger.info("\n" + "-" * 80)
    logger.info("Scenario: " + SCENARIO_NAME + "\t\tCO2 credit: " + str(CO2_CREDIT))

    # cost parameters
    # power price profile, USD/MWh
    script_path = Path(__file__, '../..').resolve()
    df_power_price = pd.read_csv(str(script_path.joinpath('resources/overall-price-signals.csv')))
    # dropna
    df_power_price = df_power_price.dropna()
    # choose scenario
    power_price = df_power_price.loc[:, SCENARIO_NAME]

    # start-up cost, $
    # CO2 emission during start-up: 100.45 tonne
    # fuel consumption during start-up: 16958.58 MMBtu
    cost_start_up = 100.45 * CO2_CREDIT + 16958.58 * cost_NG

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

    add_objective_function(m, cost_NG, CO2_CREDIT, power_price, cost_start_up, set_hour)

    # --------------------------------------------------------------------------
    # print model status

    logger.info(f"# variable: \t{sum(1 for _ in m.component_data_objects(Var))}")
    logger.info(f"# constraint: \t{sum(1 for _ in m.component_data_objects(Constraint))}")

    # --------------------------------------------------------------------------

    # set optimizer options
    solver = SolverFactory('gurobi')
    solver.options['MIPGap'] = GAP

    # # specify branch priority: y first
    # NOTE: this seems not supported in Pyomo yet. See https://support.gurobi.com/hc/en-us/community/posts/4409208647953-Setting-up-Branching-Priority-for-GUROBI-in-Pyomo-Attention-Richard-from-OR-Stackexchange-
    # y = m[:y]
    # for i in set_hour_0
    #     Gurobi.MOI.set(m, Gurobi.VariableAttribute("BranchPriority"), y[i], 1)
    # end

    # set time limit
    solver.options['TimeLimit'] = TIME_LIMIT

    # solve the problem
    results = solver.solve(m, tee=True)

    logger.info(f"solving time: {round(results.solver.time, 0)} s")

    # --------------------------------------------------------------------------

    # output results

    logger.info("Writing output...")

    write_results(m, PREFIX, SUFFIX, set_hour, CO2_CREDIT, cost_NG, power_price, n_month, cost_start_up, SCENARIO_NAME, results)

    logger.info("Done.")