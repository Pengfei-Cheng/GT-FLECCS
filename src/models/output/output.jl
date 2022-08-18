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
include("DAC_FG.jl")
include("DAC_air.jl")
include("disjunctive_vars.jl")
include("power.jl")
include("steam.jl")
include("DAC_costing.jl")
include("NPV.jl")

# ------------------------------------------------------------------------------

function write_results(m::JuMP.Model, output_prefix::String="", output_suffix::String="")

    df_CO2 = gen_CO2_df(m)
    df_power = gen_power_df(m)
    df_steam = gen_steam_df(m)
    df_operation_cost = gen_operation_cost_df(m)
    df_DAC_FG = gen_DAC_FG_df(m)
    df_DAC_air = gen_DAC_air_df(m)
    df_disjunctive_vars = gen_disjunctive_var_df(m)
    df_binary = gen_binary_df(m)
    df_DAC_costing = gen_DAC_cost_df(m)
    df_NPV, ddf_overall_profit_cost = gen_NPV_df(m, df_operation_cost, df_binary)

    # set output path
    rel_path = string(CO2_CREDIT) * "-" * SCENARIO_NAME
    if output_prefix != ""
        rel_path = output_prefix * "-" * rel_path
    end
    if output_suffix != ""
        rel_path = rel_path * "-" * output_suffix
    end
    rel_path = "results/revamp-start-up/" * rel_path
    # create folder when it does not exist
    if !isdir(rel_path)
        mkdir(rel_path)
    end

    # write CSV
    dfs = Dict([
        ("results_CO2", df_CO2),
        ("results_power", df_power),
        ("results_steam", df_steam),
        ("results_DAC_FG", df_DAC_FG),
        ("results_DAC_air", df_DAC_air),
        ("results_operation_cost", df_operation_cost),
        ("results_binary_vars", df_binary),
        ("results_disjunctive", df_disjunctive_vars),
        ("results_DAC_costing", df_DAC_costing),
        ("NPV", df_NPV),
        ("overall_profit_cost", ddf_overall_profit_cost)
        ])
    for (idx, var) in dfs
        local output_name = string(idx, ".csv")
        CSV.write(joinpath(rel_path, output_name), var)
    end

    # --------------------------------------------------------------------------

    # output meta data
    df_meta = DataFrame(
        [
            "date" => DateTime[],
            "CO2_credit" => Float64[],
            "scenario_name" => String[],
            "solve_time" => Float64[],
            "sorbent_amount" => Float64[],
            "gap" => Float64[]
        ]
    )
    push!(df_meta, [
        Dates.now(),
        CO2_CREDIT,
        SCENARIO_NAME,
        round(solve_time(m), digits=0),
        value(m[:x_sorbent_m]),
        relative_gap(m)
        ]
    )
    
    # write to csv
    meta_file_name = "meta"
    if output_prefix != ""
        meta_file_name = output_prefix * "_" * meta_file_name
    end
    if output_suffix != ""
        meta_file_name = meta_file_name * "-" * output_suffix
    end
    meta_file = "results/revamp-start-up/" * meta_file_name * ".csv"
    if isfile(meta_file)
        CSV.write(meta_file, df_meta, append=true)
    else
        CSV.write(meta_file, df_meta)
    end

end