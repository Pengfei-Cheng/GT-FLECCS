"""
Modeling module
Declare power-related constraints.

Pengfei Cheng

1. total power generation
2. GT power 
3. net power output
"""

function add_power_constraints(m)

    x_power_ST = m[:x_power_ST]
    x_power_total = m[:x_power_total]
    x_power_GT = m[:x_power_GT]
    x_power_net = m[:x_power_net]
    x_power_aux = m[:x_power_aux]
    x_load = m[:x_load]
    y = m[:y]

    # --------------------------------------------------------------------------

    # 1. TOTAL POWER GENERATION
    @constraint(
        m, eq_power_total[i = set_hour_0], 
        x_power_total[i]
        ==
        x_power_GT[i] + x_power_ST[i]
    )

    # --------------------------------------------------------------------------

    # 2. GT POWER 
    @constraint(
        m, eq_total_power_GT[i = set_hour_0],
        x_power_GT[i]
        ==
        a_power_GT * x_load[i]
    )
    # --------------------------------------------------------------------------

    # 3. NET POWER OUTPUT
    @constraint(
        m, eq_power_out[i = set_hour_0], 
        x_power_net[i]
        ==
        x_power_total[i] 
        - x_power_aux[i]
    )

end