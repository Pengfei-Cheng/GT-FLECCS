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
    x_CO2_PCC = m[:x_CO2_PCC]
    x_CO2_flue = m[:x_CO2_flue]
    x_CO2_PCC_out = m[:x_CO2_PCC_out]
    x_steam_PCC = m[:x_steam_PCC]
    x_power_PCC = m[:x_power_PCC]

    # 1. PCC CO2 CAPTURE
    @constraint(
        m, eq_PCC_CO2_cap[i = set_hour_0], 
        x_CO2_PCC[i]
        ==
        a_CO2_PCC * x_CO2_flue[i]
    )

    # --------------------------------------------------------------------------

    # 2. PCC CO2 OUTLET CONCENTRATION
    @constraint(
        m, eq_PCC_CO2_out[i = set_hour_0], 
        x_CO2_PCC_out[i]
        ==
        x_CO2_flue[i] - x_CO2_PCC[i]
    )

    # --------------------------------------------------------------------------

    # 3. PCC STEAM USAGE
    @constraint(
        m, eq_PCC_steam[i = set_hour_0], 
        x_steam_PCC[i]
        ==
        a_steam_PCC * x_CO2_PCC[i]
    )

    # --------------------------------------------------------------------------

    # 4. PCC POWER USAGE
    @constraint(
        m, eq_PCC_power[i = set_hour_0], 
        x_power_PCC[i]
        ==
        a_power_PCC * x_CO2_PCC[i]
    )
end