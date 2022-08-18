function gen_disjunctive_var_df(m)

    var = [
        "x_load_factor_D", "x_fuel_D", "x_emission_D",
        "x_power_HP_D", "x_power_IP_D", "x_power_aux_D",
        "x_steam_DAC_base_D", "x_steam_allocable_D"
    ]

    l = []
    for v in var
        l = vcat(l, [v * string(mod) => Float64[] 
            for mod in set_mode])
    end

    df_disjunctive_vars = DataFrame(l)

    for i in 0:n_hour
        local l0 = []
        for v in var
            s = Symbol(v)
            local l = [value(m[s][i, mod]) for mod in set_mode]
            l0 = vcat(l0, l)
        end
        push!(df_disjunctive_vars, l0)
    end

    return df_disjunctive_vars

end