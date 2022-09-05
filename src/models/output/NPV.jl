"""
Output module
Pengfei Cheng

Create the DataFrame for NPV terms.
"""

function gen_NPV_df(m, df_cost, df_binary)

    x_cost_DAC_TPC = value(m[:x_cost_DAC_TPC])
    x_cost_DAC_FOM = value(m[:x_cost_DAC_FOM])

    # year
    year = 2021:2042

    # total TOC w/o DAC
    TOC_wo_DAC = 1142222643
    # DAC TOC
    TOC_DAC = x_cost_DAC_TPC * (1 + 0.0311 + 0.0066 + 0.1779)
    TOC_total = TOC_wo_DAC + TOC_DAC
    # capital expenditure
    C_TDC = zeros(22, 1)
    C_TDC[1] = -0.3 * TOC_total
    C_TDC[2] = -0.7 * TOC_total

    # WC
    C_WC = zeros(22, 1)

    # depreciation
    D = zeros(22, 1)
    # 150% reducing balance
    d = 0.075
    for i in 3:22
        D[i] = TOC_total * d * ((1 - d) ^ (i - 3))
    end

    # annual fuel cost
    fuel_cost_annual = sum(df_cost[!, "fuel_cost"])
    # annual CO2 transportation cost
    CO2_transportation_cost = sum(df_cost[!, "CO2_transportation_cost"])
    # annual FOM
    FOM_wo_DAC = 47965372
    FOM_total = FOM_wo_DAC + x_cost_DAC_FOM
    # annual VOM
    VOM_total = (
        sum(df_cost[!, "x_cost_NGCC_VOM"]) + sum(df_cost[!, "x_cost_PCC_VOM"]) +
        sum(df_cost[!, "x_cost_DAC_VOM"]) + sum(df_cost[!, "x_cost_PCC_compr_VOM"]) +
        sum(df_cost[!, "x_cost_DAC_compr_VOM"])
    )
    # annual start-up cost
    start_up_cost_total = cost_start_up * sum(df_binary[!, "z0"])
    # cost excluding depreciation
    COST_EXCLUDE_D = zeros(22, 1)
    for i in 3:22
        COST_EXCLUDE_D[i] = fuel_cost_annual + CO2_transportation_cost + FOM_total +
                            VOM_total + start_up_cost_total
    end

    annual_CO2_credit = sum(df_cost[!, "CO2_credit"])
    annual_power_sell = sum(df_cost[!, "power_profit"])
    # sell
    S = zeros(22, 1)
    S_single = annual_CO2_credit + annual_power_sell
    for i in 3:22
        S[i] = S_single
    end


    # net earnings
    net_earnings = zeros(22, 1)
    for i in 3:22
        net_earnings[i] = (S[i] - COST_EXCLUDE_D[i] - D[i]) * (1 - tax_r)
    end

    # cash flow
    cash_flow = zeros(22, 1)
    for i in 1:22
        cash_flow[i] = C_TDC[i] + D[i] + net_earnings[i]
    end

    # PV
    PV = zeros(22, 1)
    for i in 1:22
        PV[i] = cash_flow[i] / (1 + int_r) ^ (i - 1)
    end

    # cumulative PV
    cum_PV = zeros(22, 1)
    cum_PV[1] = PV[1]
    for i in 2:22
        cum_PV[i] = cum_PV[i - 1] + PV[i]
    end

    # output DataFrame
    vars = ["year", "C_TDC", "C_WC", "D", "COST_EXCLUDE_D", "S", "net_earnings",
            "cash_flow", "PV", "cum_PV" ]
    df_NPV = DataFrame(map(generate_row_map, vars))

    for i in 1:22

        # local l0 = []

        # for v in vars
        #     s = Symbol(v)
        #     # l0 = vcat(l0, eval(s)[i])
        # end
        l0 = [year[i], C_TDC[i], C_WC[i], D[i], COST_EXCLUDE_D[i], S[i], net_earnings[i], cash_flow[i], PV[i], cum_PV[i]]

        push!(df_NPV, l0)
    end

    # -------------------

    # profit/cost profile

    vars = [
        "FOM", "VOM", "fuel_cost",
        "CO2_TS", "start_up_cost", "CO2_credit", 
        "electricity_value"
    ]

    df_overall_profit_cost = DataFrame(map(generate_row_map, vars))

    push!(df_overall_profit_cost, [FOM_total, VOM_total, fuel_cost_annual, CO2_transportation_cost, start_up_cost_total, annual_CO2_credit, annual_power_sell])

    return df_NPV, df_overall_profit_cost

end