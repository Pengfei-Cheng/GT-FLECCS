"""
Modeling module
Declare overall variable constraints (as sum of unit variables).

Pengfei Cheng

1. constraints for overall variables (8)
        load factor             fuel rate               CO2 emission rate
        HP steam turbine power  IP steam turbine power  DAC base steam
        allocable steam
"""

function add_overall_var_constraints(m)
    x_load_factor = m[:x_load_factor]
    x_load_factor_D = m[:x_load_factor_D]
    x_fuel = m[:x_fuel]
    x_fuel_D = m[:x_fuel_D]
    x_fuel_CO2 = m[:x_fuel_CO2]
    x_emission_D = m[:x_emission_D]
    x_power_HP = m[:x_power_HP]
    x_power_HP_D = m[:x_power_HP_D]
    x_power_IP = m[:x_power_IP]
    x_power_IP_D = m[:x_power_IP_D]
    x_power_aux = m[:x_power_aux]
    x_power_aux_D = m[:x_power_aux_D]
    x_steam_DAC_base = m[:x_steam_DAC_base]
    x_steam_DAC_base_D = m[:x_steam_DAC_base_D]
    x_steam_allocable = m[:x_steam_allocable]
    x_steam_allocable_D = m[:x_steam_allocable_D]
    
    # 1. CONSTRAINTS FOR OVERALL VARIABLES

    # load factor
    @constraint(
        m ,eq_total_load_factor[i = set_hour_0],
        x_load_factor[i]
        ==
        sum(x_load_factor_D[i, mode] for mode in set_mode)
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
        x_fuel_CO2[i]
        ==
        sum(x_emission_D[i, mode] for mode in set_mode)
    )

    # HP steam turbine power
    @constraint(
        m, eq_total_power_HP[i = set_hour_0], 
        x_power_HP[i]
        ==
        sum(x_power_HP_D[i, mode] for mode in set_mode)
    )

    # IP steam turbine power
    @constraint(
        m, eq_total_power_IP[i = set_hour_0], 
        x_power_IP[i]
        ==
        sum(x_power_IP_D[i, mode] for mode in set_mode)
    )

    # DAC base steam
    @constraint(
        m, eq_total_DAC_base_duty[i = set_hour_0],
        x_steam_DAC_base[i]
        ==
        sum(x_steam_DAC_base_D[i, mode] for mode in set_mode)
    )

    # allocable steam
    @constraint(
        m, eq_total_steam_allocable[i = set_hour_0],
        x_steam_allocable[i]
        ==
        # x_steam_allocable_D[i, dispatch_idx]
        sum(x_steam_allocable_D[i, mode] for mode in set_mode)
    )

    # auxiliary power
    @constraint(
        m, eq_total_power_aux[i = set_hour_0], 
        x_power_aux[i]
        ==
        sum(x_power_aux_D[i, mode] for mode in set_mode)
    )
end