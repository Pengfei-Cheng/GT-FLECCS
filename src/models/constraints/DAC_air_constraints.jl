"""
Modeling module
Declare DAC-air-related constraints.

Pengfei Cheng

DAC-related variables must start at 0 and end at 1-n_slice.

UPDATE:
    06-03-2022: 
        Removed A2- and R1-related constraints;
        Added mass balance inequalities.

Assumptions:
    1. we can take CO2 from air in pure form.
    2 DAC-air takes two time slots (30 min) for adsorption

1. state equation
2. continuity of states
3. initial conditions
4. end conditions
5. CO2 capture
6. steam usage
7. power usage
8. mass balance inequalities 
"""

function add_DAC_air_constraints(m)
    x_A1 = m[:x_A1]
    x_A0 = m[:x_A0]
    x_R = m[:x_R]
    x_F = m[:x_F]
    x_S = m[:x_S]
    x_sorbent_m = m[:x_sorbent_m]
    x_CO2_DAC_cap = m[:x_CO2_DAC_cap]
    x_steam_DAC = m[:x_steam_DAC]
    x_power_DAC = m[:x_power_DAC]

    # 1. STATE EQUATION
    # x_A1
    @constraint(
        m, eq_DAC_air_x_A1_state[i = set_hour_0, j = set_quarter], 
        x_A1[i, j + 1]
        ==
        x_A0[i, j]
    )
    # x_F
    @constraint(
        m, eq_DAC_air_x_f_state[i = set_hour_0, j = set_quarter], 
        x_F[i, j + 1]
        ==
        x_F[i, j] - x_A0[i, j] + x_R[i, j]
    )
    # x_S
    @constraint(
        m, eq_DAC_air_x_s_state[i = set_hour_0, j = set_quarter], 
        x_S[i, j + 1]
        ==
        x_S[i, j] - x_R[i, j] + x_A1[i, j]
    )

    # --------------------------------------------------------------------------

    # 2. CONTINUITY OF STATES
    # connect the ending slice with the beginning slice of the next hour

    # x_A1
    @constraint(
        m, eq_cont_x_A1[i = set_hour], 
        x_A1[i, 0]
        ==
        x_A1[i - 1, n_slice]
    )
    # x_F
    @constraint(
        m, eq_cont_x_F[i = set_hour], 
        x_F[i, 0]
        ==
        x_F[i - 1, n_slice]
    )
    # x_S
    @constraint(
        m, eq_cont_x_S[i = set_hour], 
        x_S[i, 0]
        ==
        x_S[i - 1, n_slice]
    )
    # --------------------------------------------------------------------------

    # 3. INITIAL CONDITIONS
    @constraint(m, eq_DAC_air_x_A1_init, x_A1[0, 0] == 0.)
    @constraint(m, eq_DAC_air_x_f_init, x_F[0, 0] == x_sorbent_m)
    @constraint(m, eq_DAC_air_x_s_init, x_S[0, 0] == 0.)

    # --------------------------------------------------------------------------

    # 4. END CONDITIONS
    @constraint(m, eq_DAC_air_x_A1_end, x_A1[n_hour, n_slice] == 0.)
    @constraint(m, eq_DAC_air_x_f_end, x_F[n_hour, n_slice] == x_sorbent_m)
    @constraint(m, eq_DAC_air_x_s_end, x_S[n_hour, n_slice] == 0.)

    # --------------------------------------------------------------------------

    # 5. CO2 capture
    @constraint(
        m, eqw_DAC_air_CO2_cap[i = set_hour_0, j=set_quarter], 
        x_CO2_DAC_cap[i, j]
        == 
        sorbent_cap_DAC_air * x_R[i, j]
    )

    # --------------------------------------------------------------------------

    # 6. STEAM USAGE
    @constraint(
        m, eq_DAC_air_steam[i = set_hour_0, j=set_quarter], 
        x_steam_DAC[i, j]
        ==
        a_DAC_air_steam * sorbent_cap_DAC_air * x_R[i, j]
    )

    # --------------------------------------------------------------------------

    # 7. POWER USAGE
    @constraint(
        m, eq_DAC_air_power[i = set_hour_0, j=set_quarter], 
        x_power_DAC[i, j]
        ==
        a_DAC_air_power * sorbent_cap_DAC_air * (x_A0[i, j] + x_A1[i, j]) / 2
    )

    # --------------------------------------------------------------------------

    # 8. MASS BALANCE INEQUALITIES 
    @constraint(
        m, eq_A0_limit[i = set_hour_0, j=set_quarter], 
        x_A0[i, j]
        <=
        x_F[i, j]
    )
    @constraint(
        m, eq_R_limit[i = set_hour_0, j=set_quarter], 
        x_R[i, j]
        <=
        x_S[i, j]
    )
    
end