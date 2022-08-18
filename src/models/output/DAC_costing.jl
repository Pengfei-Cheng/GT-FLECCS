function gen_DAC_cost_df(m)

    vars = [
        "x_sorbent_m_DAC_FG", "x_sorbent_m", "cost_sorbent",
        "x_adsorb_max_air_rate_FG", "x_adsorb_max_air_rate_air",
        "cost_adsorb_system", "TPC_DAC"
    ]

    df_DAC_costing = DataFrame(map(generate_row_map, vars))

    l0 = []
    for v in vars
        l0 = vcat(l0, value(m[Symbol(v)]))
    end
    push!(df_DAC_costing, l0)

    return df_DAC_costing

end