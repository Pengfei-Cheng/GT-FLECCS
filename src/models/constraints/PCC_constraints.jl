"""
Modeling module
Declare PCC-related constraints.

Pengfei Cheng

1. PCC CO2 capture
2. PCC CO2 outlet concentration
3. PCC steam usage
4. PCC power usage
"""

function add_PCC_constraints(m)
    x_CO2_PCC_cap = m[:x_CO2_PCC_cap]
    x_fuel_CO2 = m[:x_fuel_CO2]
    x_CO2_PCC_out = m[:x_CO2_PCC_out]
    x_steam_PCC = m[:x_steam_PCC]
    x_power_PCC = m[:x_power_PCC]

    # 1. PCC CO2 CAPTURE
    @constraint(
        m, eq_PCC_CO2_cap[i = set_hour_0], 
        x_CO2_PCC_cap[i]
        ==
        a_PCC_capture_rate * x_fuel_CO2[i]
    )

    # --------------------------------------------------------------------------

    # 2. PCC CO2 OUTLET CONCENTRATION
    @constraint(
        m, eq_PCC_CO2_out[i = set_hour_0], 
        x_CO2_PCC_out[i]
        ==
        x_fuel_CO2[i] - x_CO2_PCC_cap[i]
    )

    # --------------------------------------------------------------------------

    # 3. PCC STEAM USAGE
    # David: sometimes there is not enough steam, so we have to relax this constraint 
    @constraint(
        m, eq_PCC_steam[i = set_hour_0], 
        x_steam_PCC[i]
        ==
        a_PCC_steam_rate * x_CO2_PCC_cap[i]
    )

    # --------------------------------------------------------------------------

    # 4. PCC POWER USAGE
    @constraint(
        m, eq_PCC_power[i = set_hour_0], 
        x_power_PCC[i]
        ==
        a_PCC_power_rate * x_CO2_PCC_cap[i]
    )
end