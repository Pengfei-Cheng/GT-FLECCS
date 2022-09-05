"""
Modeling module
Declare overall variable constraints (as sum of unit variables).

Pengfei Cheng

1. constraints for overall variables (8)
        load factor             fuel rate               CO2 emission rate
        steam turbine power     auxiliary power
"""

function add_overall_var_constraints(m)
    x_load = m[:x_load]
    x_load_D = m[:x_load_D]
    x_fuel = m[:x_fuel]
    x_fuel_D = m[:x_fuel_D]
    x_CO2_flue = m[:x_CO2_flue]
    x_CO2_D_flue = m[:x_CO2_D_flue]
    x_power_ST = m[:x_power_ST]
    x_power_D_ST = m[:x_power_D_ST]
    x_power_aux = m[:x_power_aux]
    x_power_D_aux = m[:x_power_D_aux]

    # 1. CONSTRAINTS FOR OVERALL VARIABLES

    # load factor
    @constraint(
        m ,eq_total_load_factor[i = set_hour_0],
        x_load[i]
        ==
        sum(x_load_D[i, mode] for mode in set_mode)
    )

    # fuel consumption
    @constraint(
        m, eq_total_fuel_rate[i = set_hour_0], 
        x_fuel[i]
        ==
        sum(x_fuel_D[i, mode] for mode in set_mode)
    )

    # CO2 emission rate
    @constraint(
        m, eq_total_CO2_emission_rate[i = set_hour_0], 
        x_CO2_flue[i]
        ==
        sum(x_CO2_D_flue[i, mode] for mode in set_mode)
    )

    # steam turbine power
    @constraint(
        m, eq_total_power_ST[i = set_hour_0], 
        x_power_ST[i]
        ==
        sum(x_power_D_ST[i, mode] for mode in set_mode)
    )

    # auxiliary power
    @constraint(
        m, eq_total_power_aux[i = set_hour_0], 
        x_power_aux[i]
        ==
        sum(x_power_D_aux[i, mode] for mode in set_mode)
    )

end