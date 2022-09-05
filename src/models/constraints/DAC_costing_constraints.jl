"""
Modeling module
Constraints related to DAC costing.

Pengfei Cheng
2022
"""

function add_DAC_costing_constraints(m)
    x_cost_sorbent = m[:x_cost_sorbent]
    x_sorbent_total = m[:x_sorbent_total]
    x_air_adsorb = m[:x_air_adsorb]
    x_sorbent_A0 = m[:x_sorbent_A0]
    x_sorbent_A1 = m[:x_sorbent_A1]
    x_air_adsorb_max = m[:x_air_adsorb_max]
    x_cost_adsorb = m[:x_cost_adsorb]
    x_cost_DAC_TPC = m[:x_cost_DAC_TPC]

    # calculate the cost of sorbent
    @constraint(
        m, eq_cost_sorbent,
        x_cost_sorbent
        ==
        a_cost_sorbent * x_sorbent_total
    )

    # volume of blown air
    @constraint(
        m, eq_adsorb_air_volume[i = set_hour_0, j = set_quarter],
        x_air_adsorb[i, j]
        >=
        (x_sorbent_A0[i, j] + x_sorbent_A1[i, j])       # tonne sorbent
        * sorbent_cap_DAC_air / 2                       # tonne CO2
        * tonne_to_g / CO2_mole_w                       # mole CO2
        * mole_vol                                      # m^3 CO2
        / CO2_vol_ratio                                 # m^3 air
    )

    # max adsorption air rate
    @constraint(
        m, eq_adsorb_max_air_rate[i = set_hour_0, j = set_quarter],
        x_air_adsorb_max
        >=
        x_air_adsorb[i, j] / 15 / 60  # 1 slice = 15 min = 900 s
    )

    # calculate the cost of adsorption systems
    @constraint(
        m, eq_cost_adsorption_sys,
        x_cost_adsorb
        ==
        a_cost_adsorb * x_air_adsorb_max
    )

    # calculate the total capital cost of DAC systems
    @constraint(
        m, eq_capital_cost_DAC,
        x_cost_DAC_TPC
        ==
        x_cost_sorbent + x_cost_adsorb
    )
end