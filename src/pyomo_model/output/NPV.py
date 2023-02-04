"""
Output module
Pengfei Cheng

Create the DataFrame for NPV terms.
"""

import numpy as np
import pandas as pd
from pyomo.environ import value
from src.pyomo_model.params import *

def gen_NPV_df(m, df_cost, df_binary, n_month, cost_start_up):

    dfs_NPV = {}
    dfs_cost_profit = {}

    for s in set_scenario:
        # NPV
        # year
        year = list(range(2021, 2042 + 1))
        # year = 2021:2042

        # total TOC w/o DAC
        TOC_wo_DAC = 1142222643
        # DAC TOC
        TOC_DAC = (a_cost_sorbent * value(m.x_sorbent_total) * 3000 + a_cost_adsorb * value(m.x_air_adsorb_max) * 48000) * (1 + 0.0311 + 0.0066 + 0.1779)
        TOC_total = TOC_wo_DAC + TOC_DAC
        # capital expenditure
        C_TDC = np.zeros(22)
        C_TDC[0] = -0.3 * TOC_total
        C_TDC[1] = -0.7 * TOC_total

        # WC
        C_WC = np.zeros(22)

        # depreciation
        D = np.zeros(22)
        # 150% reducing balance
        d = 0.075
        for i in range(2, 21 + 1):
            D[i] = TOC_total * d * ((1 - d) ** (i - 3))

        # time length factor
        w = 12 / n_month

        # annual fuel cost
        fuel_cost_annual = sum(df_cost[s].loc[:, "cost_fuel"]) * w
        # annual CO2 transportation cost
        cost_CO2_TS = sum(df_cost[s].loc[:, "cost_CO2_TS"]) * w
        # annual FOM
        FOM_wo_DAC = 47965372
        FOM_total = FOM_wo_DAC + ((a_cost_sorbent * value(m.x_sorbent_total) * 3000 + a_cost_adsorb * value(m.x_air_adsorb_max) * 48000) * 0.05 + 2 * 110000)
        # annual VOM
        VOM_total = df_cost[s][["cost_NGCC_VOM", "cost_PCC_VOM", "cost_DAC_VOM", "cost_PCC_compr_VOM", "cost_DAC_compr_VOM"]].sum().sum() * w
        # annual start-up cost
        start_up_cost_total = cost_start_up[s] * max(sum(df_binary[s].loc[:, "z0"]) * w, 5)
        # cost excluding depreciation
        COST_EXCLUDE_D = np.zeros(22)
        for i in range(2, 21 + 1):
            COST_EXCLUDE_D[i] = fuel_cost_annual + cost_CO2_TS + FOM_total + VOM_total + start_up_cost_total

        annual_CO2_credit = sum(df_cost[s].loc[:, "credit_CO2"]) * w
        annual_power_sell = sum(df_cost[s].loc[:, "profit_power"]) * w
        # sell
        S = np.zeros(22)
        S_single = annual_CO2_credit + annual_power_sell
        for i in range(2, 21 + 1):
            S[i] = S_single

        # net earnings
        net_earnings = np.zeros(22)
        for i in range(2, 21 + 1):
            net_earnings[i] = (S[i] - COST_EXCLUDE_D[i] - D[i]) * (1 - tax_r)

        # cash flow
        cash_flow = np.zeros(22)
        for i in range(21 + 1):
            cash_flow[i] = C_TDC[i] + D[i] + net_earnings[i]

        # PV
        PV = np.zeros(22)
        for i in range(21 + 1):
            PV[i] = cash_flow[i] / (1 + int_r) ** (i - 1)

        # cumulative PV
        cum_PV = np.zeros(22)
        cum_PV[0] = PV[0]
        for i in range(1, 21 + 1):
            cum_PV[i] = cum_PV[i - 1] + PV[i]

        # output DataFrame
        vars = ["year", "C_TDC", "C_WC", "D", "COST_EXCLUDE_D", "S", "net_earnings", "cash_flow", "PV", "cum_PV" ]
        df_NPV = pd.DataFrame(columns=vars)

        df_NPV = pd.DataFrame([year, C_TDC, C_WC, D, COST_EXCLUDE_D, S, net_earnings, cash_flow, PV, cum_PV]).T
        df_NPV.columns = vars

        dfs_NPV[s] = df_NPV


        # profit/cost profile

        vars = [
            "FOM", "VOM", "fuel_cost", "CO2_TS", "start_up_cost", "CO2_credit", "electricity_value"
        ]
        df_overall_profit_cost = pd.DataFrame([[FOM_total, VOM_total, fuel_cost_annual, cost_CO2_TS, start_up_cost_total, annual_CO2_credit, annual_power_sell]])
        df_overall_profit_cost.columns = vars

        dfs_cost_profit[s] = df_overall_profit_cost

    return dfs_NPV, dfs_cost_profit