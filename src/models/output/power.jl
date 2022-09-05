function gen_power_df(m)

    vars = [
        "x_load", "x_power_GT", "x_power_ST",
        "x_power_aux", "x_power_total", "x_power_net"
    ]

    df_power = DataFrame(map(generate_row_map, vars))

    for i in set_hour

        l0 = []

        for v in vars
            s = Symbol(v)

            if occursin("DAC", v)
                l0 = vcat(l0, sum(value(m[s][i, j]) for j in set_hour_0_slices_minus_1))
            else
                l0 = vcat(l0, value(m[s][i]))
            end
        end

        push!(df_power, l0)
    end


    return df_power
end