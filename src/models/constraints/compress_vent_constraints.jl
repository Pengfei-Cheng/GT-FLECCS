"""
Modeling module
Declare compressor and vented CO2-related constraints.

Pengfei Cheng

1. CO2 compression amount
2. power usage of CO2 compression
3. total CO2 captured
"""

function add_compress_vent_constraints(m)

    x_CO2_compress = m[:x_CO2_compress]
    x_CO2_PCC = m[:x_CO2_PCC]
    x_CO2_DAC = m[:x_CO2_DAC]
    x_power_compress = m[:x_power_compress]
    x_CO2_cap_total = m[:x_CO2_cap_total]
    x_CO2_vent_PCC = m[:x_CO2_vent_PCC]

    # 1. CO2 compression amount
    # integral over all slices within each hour
    @constraint(
        m, eq_compress_CO2[i = set_hour_0], 
        x_CO2_compress[i]
        ==
        x_CO2_PCC[i] 
        + sum(x_CO2_DAC[i, j] for j in set_quarter)
    )

    # ------------------------------------------------------------------------------

    # 2. power usage of CO2 compression
    @constraint(
        m, eq_compress_CO2_power[i = set_hour_0], 
        x_power_compress[i]
        ==
        a_power_compr_PCC * x_CO2_PCC[i]
        + a_power_compr_DAC * sum(x_CO2_DAC[i, j] for j in set_quarter)
    )

    # ------------------------------------------------------------------------------

    # 3. total CO2 captured
    @constraint(
        m, eq_CO2_cap_total[i = set_hour_0], 
        x_CO2_cap_total[i]
        ==
        - x_CO2_vent_PCC[i] 
        + (1 - a_CO2_vent_DAC) * sum(x_CO2_DAC[i, j] for j in set_quarter)
    )
end