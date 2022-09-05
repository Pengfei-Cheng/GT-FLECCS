"""
Modeling module
Declare disaggregated variable constraints.

Pengfei Cheng

1.  convex combination of lambda = x_load_D (at dispatch mode)
2.  load factor during start-up
3.  load big-M

4.  fuel rate at dispatch mode
5.  fuel rate at start-up

6.  CO2 emission rate at dispatch mode
7.  CO2 emission rate at start-up

8.  constraints for other disaggregated variables at each mode (8)
        steam turbine power     auxiliary power
"""

function add_disaggregated_constraints(m)

    lambda = m[:lambda]
    x_load_D = m[:x_load_D]
    z0 = m[:z0]
    y = m[:y]
    x_fuel_D = m[:x_fuel_D]
    x_CO2_D_flue = m[:x_CO2_D_flue]
    x_power_D_ST = m[:x_power_D_ST]
    x_power_D_aux = m[:x_power_D_aux]

    # 1. CONVEX COMBINATION OF LAMBDA = X_LOAD_D (AT DISPATCH MODE)
    #    load factor is a convex combination of extreme points
    @constraint(
        m, eq_load_range_dispatch[i = set_hour_0],
        sum(lambda[i, k] * x_range[k] for k in x_range_extreme_points) 
        == 
        x_load_D[i, dispatch_idx]
    )

    # --------------------------------------------------------------------------

    # 2. LOAD DURING START-UP
    @constraint(
        m, eq_load_start_up[i = set_hour_0],
        x_load_D[i, start_up_idx] 
        == 
        sum((z0[i - k + 1]) * load_trajectory[k] for k in set_start_up_hour if i - k + 1>= 0)
    )

    # --------------------------------------------------------------------------

    # 3. LOAD BIG-M
    # for both modes, x_load_D = 0 when y = 0
    @constraint(
        m, eq_off_mode_load[i = set_hour_0, j = set_mode],
        x_load_D[i, j] 
        <= 
        100 * y[i]
    )

    # --------------------------------------------------------------------------

    # 4. FUEL RATE AT DISPATCH MODE
    @constraint(m, eq_fuel_dispatch[i = set_hour_0],
        x_fuel_D[i, dispatch_idx]
        ==
        a_fuel * x_load_D[i, dispatch_idx]
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
        x_CO2_D_flue[i, dispatch_idx]
        ==
        a_CO2_flue * x_load_D[i, dispatch_idx]
    )
    # --------------------------------------------------------------------------

    # 7. CO2 EMISSION RATE AT START-UP
    @constraint(
        m, eq_emission_start_up[i = set_hour_0], 
        x_CO2_D_flue[i, start_up_idx]
        ==
        0
    )

    # --------------------------------------------------------------------------

    # 8. CONSTRAINTS FOR OTHER disaggregated VARIABLES AT EACH MODE

    # steam turbine power
    @constraint(
        m, eq_power_ST_dispatch[i = set_hour_0],
        x_power_D_ST[i, dispatch_idx]
        ==
        a_power_ST * x_load_D[i, dispatch_idx]
    )

    @constraint(
        m, eq_power_ST_start_up[i = set_hour_0],
        x_power_D_ST[i, start_up_idx]
        ==
        0
    )

    # auxiliary power
    @constraint(
        m, eq_auxiliary_power_dispatch[i = set_hour_0], 
        x_power_D_aux[i, dispatch_idx]
        ==
        a_power_aux * x_load_D[i, dispatch_idx]
    )
    @constraint(
        m, eq_auxiliary_power_start_up[i = set_hour_0], 
        x_power_D_aux[i, start_up_idx]
        ==
        0
    )

end