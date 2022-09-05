"""
Centralized Optimization Module
Pengfei Cheng
"""

println("*" ^ 80)
println("*" ^ 18 * "   GATECH NGCC-PCC-DAC OPTIMIZATION MODEL   " * "*" ^ 18)
println("*" ^ 30 * "   Pengfei Cheng   " * "*" ^ 31)
println("*" ^ 80 * "\n")

# ------------------------------------------------------------------------------

# PARAMETERS TO ADJUST

# solving time limit
TIME_LIMIT = 3600
# solving optimality gap
GAP = 0.01

# natural gas price, $/MMBtu
global cost_NG = 3.83
# global cost_NG = 4.5
# global cost_NG = 6.0

# whether to limit the start-up times to 5
global limit_start_up = true

# how many scenarios to run
# all 36 scenarios
SCENARIOS = "ALL"
# A single scenario (for testing)
# SCENARIOS = "ONE"

# prefix and suffix for solution folder
PREFIX = "NG-383"
SUFFIX = ""

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# import parameters
println("Importing parameters...")

include("params/regression.jl")
include("params/PCC_params.jl")
include("params/DAC_params.jl")
include("params/compress_params.jl")
include("params/cost_params.jl")
include("params/start_up_params.jl")
include("params/sets_indices.jl")

# ------------------------------------------------------------------------------

# import modules
println("Importing modules...")

using JuMP
using Gurobi
using DataFrames
using CSV

include("variables.jl")
include("constraints/operation_mode_logic.jl")
include("constraints/disaggregated_constraints.jl")
include("constraints/overall_var_constraints.jl")
include("constraints/PCC_constraints.jl")
include("constraints/power_constraints.jl")
include("constraints/steam_split.jl")
include("constraints/compress_vent_constraints.jl")
include("constraints/DAC_constraints.jl")
include("constraints/DAC_costing_constraints.jl")
include("constraints/OM_costing.jl")
include("obj.jl")
include("output/output.jl")

# ------------------------------------------------------------------------------

# scenario generation: CO2 price + electricity price signal

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
scenarios_1 = vec(collect(Iterators.product(CO2_credits, scenario_names)))

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
scenarios_2 = vec(collect(Iterators.product(CO2_credits, scenario_names)))

full_scenarios = vcat(scenarios_1, scenarios_2)

# single scenario array for test
test_scenarios = [(100, "MiNg_100_NYISO")]

if SCENARIOS == "ALL"
    scenarios = full_scenarios
else
    scenarios = test_scenarios
end

# ------------------------------------------------------------------------------

for (CO2_credit, scenario_name) in scenarios

    # refer to global variables
    global SCENARIO_NAME = scenario_name
    global CO2_CREDIT = CO2_credit

    println("\n" * "-" ^ 80)
    println("Scenario: " * SCENARIO_NAME * "\t\tCO2 credit: " * string(CO2_CREDIT))

    # cost parameters
    # power price profile, USD/MWh
    df_power_price = DataFrame(CSV.File("src/resources/overall-price-signals.csv"))
    # dropna
    df_power_price = dropmissing(df_power_price)
    global power_price =(df_power_price[!, SCENARIO_NAME])

    # total hours
    global n_hour = 24 * 364
    # set of hours
    global set_hour_0 = 0:n_hour  # start from 0
    global set_hour = 1:n_hour  # start from 1

    # start-up cost, $
    # CO2 emission during start-up: 100.45 tonne
    # fuel consumption during start-up: 16958.58 MMBtu
    global cost_start_up = 100.45 * CO2_CREDIT + 16958.58 * cost_NG

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # construct model
    println("Constructing model...")
    m = Model()

    declare_variables(m)

    add_operation_mode_logic_constraints(m)
    add_disaggregated_constraints(m)
    add_overall_var_constraints(m)
    add_PCC_constraints(m)
    add_power_constraints(m)
    add_steam_split_constraints(m)
    add_compress_vent_constraints(m)
    add_DAC_constraints(m)
    add_DAC_costing_constraints(m)
    add_OM_costing_constraints(m)

    add_objective_function(m)

    # --------------------------------------------------------------------------
    # print model status

    print("Variable #\t")
    println(num_variables(m))
    print("Constraint #\t")
    println(sum(num_constraints(m, F, S) for (F, S) in list_of_constraint_types(m)))
    println()

    # --------------------------------------------------------------------------

    # set optimizer options
    set_optimizer(m, Gurobi.Optimizer)
    set_optimizer_attribute(m, "MIPGap", GAP)

    # specify branch priority: y first
    y = m[:y]
    for i in set_hour_0
        Gurobi.MOI.set(m, Gurobi.VariableAttribute("BranchPriority"), y[i], 1)
    end

    # set time limit
    set_time_limit_sec(m, TIME_LIMIT)

    # solve the problem
    optimize!(m)

    println("solving time: ", round(solve_time(m), digits=0), " s")

    # --------------------------------------------------------------------------

    # output results

    write_results(m, PREFIX, SUFFIX)
    # write_results(m)
    println("-" ^ 80 * "\n")

end