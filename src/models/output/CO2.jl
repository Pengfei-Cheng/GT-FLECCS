"""
Output module
Pengfei Cheng

Output CO2-related results.
"""

function gen_CO2_df(m)

    vars = [
        "x_CO2_flue" 
    ]

    df_CO2 = DataFrame(map(generate_row_map, vars))

    for i in set_hour

        l0 = []

        for v in vars
            s = Symbol(v)

            if occursin("DAC", v) && occursin("cap", v)
                l0 = vcat(l0, sum(value(m[s][i, j]) for j in set_hour_0_slices_minus_1))
            else
                l0 = vcat(l0, value(m[s][i]))
            end
        end

        push!(df_CO2, l0)
    end

    return df_CO2
end