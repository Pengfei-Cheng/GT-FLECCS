function gen_operation_cost_df(m)

    x_fuel = m[:x_fuel]
    x_CO2_flue = m[:x_CO2_flue]
    x_power_net = m[:x_power_net]
    x_cost_NGCC_VOM = m[:x_cost_NGCC_VOM]

    vars = [
        "fuel_cost", 
        "CO2_penalty",
        "power_profit",
        "x_cost_NGCC_VOM",
    ]

    df_cost = DataFrame(map(generate_row_map, vars))

    for i in set_hour
        fuel_cost = cost_NG * value(x_fuel[i])
        CO2_penalty = CO2_CREDIT * value(x_CO2_flue[i])
        power_profit = power_price[i] * value(x_power_net[i])
        x_cost_NGCC_VOM_t = value(x_cost_NGCC_VOM[i])
        push!(df_cost, (fuel_cost, CO2_penalty, power_profit, x_cost_NGCC_VOM_t))
    end

    return df_cost
end