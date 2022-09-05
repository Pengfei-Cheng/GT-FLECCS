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
    x_load = m[:x_load]
    x_load_D = m[:x_load_D]
    x_fuel = m[:x_fuel]
    x_fuel_D = m[:x_fuel_D]
    x_CO2_flue = m[:x_CO2_flue]
    x_CO2_D_flue = m[:x_CO2_D_flue]
    x_power_HP = m[:x_power_HP]
    x_power_D_HP = m[:x_power_D_HP]
    x_power_IP = m[:x_power_IP]
    x_power_D_IP = m[:x_power_D_IP]
    x_power_aux = m[:x_power_aux]
    x_power_D_aux = m[:x_power_D_aux]
    x_steam_DAC_base = m[:x_steam_DAC_base]
    x_steam_D_DAC_base = m[:x_steam_D_DAC_base]
    x_steam_allocable = m[:x_steam_allocable]
    x_steam_D_allocable = m[:x_steam_D_allocable]
    
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

    # HP steam turbine power
    @constraint(
        m, eq_total_power_HP[i = set_hour_0], 
        x_power_HP[i]
        ==
        sum(x_power_D_HP[i, mode] for mode in set_mode)
    )

    # IP steam turbine power
    @constraint(
        m, eq_total_power_IP[i = set_hour_0], 
        x_power_IP[i]
        ==
        sum(x_power_D_IP[i, mode] for mode in set_mode)
    )

    # DAC base steam
    @constraint(
        m, eq_total_DAC_base_duty[i = set_hour_0],
        x_steam_DAC_base[i]
        ==
        sum(x_steam_D_DAC_base[i, mode] for mode in set_mode)
    )

    # allocable steam
    @constraint(
        m, eq_total_steam_allocable[i = set_hour_0],
        x_steam_allocable[i]
        ==
        # x_steam_D_allocable[i, dispatch_idx]
        sum(x_steam_D_allocable[i, mode] for mode in set_mode)
    )

    # auxiliary power
    @constraint(
        m, eq_total_power_aux[i = set_hour_0], 
        x_power_aux[i]
        ==
        sum(x_power_D_aux[i, mode] for mode in set_mode)
    )
end