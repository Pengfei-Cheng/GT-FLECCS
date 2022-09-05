"""
Modeling module
Declare variables.

Pengfei Cheng

1. overall variables
        combustion turbine          steam turbine               power

2. operation mode logic variables
        lambda                      y                           z0

3. disaggregated variables
4. VOM

UPDATE:
        04-13-2022: updated variables for B31A.
"""

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

function declare_variables(m)
    # 1. OVERALL VARIABLES
    #    indexed by hour
    #    basic variables that describe the operations of each unit.

    # 1.1 COMBUSTION TURBINE
    # overall load factor, from 0 to 100 (as sum of single GT load factor)
    @variable(m, 0 <= x_load[set_hour_0] <= 100)
    # overall power produced by GTs
    @variable(m, 0 <= x_power_GT[set_hour_0])
    # natural gas fuel rate
    @variable(m, 0 <= x_fuel[set_hour_0])
    # CO2 emission from burning natural gas
    @variable(m, 0 <= x_CO2_flue[set_hour_0])

    # 1.2 STEAM TURBINE
    # power generation from all steam turbines
    @variable(m, 0 <= x_power_ST[set_hour_0])

    # 1.3 POWER
    # total power (sum of GTs and STs)
    @variable(m, 0 <= x_power_total[set_hour_0])
    # net power out
    @variable(m, 0 <= x_power_net[set_hour_0])
    # total auxiliary power
    @variable(m, 0 <= x_power_aux[set_hour_0])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # 2. OPERATION MODEL LOGIC VARIABLES
    #    indexed by hour

    # convex weight of each extreme point (50, 100) for dispatch mode
    # continuous, 0 to 1
    @variable(m, 0 <= lambda[set_hour_0, x_range_extreme_points] <= 1)

    # if plant is on
    # binary
    @variable(m, y[set_hour_0], Bin, start = 1)

    # if plant starts up at hour i
    # binary
    @variable(m, z0[set_hour_0], Bin, start = 0)

    # if plant is during the start-up period
    # binary
    @variable(m, z[set_hour_0], Bin, start = 0)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # 3. disaggregated VARIABLES
    #    indexed by hour and mode (start-up, or normal dispatch)

    @variable(m, 0 <= x_load_D[set_hour_0, set_mode])
    @variable(m, 0 <= x_power_D_ST[set_hour_0, set_mode])
    @variable(m, 0 <= x_power_D_aux[set_hour_0, set_mode])
    @variable(m, 0 <= x_fuel_D[set_hour_0, set_mode])
    @variable(m, 0 <= x_CO2_D_flue[set_hour_0, set_mode])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # 4. VOMs, $
    @variable(m, 0 <= x_cost_NGCC_VOM[set_hour_0])
end