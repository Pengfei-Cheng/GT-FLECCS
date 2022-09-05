"""
Modeling module
Declare DAC-air-related constraints.

Pengfei Cheng

1. state equation
2. continuity of states
3. initial conditions
4. end conditions
5. CO2 capture
6. steam usage
7. power usage
8. mass balance inequalities 
"""

function add_DAC_constraints(m)
    x_sorbent_A1 = m[:x_sorbent_A1]
    x_sorbent_A0 = m[:x_sorbent_A0]
    x_sorbent_R = m[:x_sorbent_R]
    x_sorbent_F = m[:x_sorbent_F]
    x_sorbent_S = m[:x_sorbent_S]
    x_sorbent_total = m[:x_sorbent_total]
    x_CO2_DAC = m[:x_CO2_DAC]
    x_steam_DAC = m[:x_steam_DAC]
    x_power_DAC = m[:x_power_DAC]

    # 1. STATE EQUATION
    # x_sorbent_A1
    @constraint(
        m, eq_A1_state[i = set_hour_0, j = set_quarter], 
        x_sorbent_A1[i, j + 1]
        ==
        x_sorbent_A0[i, j]
    )
    # x_sorbent_F
    @constraint(
        m, eq_f_state[i = set_hour_0, j = set_quarter], 
        x_sorbent_F[i, j + 1]
        ==
        x_sorbent_F[i, j] - x_sorbent_A0[i, j] + x_sorbent_R[i, j]
    )
    # x_sorbent_S
    @constraint(
        m, eq_s_state[i = set_hour_0, j = set_quarter], 
        x_sorbent_S[i, j + 1]
        ==
        x_sorbent_S[i, j] - x_sorbent_R[i, j] + x_sorbent_A1[i, j]
    )

    # --------------------------------------------------------------------------

    # 2. CONTINUITY OF STATES
    # connect the ending slice with the beginning slice of the next hour

    # x_sorbent_A1
    @constraint(
        m, eq_A1_cont[i = set_hour], 
        x_sorbent_A1[i, 0]
        ==
        x_sorbent_A1[i - 1, n_slice]
    )
    # x_sorbent_F
    @constraint(
        m, eq_F_cont[i = set_hour], 
        x_sorbent_F[i, 0]
        ==
        x_sorbent_F[i - 1, n_slice]
    )
    # x_sorbent_S
    @constraint(
        m, eq_S_cont[i = set_hour], 
        x_sorbent_S[i, 0]
        ==
        x_sorbent_S[i - 1, n_slice]
    )
    # --------------------------------------------------------------------------

    # 3. INITIAL CONDITIONS
    @constraint(m, eq_A1_init, x_sorbent_A1[0, 0] == 0.)
    @constraint(m, eq_f_init, x_sorbent_F[0, 0] == x_sorbent_total)
    @constraint(m, eq_s_init, x_sorbent_S[0, 0] == 0.)

    # --------------------------------------------------------------------------

    # 4. END CONDITIONS
    @constraint(m, eq_A1_end, x_sorbent_A1[n_hour, n_slice] == 0.)
    @constraint(m, eq_f_end, x_sorbent_F[n_hour, n_slice] == x_sorbent_total)
    @constraint(m, eq_s_end, x_sorbent_S[n_hour, n_slice] == 0.)

    # --------------------------------------------------------------------------

    # 5. CO2 capture
    @constraint(
        m, eq_CO2_DAC[i = set_hour_0, j=set_quarter], 
        x_CO2_DAC[i, j]
        == 
        sorbent_cap_DAC_air * x_sorbent_R[i, j]
    )

    # --------------------------------------------------------------------------

    # 6. STEAM USAGE
    @constraint(
        m, eq_steam_DAC[i = set_hour_0, j=set_quarter], 
        x_steam_DAC[i, j]
        ==
        a_steam_DAC * sorbent_cap_DAC_air * x_sorbent_R[i, j]
    )

    # --------------------------------------------------------------------------

    # 7. POWER USAGE
    @constraint(
        m, eq_power_DAC[i = set_hour_0, j=set_quarter], 
        x_power_DAC[i, j]
        ==
        a_power_DAC * sorbent_cap_DAC_air * (x_sorbent_A0[i, j] + x_sorbent_A1[i, j]) / 2
    )

    # --------------------------------------------------------------------------

    # 8. MASS BALANCE INEQUALITIES 
    @constraint(
        m, eq_A0_limit[i = set_hour_0, j=set_quarter], 
        x_sorbent_A0[i, j]
        <=
        x_sorbent_F[i, j]
    )
    @constraint(
        m, eq_R_limit[i = set_hour_0, j=set_quarter], 
        x_sorbent_R[i, j]
        <=
        x_sorbent_S[i, j]
    )
    
end