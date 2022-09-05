function gen_disaggregated_var_df(m)

    var = [
        "x_load_D", "x_fuel_D", "x_CO2_D_flue",
        "x_power_D_HP", "x_power_D_IP", "x_power_D_aux",
        "x_steam_D_DAC_base", "x_steam_D_allocable"
    ]

    l = []
    for v in var
        l = vcat(l, [v * string(mod) => Float64[] 
            for mod in set_mode])
    end

    df_disaggregated_vars = DataFrame(l)

    for i in set_hour
        local l0 = []
        for v in var
            s = Symbol(v)
            local l = [value(m[s][i, mod]) for mod in set_mode]
            l0 = vcat(l0, l)
        end
        push!(df_disaggregated_vars, l0)
    end

    return df_disaggregated_vars

end