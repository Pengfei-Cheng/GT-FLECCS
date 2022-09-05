function gen_DAC_cost_df(m)

    vars = [
        "x_sorbent_total", "x_cost_sorbent",
        "x_air_adsorb_max",
        "x_cost_adsorb", "x_cost_DAC_TPC"
    ]

    df_DAC_costing = DataFrame(map(generate_row_map, vars))

    l0 = []
    for v in vars
        l0 = vcat(l0, value(m[Symbol(v)]))
    end
    push!(df_DAC_costing, l0)

    return df_DAC_costing

end