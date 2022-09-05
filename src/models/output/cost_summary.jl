"""
Output module
Pengfei Cheng

Create the DataFrame for cost terms.
"""

function gen_cost_summary_df(m, df_operation_cost, df_binary)

    # output DataFrame
    vars = ["profit", "power sell", "fuel cost", "CO2 penalty", "VOM", "FOM", "start up"]
    df_cost_summary = DataFrame(map(generate_row_map, vars))
    annual_net_earnings = (objective_value(m) - 19465868 )
    annual_power_sell = sum(df_operation_cost[!, "power_profit"])
    annual_fuel_cost = sum(df_operation_cost[!, "fuel_cost"])
    annual_CO2_penalty = sum(df_operation_cost[!, "CO2_penalty"])
    annual_VOM = sum(df_operation_cost[!, "x_cost_NGCC_VOM"])
    annual_FOM = 19465868
    annual_start_up = cost_start_up * sum(df_binary[!, "z0"])
    # minus FOM
    push!(df_cost_summary, [annual_net_earnings, annual_power_sell, annual_fuel_cost,
                annual_CO2_penalty, annual_VOM, annual_FOM, annual_start_up])

    return df_cost_summary
end