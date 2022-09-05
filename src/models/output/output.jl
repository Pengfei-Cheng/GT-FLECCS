"""
Output module
Pengfei Cheng

Centralized output module.
"""

using DataFrames
using CSV
using Dates

function generate_row_map(s)
    return s => Float64[]
end

include("binary.jl")
include("CO2.jl")
include("operation_cost.jl")
include("disaggregated_vars.jl")
include("power.jl")
include("cost_summary.jl")

# ------------------------------------------------------------------------------

function write_results(m::JuMP.Model, output_prefix::String="", output_suffix::String="")

    df_binary = gen_binary_df(m)
    df_CO2 = gen_CO2_df(m)
    df_power = gen_power_df(m)
    df_operation_cost = gen_operation_cost_df(m)
    df_obj = gen_cost_summary_df(m, df_operation_cost, df_binary)
    df_disaggregated_vars = gen_disaggregated_var_df(m)

    # set output path
    rel_path = string(CO2_CREDIT) * "-" * SCENARIO_NAME
    if output_prefix != ""
        rel_path = output_prefix * "-" * rel_path
    end
    if output_suffix != ""
        rel_path = rel_path * "-" * output_suffix
    end

    # create results folder if it doesn't exist
    if !isdir("results")
        mkdir("results")
    end

    # create B31A folder if it doesn't exist
    if !isdir("results/B31A")
        mkdir("results/B31A")
    end

    rel_path = "results/B31A/" * rel_path
    # create folder when it does not exist
    if !isdir(rel_path)
        mkdir(rel_path)
    end
    # write CSV
    dfs = Dict([
        ("results_CO2", df_CO2),
        ("results_power", df_power),
        ("results_cost", df_operation_cost),
        ("results_binary_vars", df_binary),
        ("results_disaggregated", df_disaggregated_vars),
        ("obj_value", df_obj)
        ])
    for (idx, var) in dfs
        output_name = string(idx, ".csv")
        CSV.write(joinpath(rel_path, output_name), var)
    end

end