"""
Plotting module with functions to generate plots for a given period.

Available functions:

    plot_sorbent_air_inventory: plot sorbent inventory in DAC-air.
        input: results_DAC_air.csv
        output: sorbent_alloc_DAC_air.png

    plot_sorbent_FG_inventory: plot sorbent inventory in DAC-FG.
        input: results_DAC_FG.csv
        output: sorbent_alloc_DAC_FG.png

    plot_gross_power: plot out power and gross power.
        input: results_power.csv
        output: power_out_and_gross.png

    plot_load_and_price: plot load factor and electricity price.
        input: results_power.csv results_power_price.csv
        output: load_and_price.png

    plot_gen_power: plot generated power.
        input: results_power.csv
        output: power_generation_stacked.png

    plot_ST_gen_power: plot steam turbine generated power.
        input: results_power.csv
        output: power_generation_ST_stacked.png

    plot_power_use: plot power consumption.
        input: results_power.csv
        output: power_use_stacked.png

    plot_CO2: plot CO2 capture.
        input: results_CO2.csv
        output: CO2_capture.png

    plot_DAC_CO2: plot DAC CO2 capture.
        input: results_CO2.csv
        output: CO2_capture_DAC.png

    plot_PCC_steam: plot PCC steam usage.
        input: results_steam.csv
        output: PCC_steam.png

    plot_DAC_steam: plot DAC steam usage.
        input: results_steam.csv
        output: DAC_steam.png

    plot_DAC_steam_source: plot DAC steam source.
        input: results_steam.csv
        output: DAC_steam_source.png

    plot_cost: plot operational cost.
        input: results_cost.csv
        output: cost.png

    plot_cost_stacked: plot stacked operational cost.
        input: results_cost.csv
        output: cost_stacked.png

    plot_negative_emission: plot (profit of) negative emission.
        input: results_cost.csv
        output: negative_emission.png

    plot_profit: plot profit profile.
        input: results_cost.csv
        output: profit.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import get_results_path

# number of slices within an hour
n_slice = 4


def plot_sorbent_air_inventory(start_h=5090, delta_h=80, model_name='m14', savefig=False):
    """
    Generate stacked-bar plot for DAC-air sorbent inventory from start_h to 
    start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time indices for DAC
    start_h_DAC_idx = start_h * n_slice
    end_h_DAC_idx = end_h * n_slice

    # --------------------------------------------------------------------------

    # read results
    f_name = 'results_DAC_air'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    f_air = df["x_F"]
    s_air = df["x_S"]
    A0_air = df["x_A0"]
    A1_air = df["x_A1"]
    R_air = df["x_R"]

    # modify amount of fresh and saturated sorbent
    fresh_sorbent = f_air + R_air - A0_air
    saturated_sorbent = s_air + A1_air - R_air

    # get time range
    t_DAC_idx_range = range(start_h_DAC_idx, end_h_DAC_idx)
    t_DAC_range = df.loc[t_DAC_idx_range, 'time']

    # bar width
    w = 1 / n_slice

    # --------------------------------------------------------------------------

    _, ax = plt.subplots()

    ax.bar(t_DAC_range,
           fresh_sorbent.iloc[t_DAC_idx_range],
           label="Unalloc. Fresh",
           color="lightblue",
           align="edge",
           width=w)
    ax.bar(t_DAC_range,
           A0_air.iloc[t_DAC_idx_range],
           bottom=fresh_sorbent.iloc[t_DAC_idx_range],
           label="Alloc. Absorption",
           color="moccasin",
           align="edge",
           width=w)
    ax.bar(t_DAC_range,
           A1_air.iloc[t_DAC_idx_range],
           bottom=fresh_sorbent.iloc[t_DAC_idx_range] +
           A0_air.iloc[t_DAC_idx_range],
           label="15-min Absorption",
           color="lavender",
           align="edge",
           width=w)
    ax.bar(t_DAC_range,
           saturated_sorbent.iloc[t_DAC_idx_range],
           bottom=fresh_sorbent.iloc[t_DAC_idx_range] +
           A0_air.iloc[t_DAC_idx_range] +
           A1_air.iloc[t_DAC_idx_range],
           label="Unalloc. Saturated",
           color="lightcoral",
           align="edge",
           width=w)
    ax.bar(t_DAC_range,
           R0_air.iloc[t_DAC_idx_range],
           bottom=fresh_sorbent.iloc[t_DAC_idx_range] +
           A0_air.iloc[t_DAC_idx_range] +
           A1_air.iloc[t_DAC_idx_range] +
           saturated_sorbent.iloc[t_DAC_idx_range],
           label="Alloc. Regen.",
           color="plum",
           align="edge",
           width=w)

    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))
    ax.set_xticks(x_ticks)

    ax.legend()

    ax.set_title("DAC-air Sorbent Allocation")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Mass of Sorbent (Tonne)")
    ax.set_xlim(start_h, end_h)

    if savefig:
        f_name = "sorbent_alloc_DAC_air"
        f_path = get_results_path(f_name, model_name=model_name, ext='png')
        plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_sorbent_FG_inventory(start_h=5090, delta_h=80, model_name='m14'):
    """
    Generate stacked-bar plot for DAC-FG sorbent inventory from start_h to 
    start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time indices for DAC
    start_h_DAC_idx = start_h * n_slice
    end_h_DAC_idx = end_h * n_slice

    # --------------------------------------------------------------------------

    # read results
    f_name = 'results_DAC_FG'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    f_FG = df["x_f_FG"]
    s_FG = df["x_s_FG"]
    A0_FG = df["x_A0_FG"]
    A1_FG = df["x_A1_FG"]
    R0_FG = df["x_R0_FG"]
    R1_FG = df["x_R1_FG"]

    # modify amount of fresh and saturated sorbent
    fresh_sorbent = f_FG + R1_FG - A0_FG
    saturated_sorbent = s_FG + A1_FG - R0_FG

    # get time range
    t_DAC_idx_range = range(start_h_DAC_idx, end_h_DAC_idx)
    t_DAC_range = df.loc[t_DAC_idx_range, 'time']

    # bar width
    w = 1 / n_slice

    # --------------------------------------------------------------------------

    _, ax = plt.subplots()

    ax.bar(t_DAC_range,
           fresh_sorbent.iloc[t_DAC_idx_range],
           label="Unalloc. Fresh",
           color="lightblue",
           align="edge",
           width=w)
    ax.bar(t_DAC_range,
           A0_FG.iloc[t_DAC_idx_range],
           bottom=fresh_sorbent.iloc[t_DAC_idx_range],
           label="Alloc. Absorption",
           color="moccasin",
           align="edge",
           width=w)
    ax.bar(t_DAC_range,
           saturated_sorbent.iloc[t_DAC_idx_range],
           bottom=fresh_sorbent.iloc[t_DAC_idx_range] +
           A0_FG.iloc[t_DAC_idx_range],
           label="Unalloc. Saturated",
           color="lightcoral",
           align="edge",
           width=w)
    ax.bar(t_DAC_range,
           R0_FG.iloc[t_DAC_idx_range],
           bottom=fresh_sorbent.iloc[t_DAC_idx_range] +
           A0_FG.iloc[t_DAC_idx_range] +
           saturated_sorbent.iloc[t_DAC_idx_range],
           label="Alloc. Regen.",
           color="plum",
           align="edge",
           width=w)

    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))
    ax.set_xticks(x_ticks)

    ax.legend()

    ax.set_title("DAC-FG Sorbent Allocation")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Mass of Sorbent (Tonne)")
    ax.set_xlim(start_h, end_h)

    f_name = "sorbent_alloc_DAC_FG"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png",
                bbox_inches="tight")


def plot_gross_power(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot out power and gross power from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_power'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    _, ax = plt.subplots()
    ax.stackplot(h_range,
                 df["PowOut"].iloc[h_range],
                 df["PowGross"].iloc[h_range] - df["PowOut"].iloc[h_range],
                 labels=["Out", "Gross"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Power (MW)")
    ax.set_title("Gross Power")
    ax.set_xlim(start_h, end_h)

    f_name = "power_out_and_gross"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_load_and_price(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot load factor and electricity price from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_power'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    f_name = 'results_power_price'
    df_price = pd.read_csv(get_results_path(f_name, model_name=model_name,
                                            ext='csv'))

    _, ax = plt.subplots()

    # plot load factor
    ax.plot(h_range,
            df["x_load_factor"].iloc[h_range], drawstyle="steps-post",
            color="lightcoral",
            label="Load Factor",
            linewidth=2.5)

    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("% Load")
    ax.set_title("Load & Price")
    ax.set_ylim([-3, 103])
    ax.set_xlim(start_h, end_h)

    # plot price
    ax_b = ax.twinx()
    ax_b.plot(h_range,
              df_price.loc[h_range, "price"],
              marker="|",
              label="Price USD/MWh",
              markersize=6,
              color="mediumpurple",
              linewidth=2.5)

    # highest price
    ax_b.hlines(max(df_price.loc[:, "price"]), min(h_range), max(h_range),
                linestyle="dashed",
                label="Max. Price")

    ax_b.set_ylabel("Price $/MWh")
    ax_b.set_ylim(-3, max(df_price.loc[:, "price"] + 3))

    ax.legend()
    ax_b.legend()

    f_name = "load_and_price"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_gen_power(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot generated power from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_power'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    _, ax = plt.subplots()
    ax.stackplot(h_range, df["PowGasTur"].iloc[h_range],
                 df["PowHp"].iloc[h_range],
                 df["PowIp"].iloc[h_range],
                 df["PowLp"].iloc[h_range],
                 labels=["PowGasTur", "PowHp", "PowIp", "PowLp"],
                 colors=["seashell", "tomato", "coral", "crimson"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Power (MW)")
    ax.set_title("Power Generation")
    ax.set_xlim(start_h, end_h)
    # TODO set same y limits
    ax.set_ylim(0, max(df["PowGross"]) * 1.01)

    f_name = "power_generation_stacked"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_ST_gen_power(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot steam turbine generated power from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_power'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    _, ax = plt.subplots()
    ax.stackplot(h_range,
                 df["PowHp"].iloc[h_range],
                 df["PowIp"].iloc[h_range],
                 df["PowLp"].iloc[h_range],
                 labels=["PowHp", "PowIp", "PowLp"],
                 colors=["tomato", "coral", "crimson"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Power (MW)")
    ax.set_title("Power Generation from Steam Turbine")
    ax.set_xlim(start_h, end_h)

    f_name = "power_generation_ST_stacked"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_power_use(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot power consumption from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_power'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    df_power_use = df[["PowUsePcc",
                       "PowUseDacFlue",
                       "PowUseDacAir",
                       "PowUseComp",
                       "eq_total_aux_power_GT",
                       "AuxPowSteaT"]].iloc[h_range]

    _, ax = plt.subplots()

    ax.stackplot(h_range,
                 df_power_use["PowUsePcc"],
                 df_power_use["PowUseDacFlue"],
                 df_power_use["PowUseDacAir"],
                 df_power_use["PowUseComp"],
                 df_power_use["eq_total_aux_power_GT"],
                 df_power_use["AuxPowSteaT"],
                 labels=["PCC",
                         "DAC-FG",
                         "DAC-air",
                         "Compression",
                         "Gas Turbine",
                         "Steam Turbine"],
                 colors=["lightgray", "skyblue", "lightcoral", "lavender",
                         "mediumpurple", "moccasin"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Power (MW)")
    ax.set_title("Power Consumption")
    ax.set_xlim(start_h, end_h)

    f_name = "power_use_stacked"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_CO2(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot CO2 capture from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_CO2'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    df_CO2 = df[["PCC_CO2_cap", "DAC_FG_CO2_cap", "DAC_air_CO2_cap"]].copy()

    # calculate emission
    df_CO2["emission"] = df["fuel_CO2"] - \
        df["PCC_CO2_cap"] - df["DAC_FG_CO2_cap"]
    # # compute the maximum
    # max_CO2 = max(df["fuel_CO2"] + df_CO2["DAC_air_CO2_cap"])
    # ?
    df_CO2.loc[df_CO2["emission"] < 0, "emission"] = 0.0

    _, ax = plt.subplots()

    ax.stackplot(h_range,
                 df_CO2["PCC_CO2_cap"].iloc[h_range],
                 df_CO2["DAC_FG_CO2_cap"].iloc[h_range],
                 df_CO2["emission"].iloc[h_range],
                 df_CO2["DAC_air_CO2_cap"].iloc[h_range],
                 labels=["PCC capture",
                         "DAC-FG capture",
                         "Emissions",
                         "DAC-air capture"],
                 colors=["lightgray", "skyblue", "lightcoral", "lavender"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Tonne CO2/hr")
    ax.set_title("CO2 Capture")
    ax.set_xlim(start_h, end_h)

    f_name = "CO2_capture"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_DAC_CO2(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot DAC CO2 capture from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_CO2'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    df_CO2 = df[["DAC_FG_CO2_cap", "DAC_air_CO2_cap"]].copy()

    # calculate emission
    df_CO2["emission"] = df["fuel_CO2"] - \
        df["PCC_CO2_cap"] - df["DAC_FG_CO2_cap"]
    # # compute the maximum
    # max_CO2 = max(df["fuel_CO2"] + df_CO2["DAC_air_CO2_cap"])
    # ?
    df_CO2.loc[df_CO2["emission"] < 0, "emission"] = 0.0

    _, ax = plt.subplots()

    ax.stackplot(h_range,
                 df_CO2["DAC_FG_CO2_cap"].iloc[h_range],
                 df_CO2["emission"].iloc[h_range],
                 df_CO2["DAC_air_CO2_cap"].iloc[h_range],
                 labels=["DAC-FG capture",
                         "Emissions",
                         "DAC-air capture"],
                 colors=["skyblue", "lightcoral", "lavender"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Tonne CO2/hr")
    ax.set_title("CO2 Capture")
    ax.set_xlim(start_h, end_h)

    f_name = "CO2_capture_DAC"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_PCC_steam(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot PCC steam usage from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_steam'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    _, ax = plt.subplots()

    ax.stackplot(h_range,
                 df["SteaUsePcc"].iloc[h_range],
                 df["eq_PCC_steam_slack"].iloc[h_range],
                 labels=["PCC steam usage", "steam available to PCC"],
                 colors=["skyblue", "lightcoral"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Steam (MMBtu/hr)")
    ax.set_title("PCC steam usage")
    ax.set_xlim(start_h, end_h)

    f_name = "PCC_steam"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_DAC_steam(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot DAC steam usage from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_steam'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    df["DacTotal"] = df["SteaUseDacFlue"] + df["SteaUseDacAir"]

    _, ax = plt.subplots()

    ax.stackplot(h_range,
                 df["DacTotal"].iloc[h_range], 
                 df["DacSteaSlack"].iloc[h_range],
                 labels=["DAC steam usage", "steam available to DAC"],
                 colors=["skyblue", "lightcoral"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Steam (MMBtu/hr)")
    ax.set_title("DAC steam usage")
    ax.set_xlim(start_h, end_h)

    f_name = "DAC_steam"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_DAC_steam_source(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot DAC steam usage from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_steam'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    _, ax = plt.subplots()

    ax.stackplot(h_range,
                 df["DacSteaBaseDuty"].iloc[h_range], 
                 df["SideSteaDac"].iloc[h_range],
                 labels=["Nominal Heat", "Additional Heat (LP)"],
                 colors=["skyblue", "lightcoral"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Heat (MMBtu/hr)")
    ax.set_title("DAC Steam Source")
    ax.set_xlim(start_h, end_h)

    f_name = "DAC_steam_source"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_cost(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot operational cost from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    h_arange = np.arange(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_cost'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    # negative emission
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "negative_emission"] = abs(df.loc[:, "cost_CO2_emission"])
    df.loc[df.loc[:, "cost_CO2_emission"] >= 0, "negative_emission"] = 0.0
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "cost_CO2_emission"] = 0.0

    _, ax = plt.subplots()

    # width
    w = 0.25

    ax.bar(h_arange - 2 * w, df["cost_natural_gas"].iloc[h_range],
           width=w,
           color="skyblue",
           align="edge",
           label="Natural Gas")
    ax.bar(h_arange - w, df["cost_transportation"].iloc[h_range],
           width=w,
           color="lavender",
           align="edge",
           label="Transportation")
    ax.bar(h_arange, df["negative_emission"].iloc[h_range],
           width=w,
           color="lightgray",
           align="edge",
           label="Negative Emissions")
    ax.bar(h_arange + w, df["cost_CO2_emission"].iloc[h_range],
           width=w,
           color="lightcoral",
           align="edge",
           label="Emissions")

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("USD/hr")
    ax.set_title("Operational Cost")
    ax.set_xlim(start_h, end_h)

    f_name = "cost"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_cost_stacked(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot stacked operational cost from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_cost'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    # negative emission
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "negative_emission"] = abs(df.loc[:, "cost_CO2_emission"])
    df.loc[df.loc[:, "cost_CO2_emission"] >= 0, "negative_emission"] = 0.0
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "cost_CO2_emission"] = 0.0

    _, ax = plt.subplots()
    ax.stackplot(h_range,
                 df["cost_natural_gas"].iloc[h_range],
                 df["cost_transportation"].iloc[h_range],
                 df["cost_CO2_emission"].iloc[h_range],
                 labels=["Natural Gas", "Transportation", "Emissions"],
                 colors=["skyblue", "lavender", "lightcoral"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("USD/hr")
    ax.set_title("Operational Cost")
    ax.set_xlim(start_h, end_h)
    ax.set_ylim(0, max(df["cost_natural_gas"] + df["cost_transportation"] + df["cost_CO2_emission"]))

    f_name = "cost_stacked"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_negative_emission(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot stacked operational cost from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_cost'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    # negative emission
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "negative_emission"] = abs(df.loc[:, "cost_CO2_emission"])
    df.loc[df.loc[:, "cost_CO2_emission"] >= 0, "negative_emission"] = 0.0
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "cost_CO2_emission"] = 0.0

    _, ax = plt.subplots()
    ax.stackplot(h_range,
                 df["negative_emission"].iloc[h_range],
                 labels=["Negative Emissions"],
                 colors=["crimson"])

    ax.legend()
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Hour")
    ax.set_ylabel("USD/hr")
    ax.set_title("Negative Emissions")
    ax.set_xlim(start_h, end_h)
    ax.set_ylim(0, max(df["cost_natural_gas"] + df["cost_transportation"] + df["cost_CO2_emission"]))

    f_name = "negative_emission"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_profit(start_h=5090, delta_h=80, model_name='m14'):
    """
    Plot profit profile from start_h to start_h + delta_h.
    """

    # ending hour
    end_h = start_h + delta_h

    # time range
    h_range = range(start_h, end_h)
    # x ticks
    x_ticks = np.arange(start_h, end_h + 1, step=int((end_h - start_h) / 4))

    f_name = 'results_cost'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))
    # negative emission
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "negative_emission"] = abs(df.loc[:, "cost_CO2_emission"])
    df.loc[df.loc[:, "cost_CO2_emission"] >= 0, "negative_emission"] = 0.0
    df.loc[df.loc[:, "cost_CO2_emission"] < 0, "cost_CO2_emission"] = 0.0
    # profit
    profit = df.loc[:, "power_sale"] + df.loc[:, "negative_emission"] - \
        df.loc[:, "cost_CO2_emission"] - df.loc[:, "cost_natural_gas"] - df.loc[:, "cost_transportation"]

    _, ax = plt.subplots()

    profit.to_csv("profit.csv")

    # positive part
    profit_p = profit.copy()
    profit_p.loc[profit_p.iloc[:] < 0] = 0
    # negative part
    profit_n = profit.copy()
    profit_n.loc[profit_n.iloc[:] >= 0] = 0
    # get the maximum and minimum profit to scale the y-axis
    min_profit = min(profit_n)
    max_profit = max(profit_p)
    ax.bar(h_range, profit_p.iloc[h_range],
           color="cornflowerblue",
           label="gains",
           align="edge",
           width=0.8)
    ax.bar(h_range, profit_n.iloc[h_range],
           color="lightcoral",
           label="losses",
           align="edge",
           width=0.8)
    ax.hlines(max_profit, min(h_range), max(h_range),
              linestyle="dashed",
              label="Max. Profit",
              color="cornflowerblue")
    ax.hlines(min_profit, min(h_range), max(h_range),
              linestyle="dashed",
              label="Max. Loss",
              color="lightcoral")


    ax.set_title("Profit")
    ax.set_xlabel("Hour")
    ax.set_ylabel("USD/hr")
    ax.set_xlim(start_h, end_h)
    ax.set_ylim(min_profit * 1.1, max_profit * 1.01)

    ax.legend()
    ax.set_xticks(x_ticks)
    # plot horizontal line at 0
    plt.axhline(0)

    f_name = "profit"
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


if __name__ == "__main__":

    model_name = 'one-piece'

    # plot_sorbent_air_inventory()
    # plot_sorbent_FG_inventory()
    # plot_gross_power()
    # plot_load_and_price()
    # plot_gen_power()
    # plot_ST_gen_power()
    # plot_power_use()
    # plot_CO2()
    # plot_DAC_CO2()
    # plot_PCC_steam()
    # plot_DAC_steam()
    # plot_DAC_steam_source()
    # plot_cost()
    # plot_cost_stacked()
    # plot_negative_emission()
    # plot_profit()

    plot_sorbent_air_inventory(start_h=0, delta_h=80, model_name='one-piece')