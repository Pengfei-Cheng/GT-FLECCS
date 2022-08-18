function gen_operation_cost_df(m)

    x_fuel = m[:x_fuel]
    x_vent_CO2 = m[:x_vent_CO2]
    x_compress_CO2 = m[:x_compress_CO2]
    x_power_out = m[:x_power_out]
    VOM_NGCC = m[:VOM_NGCC]
    VOM_PCC = m[:VOM_PCC]
    VOM_DAC = m[:VOM_DAC]
    VOM_PCC_compressor = m[:VOM_PCC_compressor]
    VOM_DAC_compressor = m[:VOM_DAC_compressor]

    vars = [
        "fuel_cost", 
        "CO2_credit",
        "CO2_transportation_cost",
        "power_profit",
        "VOM_NGCC",
        "VOM_PCC",
        "VOM_DAC",
        "VOM_PCC_compressor",
        "VOM_DAC_compressor"
    ]

    df_cost = DataFrame(map(generate_row_map, vars))

    for i in 0:n_hour
        fuel_cost = cost_NG * value(x_fuel[i])
        CO2_credit = CO2_CREDIT * value(x_vent_CO2[i])
        cost_CO2_transportation_t = cost_CO2_transportation * value(x_compress_CO2[i])
        power_profit = power_price[i + 1] * value(x_power_out[i])
        VOM_NGCC_t = value(VOM_NGCC[i])
        VOM_PCC_t = value(VOM_PCC[i])
        VOM_DAC_t = value(VOM_DAC[i])
        VOM_PCC_compressor_t = value(VOM_PCC_compressor[i])
        VOM_DAC_compressor_t = value(VOM_DAC_compressor[i])
        push!(df_cost, (fuel_cost, CO2_credit, cost_CO2_transportation_t,
                        power_profit, VOM_NGCC_t, VOM_PCC_t, VOM_DAC_t,
                        VOM_PCC_compressor_t, VOM_DAC_compressor_t))
    end

    return df_cost

end