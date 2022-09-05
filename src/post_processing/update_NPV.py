"""Post-Processing Module: Updating retrofit NPV with B31A operating profit

NOTE: Update B31A_PATH, RETROFIT_PATH, and LOG_PATH to your directories.
"""

import pandas as pd
from os.path import exists

B31A_PATH = ''
RETROFIT_PATH = ''
LOG_PATH = ''

# tax rate
TAX_R = 0.2574
# interest rate
INT_R = 0.0297
# TOC and FOM of PCC
TOC_PCC = 887213895
FOM_PCC = 22193424


def update_NPV(folder_name, PCC_base=False, PCC_extra=False, log=True, prefix=''):
    """Main function to update the NPV and the cash flow table of a given
    solution.

    Args:
        folder name (string): Name of the result folder.
        PCC_base (bool): If the capital cost of PCC is reduced by 25% (DOE feed
        study).
        PCC_extra (bool): If the capital cost of PCC is reduced by 15% (other
        owner's cost).
        log (bool): Whether logging the result or not.
        prefix (string): Prefix for folder name.
    """

    # avoid only PCC_extra and not PCC_base
    if PCC_extra and not PCC_base:
        raise ValueError("Cannot only reduce PCC cost by 15%!")

    B31A_profit = read_B31A_profit(folder_name)
    df_NPV, df_cost = read_retrofit_solutions(folder_name)

    update_selling(df_NPV, df_cost, B31A_profit)

    if PCC_base:
        update_PCC_cost(df_NPV, PCC_extra=PCC_extra)

    update_cash_flow_table(df_NPV)

    save_cash_flow(df_NPV, folder_name, PCC_base=PCC_base,
                     PCC_extra=PCC_extra, prefix=prefix)

    if log:
        log_NPV(df_NPV, folder_name,
                        PCC_base=PCC_base, PCC_extra=PCC_extra, prefix=prefix)


def read_B31A_profit(folder_name):
    """Read the annual profit of B31A."""

    B31A_path = B31A_PATH + folder_name + '/'
    df = pd.read_csv(B31A_path + 'obj_value.csv')
    profit = df.loc[0, "profit"]
    return profit


def read_retrofit_solutions(folder_name):
    """Read the cost and cash flow table of retrofit."""
    folder_path = RETROFIT_PATH + folder_name

    cost_name = 'results_operation_cost.csv'
    NPV_name = 'NPV.csv'

    df_cost = pd.read_csv(folder_path + '/' + cost_name)
    df_cash_flow = pd.read_csv(folder_path + '/' + NPV_name)

    return df_cash_flow, df_cost


def update_cash_flow_table(df):
    """Update the columns of the cash flow table, starting from net earnings.
    """
    df["net_earnings"] = (
        df["S"] - df["COST_EXCLUDE_D"] - df["D"]) * (1 - TAX_R)

    # update cash flow
    df["cash_flow"] = df["net_earnings"] + df["C_TDC"] + df["D"]

    # update PV
    for i in range(22):
        df.loc[i, "PV"] = df.loc[i, "cash_flow"] / ((1 + INT_R) ** i)

    # update cumulative PV
    df.loc[0, "cum_PV"] = df.loc[0, "PV"]
    for i in range(1, 22):
        df.loc[i, "cum_PV"] = df.loc[i - 1, "cum_PV"] + df.loc[i, "PV"]


def update_selling(df_cash_flow, df_cost, B31A_profit):
    """Update the B31A profit into the selling column of the NPV table."""

    annual_CO2_credit = - sum(df_cost.loc[:, "CO2_credit"])
    annual_power_sell = sum(df_cost.loc[:, "power_profit"])

    # update selling column
    df_cash_flow.loc[2:21, "S"] = annual_CO2_credit + annual_power_sell - B31A_profit


def update_PCC_cost(df, PCC_extra=False):
    """Update the PCC capital cost in the NPV table (in the 'C_TDC' and
    'COST_EXCLUDE_D' columns).

    04-25-2022: add another 15% for other owner's cost.
    """

    if PCC_extra:
        rate = 0.25 + 0.1779 / (1 + 0.1779)
    else:
        rate = 0.25

    # update CAPEX
    d_PCC_TOC = TOC_PCC * rate
    df.loc[0, "C_TDC"] += 0.3 * d_PCC_TOC
    df.loc[1, "C_TDC"] += 0.7 * d_PCC_TOC

    # update FOM
    d_FOM_PCC = FOM_PCC * rate
    df.loc[2:21, 'COST_EXCLUDE_D'] -= d_FOM_PCC


def save_cash_flow(df_NPV, folder_name, PCC_base=False, PCC_extra=False, prefix=''):
    """Save updated cash flow table into a new csv file."""
    folder_path = RETROFIT_PATH + folder_name + '/'

    file_name = prefix + 'NPV_w_B31A'
    if PCC_base:
        if PCC_extra:
            df_NPV.to_csv(folder_path + file_name + '_PCC_40.csv')
        else:
            df_NPV.to_csv(folder_path + file_name + '_PCC_25.csv')
    else:
        df_NPV.to_csv(folder_path + file_name + '.csv')


def log_NPV(df_NPV, folder_name, PCC_base=False, PCC_extra=False, prefix=''):
    """Save updated triple (price signal, CO2 price, NPV) into log."""

    CO2_price, price_signal = folder_name.split(
        "month-")[1].split("-")[0], ("-").join(folder_name.split("month-")[1].split("-")[1:])

    NPV = df_NPV.loc[21, "cum_PV"]
    sol_row = pd.Series({
        'scenario': price_signal,
        'CO2_price': CO2_price,
        'NPV': NPV
    }).to_frame().T

    log_file = 'NPVs_w_B31A'
    if PCC_base:
        if PCC_extra:
            log_file += '_PCC_40'
        else:
            log_file += '_PCC_25'
    log_file += '.csv'

    if prefix != '':
        log_file = prefix + '_' + log_file

    if exists(LOG_PATH + log_file):
        sol_row.to_csv(LOG_PATH + log_file, index=False,
                       header=False, mode='a')
    else:
        sol_row.to_csv(LOG_PATH + log_file, index=False, header=True, mode='a')
