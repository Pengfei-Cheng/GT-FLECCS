"""
Modeling module
Declare power-related constraints.

Pengfei Cheng

1. power from LP steam turbine
2. total power from all steam turbines
3. total power generation
4. GT power 
5. net power output
"""

function add_power_constraints(m)

    x_steam_for_LP = m[:x_steam_for_LP]
    x_power_ST = m[:x_power_ST]
    x_power_HP = m[:x_power_HP]
    x_power_IP = m[:x_power_IP]
    x_power_LP = m[:x_power_LP]
    x_power_total = m[:x_power_total]
    x_power_GT = m[:x_power_GT]
    x_power_out = m[:x_power_out]
    x_power_PCC = m[:x_power_PCC]
    x_power_aux = m[:x_power_aux]
    x_DAC_FG_power = m[:x_DAC_FG_power]
    x_power_DAC = m[:x_power_DAC]
    x_compress_power = m[:x_compress_power]
    x_load_factor = m[:x_load_factor]
    y = m[:y]

    # 1. POWER FROM LP STEAM TURBINE
    @constraint(
        m, eq_power_LP[i = set_hour_0], 
        x_power_LP[i]
        ==
        x_steam_for_LP[i] * a_power_LP_steam
    )

    # --------------------------------------------------------------------------

    # 2. TOTAL POWER FROM ALL STEAM TURBINES
    @constraint(m, eq_total_power_ST[i = set_hour_0], 
        x_power_ST[i]
        ==
        x_power_HP[i] + x_power_IP[i] + x_power_LP[i]
    )

    # --------------------------------------------------------------------------

    # 3. TOTAL POWER GENERATION
    @constraint(
        m, eq_power_total[i = set_hour_0], 
        x_power_total[i]
        ==
        x_power_GT[i] + x_power_ST[i]
    )

    # --------------------------------------------------------------------------

    # 4. GT POWER 
    @constraint(
        m, eq_total_power_GT[i = set_hour_0],
        x_power_GT[i]
        ==
        (a_power_GT * x_load_factor[i] + b_power_GT * y[i])
    )
    # --------------------------------------------------------------------------

    # 5. NET POWER OUTPUT
    @constraint(
        m, eq_power_out[i = set_hour_0], 
        x_power_out[i]
        ==
        x_power_total[i] 
        - x_power_PCC[i]
        - sum(x_DAC_FG_power[i, j] for j in set_quarter)
        - sum(x_power_DAC[i, j] for j in set_quarter)
        - x_compress_power[i] 
        - x_power_aux[i]
    )
end