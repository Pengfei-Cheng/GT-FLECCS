function gen_disaggregated_var_df(m)

    var = [
        "x_load_D", "x_fuel_D", "x_CO2_D_flue",
        "x_power_D_ST", "x_power_D_aux",
    ]

    l = []
    for v in var
        l = vcat(l, [v * string(mod) => Float64[] for mod in set_mode])
    end

    df_disjunctive_vars = DataFrame(l)

    for i in 0:n_horizon
        l0 = []
        for v in var
            s = Symbol(v)
            l = [value(m[s][i, mod]) for mod in set_mode]
            l0 = vcat(l0, l)
        end
        push!(df_disjunctive_vars, l0)
    end

    return df_disjunctive_vars

end