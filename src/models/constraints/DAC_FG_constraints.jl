"""
Modeling module
Declare DAC-FG-related constraints.

Pengfei Cheng

DAC-related variables must start at 0 and end at 1-n_slice.

WARNING: This module is not in use for a while. Double check the constraints
before activating them as they may not be correct.

Assumptions: 
    1. DAC-FG takes one time slot (15 min) for adsorption

1. state equation
            x_A1_FG            x_R1_FG
            x_f_FG             x_s_FG
2. continuity of states
            x_A1_FG            x_R1_FG
            x_f_FG             x_s_FG
3. initial conditions
            x_A1_FG            x_R1_FG
            x_f_FG             x_s_FG
4. end conditions
            x_A1_FG            x_R1_FG
            x_f_FG             x_s_FG
5. CO2 capture
6. steam usage
7. power usage
8. vented CO2 (for FG)
9. DAC-FG CO2 inlet concentration
"""

# STATE EQUATION

function add_DAC_FG_constraints(m)

    x_A0_FG = m[:x_A0_FG]
    x_A1_FG = m[:x_A1_FG]
    x_R0_FG = m[:x_R0_FG]
    x_R1_FG = m[:x_R1_FG]
    x_f_FG = m[:x_f_FG]
    x_s_FG = m[:x_s_FG]
    x_sorbent_m_DAC_FG = m[:x_sorbent_m_DAC_FG]
    x_DAC_FG_CO2_cap = m[:x_DAC_FG_CO2_cap]
    x_DAC_FG_steam = m[:x_DAC_FG_steam]
    x_DAC_FG_power = m[:x_DAC_FG_power]
    x_DAC_FG_CO2_vent = m[:x_DAC_FG_CO2_vent]
    x_CO2_DAC_FG_in = m[:x_CO2_DAC_FG_in]
    x_CO2_PCC_out = m[:x_CO2_PCC_out]
    x_CO2_PCC_vent = m[:x_CO2_PCC_vent]

    # x_A1_FG
    @constraint(
        m, eq_DAC_FG_A1_state[i = set_hour_0, j=set_quarter], 
        x_A1_FG[i, j + 1]
        ==
        x_A0_FG[i, j]
    )

    # x_R1_FG
    @constraint(
        m, eq_DAC_FG_R1_state[i = set_hour_0, j=set_quarter], 
        x_R1_FG[i, j + 1]
        ==
        x_R0_FG[i, j]
    )

    # x_f_FG
    @constraint(
        m, eq_DAC_FG_f_state[i = set_hour_0, j = set_quarter], 
        x_f_FG[i, j + 1]
        ==
        x_f_FG[i, j] - x_A0_FG[i, j] + x_R1_FG[i, j]
    )

    # x_s_FG
    @constraint(
        m, eq_DAC_FG_s_state[i = set_hour_0, j = set_quarter], 
        x_s_FG[i, j + 1]
        ==
        x_s_FG[i, j] - x_R0_FG[i, j] + x_A1_FG[i, j]
    )

    # --------------------------------------------------------------------------

    # 2. CONTINUITY OF STATES
    # connect the ending slice with the beginning slice of the next hour
    @constraint(
        m, eq_cont_x_A1_FG[i = 1:n_hour], 
        x_A1_FG[i, 0]
        ==
        x_A1_FG[i - 1, n_slice]
    )
    @constraint(
        m, eq_cont_x_R1_FG[i = 1:n_hour], 
        x_R1_FG[i, 0]
        ==
        x_R1_FG[i - 1, n_slice]
    )
    @constraint(
        m, eq_cont_x_f_FG[i = 1:n_hour], 
        x_f_FG[i, 0]
        ==
        x_f_FG[i - 1, n_slice]
    )
    @constraint(
        m, eq_cont_x_s_FG[i = 1:n_hour], 
        x_s_FG[i, 0]
        ==
        x_s_FG[i - 1, n_slice]
    )

    # --------------------------------------------------------------------------

    # 3. INITIAL CONDITIONS
    @constraint(m, eq_DAC_FG_x_A1_init, x_A1_FG[0, 0] == 0.)
    @constraint(m, eq_DAC_FG_E1_init, x_R1_FG[0, 0] == 0.)
    @constraint(m, eq_DAC_FG_cap_init, x_f_FG[0, 0] == x_sorbent_m_DAC_FG)
    @constraint(m, eq_DAC_FG_f_init, x_s_FG[0, 0] == 0.)

    # --------------------------------------------------------------------------

    # 4. END CONSTRAINTS
    # David: we need to get rid of them and then put them back (?)
    @constraint(m, eq_DAC_FG_x_A1_end, x_A1_FG[n_hour, n_slice] == 0.)
    @constraint(m, eq_DAC_FG_x_R1_end, x_R1_FG[n_hour, n_slice] == 0.)
    @constraint(m, eq_DAC_FG_x_f_end, x_f_FG[n_hour, n_slice] == x_sorbent_m_DAC_FG)
    @constraint(m, eq_DAC_FG_s_end, x_s_FG[n_hour, n_slice] == 0.)

    # --------------------------------------------------------------------------

    # 5. CO2 CAPTURE
    @constraint(
        m, eq_DAC_FG_CO2_cap[i = set_hour_0, j = set_quarter], 
        x_DAC_FG_CO2_cap[i, j] == 
        #sorbent_cap_DAC_FG * x_R1_FG[i, j]
        sorbent_cap_DAC_FG * x_A1_FG[i, j]
    )

    # --------------------------------------------------------------------------

    # 6. STEAM USAGE
    @constraint(
        m, eq_DAC_FG_steam[i = set_hour_0, j = set_quarter], 
        x_DAC_FG_steam[i, j] == 
        #a_DAC_FG_steam * x_DAC_FG_CO2_cap[i, j]
        a_DAC_FG_steam * sorbent_cap_DAC_FG * x_R1_FG[i, j]
    )

    # --------------------------------------------------------------------------

    # 7. POWER USAGE
    @constraint(
        m, eq_DAC_FG_power[i = set_hour_0, j = set_quarter], 
        x_DAC_FG_power[i, j]
        ==
        a_DAC_FG_power * x_DAC_FG_CO2_cap[i, j]
    )

    # --------------------------------------------------------------------------

    # 8. VENTED CO2 (FOR FG)
    # integral over all slices within each hour
    @constraint(
        m, eq_DAC_FG_CO2_vent[i = set_hour_0], 
        x_DAC_FG_CO2_vent[i]
        ==
        x_CO2_DAC_FG_in[i] 
        - sum(x_DAC_FG_CO2_cap[i, j] for j in  set_quarter)
    )

    # --------------------------------------------------------------------------

    # 9. DAC-FG CO2 inlet concentration
    @constraint(
        m, eq_DAC_FG_CO2_in[i = set_hour_0], 
        x_CO2_DAC_FG_in[i]
        ==
        x_CO2_PCC_out[i] - x_CO2_PCC_vent[i]
    )
end