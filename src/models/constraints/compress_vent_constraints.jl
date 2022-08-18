"""
Modeling module
Declare compressor and vented CO2-related constraints.

Pengfei Cheng

1. CO2 compression rate
2. power usage of CO2 compression
3. total vented CO2

UPDATE:
    04-12-2022:
        updated compression power usage.
        updated vented term from DAC CO2 compression.
"""

function add_compress_vent_constraints(m)

    x_compress_CO2 = m[:x_compress_CO2]
    x_CO2_PCC_cap = m[:x_CO2_PCC_cap]
    x_DAC_FG_CO2_cap = m[:x_DAC_FG_CO2_cap]
    x_CO2_DAC_cap = m[:x_CO2_DAC_cap]
    x_compress_power = m[:x_compress_power]
    x_vent_CO2 = m[:x_vent_CO2]
    x_CO2_PCC_vent = m[:x_CO2_PCC_vent]
    x_DAC_FG_CO2_vent = m[:x_DAC_FG_CO2_vent]

    # 1. CO2 compression rate
    # integral over all slices within each hour
    @constraint(
        m, eq_compress_CO2[i = set_hour_0], 
        x_compress_CO2[i]
        ==
        x_CO2_PCC_cap[i] 
        + sum(x_DAC_FG_CO2_cap[i, j] for j in set_quarter)
        + sum(x_CO2_DAC_cap[i, j] for j in set_quarter)
    )

    # ------------------------------------------------------------------------------

    # 2. power usage of CO2 compression
    @constraint(
        m, eq_compress_CO2_power[i = set_hour_0], 
        x_compress_power[i]
        ==
        a_compress_power_PCC * x_CO2_PCC_cap[i]
        + a_compress_power_DAC * (
            sum(x_DAC_FG_CO2_cap[i, j] for j in set_quarter)
            + sum(x_CO2_DAC_cap[i, j] for j in set_quarter)
        )
    )

    # ------------------------------------------------------------------------------

    # 3. total vented CO2
    @constraint(
        m, eq_vent_CO2[i = set_hour_0], 
        x_vent_CO2[i]
        ==
        x_CO2_PCC_vent[i] 
        + x_DAC_FG_CO2_vent[i] 
        - (1 - a_compress_vent_DAC) * sum(x_CO2_DAC_cap[i, j] for j in set_quarter)
    )
end