function gen_DAC_air_df(m)

    vars = [
        "time",
        "x_sorbent_F", "x_sorbent_S", "x_sorbent_A0", "x_sorbent_A1", "x_sorbent_R"
    ]

    df_DAC_air = DataFrame(map(generate_row_map, vars))

    for i in set_hour

        for j in set_quarter

            local l0 = []

            for v in vars
                if v == "time"
                    l0 = vcat(l0, i + j * 1 / n_slice)
                else
                    s = Symbol(v)
                    l0 = vcat(l0, value(m[s][i, j]))
                end
            end

            push!(df_DAC_air, l0)

        end
    end

    return df_DAC_air

end