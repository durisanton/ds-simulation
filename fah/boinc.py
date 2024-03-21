import statistics
from typing import Optional

import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from petnetsim import PetriNet

from fah.models import Params
from fah.nets.boinc_net import BoincNet
from fah.utils.constants import Constants


class BoincSimulation:
    def __init__(self):
        self.boinc_net: Optional[PetriNet] = None
        self.params: Params = Params.init()
        self.place_tokens: dict[str: list[int]] = dict()
        self.place_time: dict[str: float] = dict()
        self.time_computed: list[float] = list()
        self.stats: dict[str: dict[str: int]] = dict()
        self.time: dict[int: list[float]] = dict()

    def make_net(self) -> bool:
        self.boinc_net = BoincNet(params=self.params).make_net()
        if self.boinc_net is None:
            return False
        return True

    # one run of simulation
    def single_run(self) -> None:
        # main loop
        while not self.boinc_net.ended and self.boinc_net.step_num < self.params.max_steps:
            self.boinc_net.step()
            # filling dictionaries
            for p in self.boinc_net.places:
                self.place_tokens.setdefault(p.name, list()).append(p.tokens)
                self.place_time.setdefault(p.name, list()).append(self.boinc_net.time)
                if p.name == 'project_computed' and p.tokens == 1:
                    self.time_computed.append(self.boinc_net.time)

    # more runs of simulation, data are saved in stats
    def in_loop_run(self, stats_loop: int) -> None:
        # make new nets with changed probabilities
        self.make_net()
        # loop run and filling stats for each loop
        for loop in range(1, self.params.loops + 1):
            self.boinc_net.reset()
            while not self.boinc_net.ended and self.boinc_net.step_num < self.params.max_steps:
                self.boinc_net.step()
            for p in self.boinc_net.places:
                self.stats.setdefault(f'loop_{loop}', dict()).setdefault(f'{p.name}', list()).append(p.tokens)
                self.stats[f'loop_{loop}']['time'] = self.boinc_net.time
            self.time.setdefault(stats_loop, list()).append(self.boinc_net.time)

    def pause_simulation(self) -> None:
        self.params.in_pause_min_time = [i * 10 for i in self.params.in_pause_min_time]  # for better visualization
        self.params.in_pause_max_time = [i * 10 for i in self.params.in_pause_max_time]
        for stats_loop in range(0, self.params.stats_loops):
            self.in_loop_run(stats_loop=stats_loop)
            # change probability of pause in each loop
            self.params.pause_on_probability = [i - .1 for i in self.params.pause_on_probability]
            self.params.pause_off_probability = [i + .1 for i in self.params.pause_off_probability]

    def deadline_simulation(self):
        # initial setup for deadline simulation
        self.params.job_running_probability = [1, 1, 1, 1, 1]
        self.params.job_crash_probability = [0, 0, 0, 0, 0]
        for stats_loop in range(0, self.params.stats_loops):
            self.in_loop_run(stats_loop=stats_loop)
            # change probability of "project deadline"
            self.params.job_running_probability = [i - .1 for i in self.params.job_running_probability]
            self.params.job_crash_probability = [i + .1 for i in self.params.job_crash_probability]

            # change computation time for "project deadline" simulation
            self.params.compute_1_max_time = [i + 100 for i in self.params.compute_1_max_time]
            self.params.compute_2_max_time = [i + 100 for i in self.params.compute_2_max_time]

    # for plotting deadline stats
    def plot_deadline(self) -> Figure:
        fig, axs = plt.subplots(nrows=1, ncols=1, facecolor='w', edgecolor='k', sharex=True)
        if not self.make_net():
            return fig
        self.deadline_simulation()
        mean: list[float] = [statistics.mean(self.time[i]) for i in range(self.params.stats_loops)]
        std: list[float] = [statistics.stdev(self.time[i]) for i in range(self.params.stats_loops)]
        ind: list[int] = [i for i in range(self.params.stats_loops)]
        # plot requests for each microservice
        fig.subplots_adjust(hspace=.5, wspace=.1)
        fig.suptitle(t='Duration of project computation', fontsize=16)
        axs.bar(x=ind, height=mean, width=.1, yerr=np.array(std), label='time')
        axs.axhline(y=2500, color='k', linestyle='--', label='deadline')
        axs.legend(fontsize=16)
        axs.set_ylabel(ylabel='time [s]', fontsize=16)
        axs.set_xticks(ind)
        axs.set_xticklabels(labels=Constants.deadline_plot_labels, fontsize=16)
        axs.set_xlabel(xlabel='computation time [s]', fontsize=16)
        axs.grid(axis='y')
        return fig

    # plot deadline; job pause method
    def plot_pause_deadline(self):
        fig, axs = plt.subplots(nrows=1, ncols=1, facecolor='w', edgecolor='k', sharex=True)
        if not self.make_net():
            return fig
        self.pause_simulation()
        mean: list[float] = [statistics.mean(self.time[i]) for i in range(self.params.stats_loops)]
        std: list[float] = [statistics.stdev(self.time[i]) for i in range(self.params.stats_loops)]
        ind: list[int] = [i for i in range(self.params.stats_loops)]
        # plot requests for each microservice
        fig.subplots_adjust(hspace=.5, wspace=.1)
        fig.suptitle(t='Duration of project computation', fontsize=16)
        axs.bar(x=ind, height=mean, width=.1, yerr=np.array(std), label='time')
        axs.legend(fontsize=16)
        axs.set_ylabel(ylabel='time [s]', fontsize=16)
        axs.set_xticks(ticks=ind)
        axs.set_xticklabels(labels=Constants.pause_plot_labels, fontsize=16)
        axs.set_xlabel(xlabel='probability [%]', fontsize=16)
        axs.grid(axis='y')
        return fig

    def plot_stats(self) -> Figure:
        fig, axs = plt.subplots(nrows=1, ncols=1, facecolor='w', edgecolor='k', sharex=True)
        if not self.make_net():
            return fig
        ind: list[int] = [i + 1 for i in range(self.params.loops)]
        time: list[float] = [self.stats[f'loop_{loop}']['time'] for loop in range(1, self.params.loops + 1)]
        # plot requests for each microservice
        fig.subplots_adjust(hspace=.5, wspace=.1)
        fig.suptitle(t='Duration of project computation', fontsize=16)
        axs.bar(x=ind, height=time, width=.1, label='time')
        axs.legend()
        axs.set_ylabel(ylabel='time [s]')
        axs.set_xlabel(xlabel='loop')
        return fig

    def plot_gant(self):
        """
            gant plot of basic setup of nets
        """
        fig: Figure = plt.figure(figsize=(20, 8))
        if not self.make_net():
            return fig
        self.single_run()
        ax: Axes = fig.add_subplot(111)
        fig.suptitle(t='Number of results for individual tasks', fontsize=16)
        for i in range(1, self.params.tasks + 1):
            start_time: float = 0.0
            results_counter: list[int] = self.place_tokens[f'task{i}_results_counter']
            weights: list[int] = [i for i in range(max(results_counter))]
            norm: Normalize = mp.colors.Normalize(vmin=min(weights), vmax=max(weights))
            cmap: ScalarMappable = mp.cm.ScalarMappable(norm=norm, cmap=Constants.cmaps[i])
            cmap.set_array([])
            for j in range(0, max(results_counter)):
                idx: int = max(index for index, item in enumerate(results_counter) if item == j)
                end_time: float = self.place_time[f'task{i}_results_counter'][idx]
                if start_time > 0:
                    ax.barh(i - 1, end_time - start_time, left=start_time, height=0.3, align='center', alpha=0.8,
                            color=cmap.to_rgba(j))
                else:
                    pass
                start_time = end_time
        ax.axvline(x=self.time_computed[0], color='k', linestyle='-.', label='project computed')
        ax.legend()
        ax.set_yticks([i for i in range(self.params.tasks)])
        ax.set_yticklabels(labels=[f'Task {i+1}' for i in range(self.params.tasks)])
        ax.set_xlabel(xlabel='time [s]')
        # ax.set_xlim(xmin = 0, xmax = time_computed + 200)
        # ax.grid(color = 'g', linestyle = ':')
        return fig

    def basic_info(self):
        print('CONFLICT GROUPS')
        print(self.boinc_net.conflict_groups_str)
        print('------------------------------------')
        self.boinc_net.reset()
        print('INITIAL TOKENS:')
        self.boinc_net.print_places()
        print('------------------------------------')
        print('TRANSITIONS STATS:')
        for t in self.boinc_net.transitions:
            print(t.name, t.fired_times, sep=': ')
        print('------------------------------------')
        print('PLACES STATS:')
        self.boinc_net.print_places()


if __name__ == '__main__':
    BoincSimulation().make_net()
