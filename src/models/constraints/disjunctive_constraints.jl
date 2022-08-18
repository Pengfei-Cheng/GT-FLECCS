"""
Modeling module
Declare disjunctive variable constraints.

Pengfei Cheng

1.  convex combination of lambda = x_load_factor_D (at dispatch mode)
2.  load factor during start-up
3.  load big-M

4.  fuel rate at dispatch mode
5.  fuel rate at start-up

6.  CO2 emission rate at dispatch mode
7.  CO2 emission rate at start-up

8.  constraints for other disjunctive variables at each mode (8)
        HP steam turbine power  IP steam turbine power
        DAC base steam          allocable steam
"""

function add_disjunctive_constraints(m)
    lambda = m[:lambda]
    x_load_factor_D = m[:x_load_factor_D]
    z = m[:z]
    z2 = m[:z2]
    y = m[:y]
    x_fuel_D = m[:x_fuel_D]
    x_emission_D = m[:x_emission_D]
    x_power_HP_D = m[:x_power_HP_D]
    x_power_IP_D = m[:x_power_IP_D]
    x_power_aux_D = m[:x_power_aux_D]
    x_steam_DAC_base_D = m[:x_steam_DAC_base_D]
    x_steam_allocable_D = m[:x_steam_allocable_D]

    # 1. CONVEX COMBINATION OF LAMBDA = X_LOAD_FACTOR_D (AT DISPATCH MODE)
    #    load factor is a convex combination of extreme points
    @constraint(
        m, eq_load_range_dispatch[i = set_hour_0],
        sum(lambda[i, k] * x_range[k] for k in x_range_extreme_points) 
        == 
        x_load_factor_D[i, dispatch_idx]
    )

    # --------------------------------------------------------------------------

    # 2. LOAD DURING START-UP
    @constraint(
        m, eq_load_start_up[i = set_hour_0],
        x_load_factor_D[i, start_up_idx] 
        == 
        sum((z[i - k + 1]) * load_trajectory[k] for k in set_start_up_hour if i - k + 1>= 0)
    )

    # --------------------------------------------------------------------------

    # 3. LOAD BIG-M
    # for both modes, x_load_factor_D = 0 when y = 0
    @constraint(
        m, eq_off_mode_load[i = set_hour_0, j = set_mode],
        x_load_factor_D[i, j] 
        <= 
        100 * y[i]
    )

    # --------------------------------------------------------------------------

    # 4. FUEL RATE AT DISPATCH MODE
    @constraint(m, eq_fuel_dispatch[i = set_hour_0],
        x_fuel_D[i, dispatch_idx]
        ==
        a_fuel * x_load_factor_D[i, dispatch_idx] + b_fuel * (y[i] - z2[i])
    )

    # --------------------------------------------------------------------------

    # 5. FUEL RATE AT START-UP
    @constraint(m, eq_fuel_start_up[i = set_hour_0], 
        x_fuel_D[i, start_up_idx]
        ==
        0
    )

    # --------------------------------------------------------------------------

    # 6. CO2 EMISSION RATE AT DISPATCH MODE
    @constraint(
        m, eq_emission_dispatch[i = set_hour_0],
        x_emission_D[i, dispatch_idx]
        ==
        a_emission * x_load_factor_D[i, dispatch_idx] + b_emission * (y[i] - z2[i])
    )
    # --------------------------------------------------------------------------

    # 7. CO2 EMISSION RATE AT START-UP
    @constraint(
        m, eq_emission_start_up[i = set_hour_0], 
        x_emission_D[i, start_up_idx]
        ==
        0
    )

    # --------------------------------------------------------------------------

    # 13. CONSTRAINTS FOR OTHER DISJUNCTIVE VARIABLES AT EACH MODE

    # HP steam turbine power
    @constraint(
        m, eq_power_HP_dispatch[i = set_hour_0],
        x_power_HP_D[i, dispatch_idx]
        ==
        a_power_HP * x_load_factor_D[i, dispatch_idx] + b_power_HP * (y[i] - z2[i])
    )

    @constraint(
        m, eq_power_HP_start_up[i = set_hour_0],
        x_power_HP_D[i, start_up_idx]
        ==
        0
    )

    # IP steam turbine power
    @constraint(
        m, eq_power_IP_dispatch[i = set_hour_0],
        x_power_IP_D[i, dispatch_idx]
        ==
        a_power_IP * x_load_factor_D[i, dispatch_idx] + b_power_IP * (y[i] - z2[i])
    )
    @constraint(
        m, eq_power_IP_start_up[i = set_hour_0],
        x_power_IP_D[i, start_up_idx]
        ==
        0
    )

    # DAC base steam
    @constraint(
        m, eq_DAC_base_steam_dispatch[i = set_hour_0],
        x_steam_DAC_base_D[i, dispatch_idx]
        ==
        a_DAC_base_steam * x_load_factor_D[i, dispatch_idx] + b_DAC_base_steam * (y[i] - z2[i])
    )
    @constraint(
        m, eq_DAC_base_steam_start_up[i = set_hour_0],
        x_steam_DAC_base_D[i, start_up_idx]
        ==
        0
    )

    # allocable steam
    @constraint(
        m, eq_allocable_steam_dispatch[i = set_hour_0],
        x_steam_allocable_D[i, dispatch_idx]
        ==
        a_allocable_steam * x_load_factor_D[i, dispatch_idx] + b_allocable_steam * (y[i] - z2[i])
        # (a_allocable_steam * x_load_factor_D[i, dispatch_idx] + b_allocable_steam * y[i])
    )
    @constraint(
        m, eq_allocable_steam_start_up[i = set_hour_0],
        x_steam_allocable_D[i, start_up_idx]
        ==
        0
    )

    # auxiliary power
    @constraint(
        m, eq_auxiliary_power_dispatch[i = set_hour_0], 
        x_power_aux_D[i, dispatch_idx]
        ==
        a_aux_power * x_load_factor_D[i, dispatch_idx] + b_aux_power * (y[i] - z2[i])
    )
    @constraint(
        m, eq_auxiliary_power_start_up[i = set_hour_0], 
        x_power_aux_D[i, start_up_idx]
        ==
        0
    )
end