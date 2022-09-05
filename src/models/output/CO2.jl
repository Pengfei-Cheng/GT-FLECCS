"""
Output module
Pengfei Cheng

Output CO2-related results.
"""

function gen_CO2_df(m)

    vars = [
        "x_CO2_flue", "x_CO2_PCC", "x_CO2_vent_PCC",
        "x_CO2_DAC", "x_CO2_cap_total"
    ]

    df_CO2 = DataFrame(map(generate_row_map, vars))

    for i in set_hour

        local l0 = []

        for v in vars
            s = Symbol(v)

            if occursin("x_CO2_DAC", v)
                l0 = vcat(l0, sum(value(m[s][i, j]) for j in set_quarter))
            else
                l0 = vcat(l0, value(m[s][i]))
            end
        end

        push!(df_CO2, l0)
    end

    return df_CO2

end