function gen_steam_df(m)

    vars = [
        "x_steam_PCC",
        "x_steam_DAC_total", "x_steam_DAC",
        "x_steam_DAC_slack", "x_steam_allocable", "x_steam_DAC_base",
        "x_steam_DAC_extra", "x_steam_for_LP"
    ]

    df_steam = DataFrame(map(generate_row_map, vars))

    for i in 0:n_hour

        local l0 = []

        for v in vars
            s = Symbol(v)

            if v == "x_steam_DAC"
                l0 = vcat(l0, sum(value(m[s][i, j]) for j in set_quarter))
            else
                l0 = vcat(l0, value(m[s][i]))
            end
        end

        push!(df_steam, l0)
    end

    return df_steam

end