import numpy as np
from scipy.optimize import fsolve
import pandas as pd

# unit_CO2_credit = 100
unit_CO2_transportation_cost = 10

load_factor = 1
DAC_size = 2990
net_power = 475.432
unit_fuel_cost = 3.83
fuel_usage = 4616
CO2_capture = 132.63


def calc_B31A_hourly_profit(elec_price, unit_CO2_credit):
    power_sell = 727 * elec_price
    total_fuel_cost = unit_fuel_cost * 6.363 * 727
    CO2_penalty = unit_CO2_credit * 0.336 * 740

    VOM = 1.70517 * 727

    total_cost = total_fuel_cost + CO2_penalty + VOM
    total_profit = power_sell

    net_earning = max(total_profit - total_cost, 0)

    return net_earning

def calc_B31A_annual_profit(elec_price, unit_CO2_credit):

    B31A_hourly_profit = calc_B31A_hourly_profit(elec_price, unit_CO2_credit)

    FOM = 19465868

    return B31A_hourly_profit * 7446 - FOM


def calc_hourly_profit(elec_price, unit_CO2_credit):

    power_sell = net_power * elec_price
    total_fuel_cost = unit_fuel_cost * fuel_usage
    CO2_credit = CO2_capture * unit_CO2_credit
    CO2_transportation_cost = CO2_capture * unit_CO2_transportation_cost

    VOM = 8751464 / 7446 + (18527935 + 1745198 + 861984) / 8760 + 9 * CO2_capture

    total_cost = total_fuel_cost + CO2_transportation_cost + VOM
    total_profit = power_sell + CO2_credit

    return total_cost, total_profit


def calc_annual_profit(elec_price, unit_CO2_credit):

    cost, profit = calc_hourly_profit(elec_price, unit_CO2_credit)

    FOM = 62149816

    annual_profit = profit * 7446
    annual_cost = cost * 7446 + FOM

    return annual_cost, annual_profit


def calc_NPV(elec_price, unit_CO2_credit, count_B31A=False):

    IRR = 0.12

    cost, profit = calc_annual_profit(elec_price, unit_CO2_credit)

    df = pd.DataFrame(columns=['year', 'C_TDC', 'C_WC', 'D', 'COST_EXCLUDE_D', 'S', 'net_earnings', 'cash_flow', 'PV', 'NPV'])
    years = range(2021, 2043)

    TOC = 1481726206
    C_TDC = np.zeros(22)
    C_TDC[0] = - TOC * 0.3
    C_TDC[1] = - TOC * 0.7 / (1 + IRR)

    C_WC = np.zeros(22)

    D = np.zeros(22)
    # 150% reducing balance
    d = 0.075
    for i in range(2, 22):
        D[i] = TOC * d * ((1 - d) ** (i - 3))

    COST = np.zeros(22)
    for i in range(2, 22):
        COST[i] = cost


    S = np.zeros(22)
    if count_B31A:
        profit_B31A = calc_B31A_annual_profit(elec_price, unit_CO2_credit)
        for i in range(2, 22):
            S[i] = profit - profit_B31A
    else:
        for i in range(2, 22):
            S[i] = profit

    tax_r = 0.2574

    net_earnings = np.zeros(22)
    for i in range(2, 22):
        net_earnings[i] = (S[i] - COST[i] - D[i]) * (1 - tax_r)

    cash_flow = np.zeros(22)
    for i in range(22):
        cash_flow[i] = net_earnings[i] + C_TDC[i] + D[i]

    PV = np.zeros(22)
    for i in range(22):
        PV[i] = cash_flow[i] / (1 + IRR) ** (i - 1)

    cum_PV = np.zeros(22)
    cum_PV[0] = PV[0]
    for i in range(1, 22):
        cum_PV[i] = cum_PV[i - 1] + PV[i]

    for i in range(22):
        temp_df = pd.DataFrame([[years[i], C_TDC[i], C_WC[i], D[i], COST[i], S[i], net_earnings[i], cash_flow[i], PV[i], cum_PV[i]]], columns=['year', 'C_TDC', 'C_WC', 'D', 'COST_EXCLUDE_D', 'S', 'net_earnings', 'cash_flow', 'PV', 'NPV'])
        df = pd.concat([df, temp_df])

    NPV = df.iloc[-1, -1]

    return df, NPV

if __name__ == "__main__":

    def calc_NPV_wrapper(elec_price):

        df, NPV = calc_NPV(elec_price, unit_CO2_credit, count_B31A=True)

        return NPV

    IRR = 0.12
    unit_CO2_credits = [100, 150, 225, 300, 350, 400, 450, 500]

    df = pd.DataFrame(columns=['IRR', 'unit_CO2_credit', 'electricity price'])

    for unit_CO2_credit in unit_CO2_credits:

        root = fsolve(calc_NPV_wrapper, 200)
        print(calc_NPV_wrapper(root))
        # print(IRR, unit_CO2_credit, root[0])
        tmp_df = pd.DataFrame([[IRR, unit_CO2_credit, root[0]]], columns=['IRR', 'unit_CO2_credit', 'electricity price'])
        df = pd.concat([df, tmp_df])

    # root = fsolve(calc_NPV_wrapper, 40)

    pass
