"""
Output module
Pengfei Cheng

Output CO2-related results.
"""

function gen_CO2_df(m)

    vars = [
        "x_fuel_CO2", 
        "x_CO2_PCC_cap", "x_CO2_PCC_out", "x_CO2_PCC_vent",
        # "x_CO2_DAC_FG_in", "x_DAC_FG_CO2_cap", "x_DAC_FG_CO2_vent",
        "x_CO2_DAC_cap", "x_vent_CO2"
    ]

    df_CO2 = DataFrame(map(generate_row_map, vars))

    for i in 0:n_hour

        local l0 = []

        for v in vars
            s = Symbol(v)

            if occursin("DAC", v) && occursin("cap", v)
                l0 = vcat(l0, sum(value(m[s][i, j]) for j in set_quarter))
            else
                l0 = vcat(l0, value(m[s][i]))
            end
        end

        push!(df_CO2, l0)
    end

    return df_CO2

end