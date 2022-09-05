function gen_operation_cost_df(m)

    x_fuel = m[:x_fuel]
    x_CO2_cap_total = m[:x_CO2_cap_total]
    x_CO2_compress = m[:x_CO2_compress]
    x_power_net = m[:x_power_net]
    x_cost_NGCC_VOM = m[:x_cost_NGCC_VOM]
    x_cost_PCC_VOM = m[:x_cost_PCC_VOM]
    x_cost_DAC_VOM = m[:x_cost_DAC_VOM]
    x_cost_PCC_compr_VOM = m[:x_cost_PCC_compr_VOM]
    x_cost_DAC_compr_VOM = m[:x_cost_DAC_compr_VOM]

    vars = [
        "fuel_cost", 
        "CO2_credit",
        "CO2_transportation_cost",
        "power_profit",
        "x_cost_NGCC_VOM",
        "x_cost_PCC_VOM",
        "x_cost_DAC_VOM",
        "x_cost_PCC_compr_VOM",
        "x_cost_DAC_compr_VOM"
    ]

    df_cost = DataFrame(map(generate_row_map, vars))

    for i in set_hour
        fuel_cost = cost_NG * value(x_fuel[i])
        CO2_credit = CO2_CREDIT * value(x_CO2_cap_total[i])
        cost_CO2_TS_t = a_cost_CO2_TS * value(x_CO2_compress[i])
        power_profit = power_price[i] * value(x_power_net[i])
        cost_NGCC_VOM_t = value(x_cost_NGCC_VOM[i])
        cost_PCC_VOM_t = value(x_cost_PCC_VOM[i])
        cost_DAC_VOM_t = value(x_cost_DAC_VOM[i])
        cost_PCC_compr_VOM_t = value(x_cost_PCC_compr_VOM[i])
        cost_DAC_compr_VOM_t = value(x_cost_DAC_compr_VOM[i])
        push!(df_cost, (fuel_cost, CO2_credit, cost_CO2_TS_t,
                        power_profit, cost_NGCC_VOM_t, cost_PCC_VOM_t, cost_DAC_VOM_t,
                        cost_PCC_compr_VOM_t, cost_DAC_compr_VOM_t))
    end

    return df_cost

end