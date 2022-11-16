import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from ema_workbench.analysis import plotting as emaplt
from matplotlib import pyplot as plt
from matplotlib.patches import ConnectionPatch
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

from src.datamanager import DataManager
from src.utils import filter_dict
import logging

plt.rcParams.update({'font.size': 16})

# plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Tahoma']


# plt.tight_layout()
# plt.subplots_adjust(left=-0.2, bottom=0.1, right=1.2, top=1)


def set_aspect(ax1, ratio):
    """
    :type ax1: axes to modify
    :type ratio: define y-unit to x-unit ratio
    """
    # get x and y limits
    x_left, x_right = ax1.get_xlim()
    y_low, y_high = ax1.get_ylim()
    # set aspect ratio
    ax1.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)
    # raise NotImplementedError()


def plot_experiments(outcomes_df, datamanager: DataManager = None, outcome_selector=None, experiment_selector=None,
                     code_black=None, legend_override=None, y_units='', add_scenario_count=True, **kwargs):
    time = outcomes_df['TIME']

    if outcome_selector is not None:
        df_to_plot = outcomes_df[outcome_selector]
        save_name = '_'.join(outcome_selector)
    else:
        df_to_plot = outcomes_df
        save_name = 'all'

    if experiment_selector is not None:
        time = time.loc[experiment_selector]
        df_to_plot = df_to_plot.loc[experiment_selector]

    # fig, ax1 = plt.subplots(constrained_layout=True)
    fig, ax1 = plt.subplots()
    ax1.axhline(y=0, color='black', linestyle='dashed', linewidth=1)

    for i, col in enumerate(df_to_plot):
        for index, single_output in df_to_plot[col].groupby(level=0):
            time = outcomes_df.loc[index, 'TIME']
            if legend_override is not None:
                legend = legend_override[index]
            else:
                legend = col

            if add_scenario_count:
                legend = legend + ": scenario " + str(index)

            ax1.plot(time, single_output, label=legend, **kwargs)
            ax1.set_ylabel(y_units)
            # set y-axis limit to a displayable value
            ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

            plt.locator_params(nbins=5)

    x_label = "Time (Day)"
    ax1.set_xlabel(x_label)

    if code_black is not None:
        shape = (time.shape[0],)
        limit = np.full(shape, code_black)
        ax1.plot(time, limit, label='Capacity', **kwargs)

    set_aspect(ax1, 9 / 16)
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=1)

    plt.tight_layout()
    # plt.subplots_adjust(left=-0.3, bottom=0.2, right=1.3, top=0.8)

    if datamanager is not None:
        plt.savefig(os.path.join(datamanager.get_time_series_plots_path(), save_name))
    plt.show()


def scatter(experiments, outcomes, outcome_selector, datamanager: DataManager, legend=True, experiments_to_show=None,
            code_black=None):
    if len(outcome_selector) != 2:
        raise RuntimeError('only scatter plot with 2 dimensions is supported')

    scatter_data = filter_dict(outcomes, outcome_selector)
    for key, val in scatter_data.items():
        filtered_val = val[experiments_to_show]
        scatter_data[key] = filtered_val
    time = (filter_dict(outcomes, ['TIME'])['TIME'])[
        experiments_to_show]  # make sure time is an array, and not a matrix (it's not 100%, but for now it is good?)

    x = list(scatter_data.items())[0][1]
    y = list(scatter_data.items())[1][1]
    c = time
    plt.title("sample text")
    plt.xlabel(list(scatter_data.items())[0][0])
    plt.ylabel(list(scatter_data.items())[1][0])
    plot_name = '{}_vs_{}'.format(outcome_selector[0], outcome_selector[1])
    plt.scatter(x, y, cmap=None)
    plt.savefig(os.path.join(datamanager.scatter_plots_path, plot_name))
    plt.show()


def plot_experiments_old(experiments, outcomes, datamanager: DataManager, outcome_selector=None,
                         experiment_selector=None,
                         code_black=None):
    # select columns to plot
    if outcome_selector is not None:
        outcome_selector.append('TIME')
        dict_to_plot = filter_dict(outcomes, outcome_selector)
        save_name = '_'.join(outcome_selector)
    else:
        dict_to_plot = outcomes
        save_name = 'all'

    # generate capacity limit curve
    if code_black is not None:
        time = dict_to_plot['TIME']
        shape = (1, time.shape[1])
        limit = np.full(shape, code_black)
        for outcome in outcome_selector:
            if outcome != 'TIME':
                # append code_black as another outcome line
                dict_to_plot[outcome] = np.vstack([dict_to_plot[outcome], limit])
            else:
                # append one more row to time
                new_time = np.vstack([time, time[0:1, :]])
                dict_to_plot['TIME'] = new_time
        # add 1 more row to 'experiments' (bc ema_workbench internal structure)
        experiments = pd.concat([experiments, experiments.iloc[0:1, :]])
        experiments = experiments.reset_index()
        # experiments['scenario']
        # reshape experiment selector, so we can add the last element
        if experiment_selector is not None:
            # experiment_selector = list(experiment_selector).append(-1)
            # jfc this is very ugly (it converts a slice to a list and adds the last to the end (to select code black)
            experiment_selector = list(range(experiment_selector.start or 0, experiment_selector.stop,
                                             experiment_selector.step or 1))
            experiment_selector.append(time.shape[0])
        emaplt.lines(experiments, dict_to_plot, experiments_to_show=experiment_selector, density=emaplt.Density.KDE)
    else:
        emaplt.lines(experiments, dict_to_plot, experiments_to_show=experiment_selector, density=emaplt.Density.KDE)
    plt.savefig(os.path.join(datamanager.get_time_series_plots_path(), save_name))
    plt.show()


def plot_clusters(experiments, outcomes_df, outcome_selector, clusters_df, cluster_to_plot):
    # abandoned!!!
    if len(outcome_selector) != 1:
        raise NotImplementedError()
    outcome_selector = str(outcome_selector[0])
    time_series_to_plot = outcomes_df[outcome_selector]
    clusters_df = clusters_df.reset_index()
    in_cluster_experiment_ids = clusters_df[clusters_df['PIC'] == cluster_to_plot].loc[:, 'index']

    time_series_to_plot = time_series_to_plot.reset_index().reindex()

    mask = time_series_to_plot.loc[:, 'experiment_id'].isin(in_cluster_experiment_ids)
    time_series_to_plot = time_series_to_plot[mask]
    grey_mask = not mask
    time_series_to_plot_in_grey = time_series_to_plot[grey_mask]

    # https://stackoverflow.com/questions/26255671/pandas-column-values-to-columns
    series_to_plot = time_series_to_plot.groupby(['data_point_id', 'experiment_id'])[outcome_selector].aggregate(
        'first').unstack()

    deb = 0 + 1
    # sns.lineplot(outcomes[outcome_selector[0]])
    raise NotImplementedError()


# bare-bones style:
def plot_bar(outcomes_df, datamanager: DataManager = None, outcome_selector=None, experiment_selector=None,
             code_black=None, legend_override=None, y_units='', add_scenario_count=True, **kwargs):
    df_to_plot = outcomes_df[outcome_selector]
    df_to_plot = df_to_plot.loc[experiment_selector]

    fig, ax1 = plt.subplots()
    ax1.axhline(y=0, color='black', linestyle='dashed', linewidth=1)

    for i, col in enumerate(df_to_plot):
        for index, single_output in df_to_plot[col].groupby(level=0):
            time = outcomes_df.loc[index, 'TIME']

            legend = legend_override[index]

            # bar graph grouping
            n = 7  # days to group
            time = time[time.index % n == 0]
            single_output = single_output.droplevel(level=0)
            single_output = single_output.groupby(single_output.index // n).sum()

            single_output_positive = single_output.apply(lambda a: a if a >= 0 else 0)
            single_output_negative = single_output.apply(lambda a: a if a <= 0 else 0)

            # offset for multi-bar plot https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
            w = 2  # width of the bars
            offset = w
            if index == 0:
                ax1.bar(time + offset, single_output_positive, color='#1f77b4', width=w, **kwargs)
                ax1.bar(time + offset, single_output_negative, color='#1f77b4', width=w, label=legend, **kwargs)
            if index == 1:
                ax1.bar(time, single_output_positive, color='#ff7f0e', width=w, **kwargs)
                ax1.bar(time, single_output_negative, color='#ff7f0e', width=w, label=legend, **kwargs)

            if index == 2:
                ax1.bar(time - offset, single_output_positive, color='#2ca02c', width=w, **kwargs)
                ax1.bar(time - offset, single_output_negative, color='#2ca02c', width=w, label=legend, **kwargs)

            ax1.set_ylabel(y_units)
            # set y-axis limit to a displayable value
            ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

            plt.locator_params(nbins=5)

    x_label = "Time (Day)"
    ax1.set_xlabel(x_label)

    set_aspect(ax1, 9 / 16)
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=1)

    plt.tight_layout()
    plt.show()
