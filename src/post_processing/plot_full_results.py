"""
Plotting module with functions to generate plots for the whole time period. All
output images are 16 x 4 (or 16 x 2).

Available functions:

    plot_modes: plot the running modes of two natural gas turbines.
        input: results_binary_vars.csv
        output: results_binary_vars.png or results_schedule.png

    plot_heat_frac: plot the fraction of heat utilized by DAC.
        input: results_steam.csv
        output: results_heat_frac.png

    plot_alloc_load_price: plot heat allocation, load and price.
        input: results_power.csv results_power_price.csv results_steam.csv
        output: heat_load_price.png

    plot_profit: plot profit profile.
        input: results_cost.csv
        output: results_profit.png

    plot_heat_allocation_DAC: plot heat utilized by DAC.
        input: results_steam.csv
        output: DAC_steam.png
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import generate_rec_data, preprocess_binary_results, get_results_path


def plot_modes(model_name='m14', plot_mode='step'):
    """Plot the modes of two natural gas turbines for the whole time period.

    In the result csv file, y is formulated as y11:
    - first digit represents unit (0 to 1)
    - second digit represents mode (0 to 3)

    plot_mode:
    - 'step': draw as step function
    - 'schedule': draw as blocks (only with value 1)

    Output:
        (16 x 4) figure
    """

    # read result csv
    f_name = "results_binary_vars"
    df = pd.read_csv(get_results_path(f_name, model_name=model_name, ext='csv'))

    # create figure
    _, axes = plt.subplots(2, 1, figsize=(16, 4), dpi=300, sharex=True)

    # --------------------------------------------------------------------------

    units = ['a', 'b']
    modes = ["off", "cold start", "warm start", "on"]
    colors = ["gray", "blue", "red", "orange"]
    # height factor
    h_factor = 1.75

    # one plot for each unit
    for i, unit in enumerate(units):

        # get the current ax
        ax = axes[i]
        plt.sca(ax)

        # plot each mode
        for j, mode in enumerate(modes):

            # height
            h = h_factor * j
            # column name
            col = "y" + str(i) + str(j)

            # baseline
            ax.hlines(h, min(df.index)-1, max(df.index)+1, color="k",
                      alpha=0.1)

            # step mode
            if plot_mode == 'step':

                # preprocess data
                x, y = preprocess_binary_results(df.index, df[col])

                # state as step function
                ax.step(x, [_y + h for _y in y],
                        label=mode,
                        color=colors[j],
                        # linestyle="dotted",
                        # marker=".",
                        # fillstyle="none"
                        )

            # schedule mode
            elif plot_mode == 'schedule':

                # preprocess data
                rec_data = generate_rec_data(df.index, df[col])

                # state line
                ax.broken_barh(rec_data, [h - 0.5 * h_factor, h_factor],
                               label=mode,
                               color=colors[j],
                               # linestyle="dotted",
                               # marker=".",
                               # fillstyle="none"
                               )
            else:
                raise ValueError("Wrong plot mode!")

            # add label
            if plot_mode == 'step':
                ax.text(-7.5, h + 0.15, mode, horizontalalignment='right',
                        verticalalignment='center')
            else:  # 'schedule'
                ax.text(-7.5, h, mode, horizontalalignment='right',
                        verticalalignment='center')

        # add unit label
        ax.text(-60, h_factor * (len(modes) - 1) / 2, 'unit ' + unit,
                horizontalalignment='center',
                verticalalignment='center', rotation='vertical')

        # ----------------------------------------------------------------------

        # # remove spines
        # ax.spines['left'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        # ax.spines['top'].set_visible(False)

        # make sure the x axis start from 0
        ax.set_xlim(0, df.index[-1])

        # add the final index as extra tick
        original_ticks = list(ax.get_xticks())[:-1]
        new_ticks = original_ticks + [df.index[-1]]
        plt.xticks(new_ticks)

        # remove y ticks
        ax.set_yticks([])

        # set x label
        if unit == 'b':
            ax.set_xlabel('hour')

        # show grid
        ax.grid(True)

    plt.tight_layout()

    # save figure
    if plot_mode == 'schedule':
        f_name = 'results_schedule'
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png",
                # transparent=True,
                bbox_inches="tight")


def plot_heat_frac(model_name='m14'):
    """Plot the fraction of heat utilized by DAC."""

    # read from results_steam
    f_name = 'results_steam'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    # calculate DAC heat usage ratio
    df["heat_frac"] = df["x_steam_DAC_extra"] / df["x_steam_allocable"]

    # preprocess the data (remove redundant values)
    x, y = preprocess_binary_results(df.index, df['heat_frac'])

    _, ax = plt.subplots(figsize=(16, 2), dpi=300)
    ax.step(x, y,
            marker=".",
            fillstyle="none",
            color="firebrick",
            # linestyle="dashed"
            )

    f_name = 'results_heat_frac'
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    plt.savefig(f_path, format="png")


def plot_alloc_load_price(model_name='m14'):
    """Plot heat allocation, load and price in the same plot."""

    # read data
    df_power = pd.read_csv(get_results_path(
        'results_power', model_name=model_name, ext='csv'))
    df_price = pd.read_csv(get_results_path(
        'results_power_price', model_name=model_name, ext='csv'))
    df_steam = pd.read_csv(get_results_path(
        'results_steam', model_name=model_name, ext='csv'))

    # calculate heat frac
    df_steam["heat_frac"] = df_steam["x_steam_DAC_extra"] / \
        df_steam["x_steam_allocable"] * 100

    _, ax = plt.subplots(figsize=(16, 2), dpi=300)

    # plot load factor
    l1 = ax.plot(df_power.index, df_power["x_load_factor"],
                 color="lime",
                 label="% GT Load",
                 alpha=0.6
                 )

    # plot heat frac
    l2 = ax.plot(df_steam.index, df_steam["heat_frac"],
                 marker=None,
                 fillstyle="none",
                 color="red",
                 linestyle="dashed",
                 label="% Heat DAC",
                 alpha=0.6
                 )

    # set labels
    ax.set_xlabel("Hour")
    ax.set_ylabel("%")
    # set title
    ax.set_title("Load factor, DAC heat fraction, and power price")
    # set x range
    ax.set_xlim([0, df_steam.index[-1]])
    # set y range
    ax.set_ylim([-3, 103])

    # create twin axes sharing axis
    axb = ax.twinx()

    # plot price
    l3 = axb.plot(df_price.index, df_price["price"],
                  color="orange", label="Price", alpha=0.6)
    # set ylabel on the right
    axb.set_ylabel("USD/MWh")

    # add legend
    lns = l1 + l2 + l3
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, bbox_to_anchor=(1.05, 0.75))

    # save fig
    f_path = get_results_path('heat_load_price', model_name=model_name,
                              ext='png')
    plt.savefig(f_path, format="png", bbox_inches="tight")


def plot_profit(model_name='m14'):
    """Plot profit profile."""

    # read from results cost
    f_name = 'results_cost'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    profit = df.loc[:, "x_power_out"] - df.loc[:, "x_vent_CO2"] - \
        df.loc[:, "x_compress_CO2"] - df.loc[:, "x_fuel"]

    profit_p = profit.copy()
    profit_p.loc[profit_p.iloc[:] < 0] = 0

    profit_n = profit.copy()
    profit_n.loc[profit_n.iloc[:] >= 0] = 0

    # get maximum and minimum profit to scale y-axis
    min_profit = min(profit_n)
    max_profit = max(profit_p)

    fig, ax = plt.subplots(figsize=(16, 2), dpi=300)

    # surplus
    ax.bar(profit_p.index, profit_p, color="cornflowerblue", label="surplus")

    # deficit
    ax.bar(profit_n.index, profit_n, color="lightcoral", label="deficit")

    # baseline
    ax.hlines(0.0, min(df.index)-1, max(df.index)+1,
              color="k",
              #  linestyle="dotted",
              linewidth=1,
              )

    # set x range
    ax.set_xlim(0, df.index[-1])

    # # hide spines
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_visible(False)

    # plot legend
    ax.legend()

    # # set title
    # ax.set_title("Value")

    # set label
    ax.set_xlabel("hour")
    ax.set_ylabel("USD/hr")

    plt.tight_layout()

    f_name = 'results_profit'
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    fig.savefig(f_path, bbox_inches="tight")


def plot_heat_allocation_DAC(model_name='m14'):
    """Plot the heat used by DAC."""

    f_name = 'results_steam'
    df = pd.read_csv(get_results_path(
        f_name, model_name=model_name, ext='csv'))

    fig, ax = plt.subplots(figsize=(16, 2), dpi=300)

    ax.stackplot(df.index,
                 df["x_steam_DAC_base"], df["x_steam_DAC_extra"],
                 labels=["Nominal Heat", "Additional Heat (LP)"],
                 colors=["pink", "skyblue"])

    ax.legend()

    ax.set_xlabel("hour")
    ax.set_ylabel("heat (MMBtu/hr)")
    ax.set_title("Dac Steam Source")

    plt.tight_layout()

    f_name = 'DAC_steam'
    f_path = get_results_path(f_name, model_name=model_name, ext='png')
    fig.savefig(f_path, bbox_inches="tight")


if __name__ == "__main__":

    model_name = 'one-piece'
    # plot_modes()
    # plot_modes(plot_mode='schedule')
    plot_alloc_load_price(model_name=model_name)
    plot_profit(model_name=model_name)
    plot_heat_allocation_DAC(model_name=model_name)

    plot_modes(model_name=model_name, plot_mode='schedule')
