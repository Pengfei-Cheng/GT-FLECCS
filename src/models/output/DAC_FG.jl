function gen_DAC_FG_df(m)

    vars = [
        "time",
        "x_f_FG", "x_s_FG", "x_A0_FG", "x_A1_FG", "x_R0_FG", "x_R1_FG"
    ]

    df_DAC_FG = DataFrame(map(generate_row_map, vars))

    for i in 0:n_hour

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

            push!(df_DAC_FG, l0)

        end
    end

    return df_DAC_FG

end