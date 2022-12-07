"""
Modeling module
Declare steam split constraints.

Pengfei Cheng

1. steam allocation 
2. total DAC steam
3. DAC steam slack 
4. steam rate limit

UPDATE:
    01-21-2022: added steam rate limit constraint.
"""

function add_steam_split_constraints(m)

    x_steam_allocable = m[:x_steam_allocable]
    x_steam_DAC_extra = m[:x_steam_DAC_extra]
    x_steam_LP = m[:x_steam_LP]
    x_steam_DAC_total = m[:x_steam_DAC_total]
    x_steam_DAC_base = m[:x_steam_DAC_base]
    x_steam_DAC_extra = m[:x_steam_DAC_extra]
    x_steam_DAC = m[:x_steam_DAC]

    # 1. STEAM ALLOCATION 
    @constraint(
        m, eq_steam_allocation[i = set_hour_0],
        x_steam_allocable[i]
        ==
        x_steam_DAC_extra[i] + x_steam_LP[i]
    )

    # --------------------------------------------------------------------------

    # 2. TOTAL DAC STEAM
    @constraint(
        m, eq_DAC_total_duty[i = set_hour_0],
        x_steam_DAC_total[i]
        ==
        x_steam_DAC_base[i] + x_steam_DAC_extra[i]
    )

    # --------------------------------------------------------------------------

    # 3. DAC STEAM SLACK 
    # integral over all slices within each hour
    @constraint(
        m, eq_DAC_steam_slack_int[i = set_hour_0], 
        x_steam_DAC_total[i] 
        >=
        sum(x_steam_DAC[i, j] for j in set_quarter)
    )

    # --------------------------------------------------------------------------

    # 4. STEAM RATE LIMIT
    # 15-min steam into DACs cannot exceed 1/4 of 1-hour available steam
    @constraint(
        m, eq_DAC_steam_rate_limit[i = set_hour_0, j = set_quarter],
        x_steam_DAC_total[i] / 4
        >=
        x_steam_DAC[i, j]
    )
end