"""
Modeling module
Constraints related to DAC costing.

Pengfei Cheng
2022

UPDATE:
    04-07-2022: eq_adsorb_air_volume_DAC_air: RHS - 
        (x_A0[i, j] + x_A1[i, j]) is updated to x_A0[i, j]
        x_A1 air for those batches is already in the contactor, no need to
        blow air again
    07-25-2022: eq_adsorb_air_volume_DAC_air: RHS - 
        x_A1 term is added back as the air is blown continuously through the 
        contactor for 30 min. 
        A factor (0.5) is added as the capacity is for 30-min adsorption.
"""

function add_DAC_costing_constraints(m)
    cost_sorbent = m[:cost_sorbent]
    x_sorbent_m = m[:x_sorbent_m]
    x_sorbent_m_DAC_FG = m[:x_sorbent_m_DAC_FG]
    x_adsorb_air_volume_DAC_air = m[:x_adsorb_air_volume_DAC_air]
    x_A0 = m[:x_A0]
    x_A1 = m[:x_A1]
    x_adsorb_air_volume_DAC_FG = m[:x_adsorb_air_volume_DAC_FG]
    x_A0_FG = m[:x_A0_FG]
    x_adsorb_max_air_rate_air = m[:x_adsorb_max_air_rate_air]
    x_adsorb_max_air_rate_FG = m[:x_adsorb_max_air_rate_FG]
    cost_adsorb_system = m[:cost_adsorb_system]
    TPC_DAC = m[:TPC_DAC]

    # calculate the cost of sorbent
    @constraint(
        m, eq_cost_sorbent,
        cost_sorbent
        ==
        a_contactor * (x_sorbent_m_DAC_FG + x_sorbent_m)
    )

    # volume of blown air for DAC-air and DAC-FG adsorption
    @constraint(
        m, eq_adsorb_air_volume_DAC_air[i = set_hour_0, j = set_quarter],
        x_adsorb_air_volume_DAC_air[i, j]
        >=
        (x_A0[i, j] + x_A1[i, j]) * sorbent_cap_DAC_air / 2     # tonne CO2
        * tonne_to_g / CO2_mole_w                               # mole CO2
        * mole_vol                                              # m^3 CO2
        / CO2_vol_ratio                                         # m^3 air
    )
    @constraint(
        m, eq_adsorb_air_volume_DAC_FG[i = set_hour_0, j = set_quarter],
        x_adsorb_air_volume_DAC_FG[i, j]
        >=
        x_A0_FG[i, j] * sorbent_cap_DAC_FG                      # tonne CO2
        * tonne_to_g / CO2_mole_w                               # mole CO2
        * mole_vol                                              # m^3 CO2
        / CO2_vol_ratio_FG                                      # m^3 air
    )

    # adsorption air rate
    @constraint(
        m, eq_adsorb_max_air_rate_air[i = set_hour_0, j = set_quarter],
        x_adsorb_max_air_rate_air
        >=
        x_adsorb_air_volume_DAC_air[i, j] / 15 / 60  # 1 slice = 15 min = 900 s
    )
    @constraint(
        m, eq_adsorb_max_air_rate_FG[i = set_hour_0, j = set_quarter],
        x_adsorb_max_air_rate_FG
        >=
        x_adsorb_air_volume_DAC_FG[i, j] / 15 / 60  # 1 slice = 15 min = 900 s
    )

    # calculate the cost of adsorption systems
    @constraint(
        m, eq_cost_adsorption_sys,
        cost_adsorb_system
        ==
        a_adsorb_sys * (x_adsorb_max_air_rate_FG + x_adsorb_max_air_rate_air)
    )

    # calculate the total capital cost of DAC systems
    @constraint(
        m, eq_capital_cost_DAC,
        TPC_DAC
        ==
        cost_sorbent + cost_adsorb_system
    )
end