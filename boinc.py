import json
from typing import Dict, List

import matplotlib.pyplot as plt
import matplotlib as mp
import statistics
import numpy as np
from petnetsim import PetriNet

from nets.boinc_net import BoincNet
from params import NetParams


class BoincSimulation:
    def __init__(self):
        self.boinc_net = None
        self.params = None
        self.place_tokens: Dict = dict()
        self.place_time: Dict = dict()
        self.time_computed: List = list()
        self.stats = dict()
        self.time = dict()

    @staticmethod
    def load_params() -> NetParams:
        with open(file='params.json') as file:
            params = NetParams.from_dict(json.load(file))
        return params

    def make_net(self):
        self.boinc_net: PetriNet = BoincNet(params=self.params).make_net()

    def main(self):
        self.params: NetParams = self.load_params()
        self.make_net()

        self.run()
        self.loop_run()

        # uncomment for simulation
        self.basic_info()
        self.plot_pause_deadline()
        self.plot_deadline()
        self.plot_gant()
        plt.show()

    # one run of simulation
    def run(self):
        for p in self.boinc_net.places:
            self.place_tokens[p.name] = list()
            self.place_time[p.name] = list()
        # main loop
        while not self.boinc_net.ended and self.boinc_net.step_num < self.params.max_steps:
            self.boinc_net.step()
            # filling dictionaries
            for p in self.boinc_net.places:
                self.place_tokens[p.name].append(p.tokens)
                self.place_time[p.name].append(self.boinc_net.time)
                if p.name == 'project_computed' and p.tokens == 1:
                    self.time_computed.append(self.boinc_net.time)

    # more runs of simulation, data are saved in stats
    def loop_run(self):
        ## used for simulating pause statistics; uncomment for this kind of simulation
        # in_pause_min_time = np.array(in_pause_min_time) * 10   #for better visualization
        # in_pause_max_time = np.array(in_pause_max_time) * 10

        # initial setup for deadline simulation
        # job_running_probability = [1, 1, 1, 1, 1]
        # job_crash_probability = [0, 0, 0, 0, 0]

        # loop for make some statistics data
        for i in range(0, self.params.stats_loops):
            self.time[i] = []
            # make new nets with changed probabilities
            self.make_net()
            # loop run and filling stats for each loop
            for loop in range(1, self.params.loops + 1):
                self.boinc_net.reset()
                self.stats[f'loop_{loop}'] = dict()

                while not self.boinc_net.ended and self.boinc_net.step_num < self.params.max_steps:
                    self.boinc_net.step()

                for p in self.boinc_net.places:
                    self.stats[f'loop_{loop}'][f'{p.name}'] = []
                    self.stats[f'loop_{loop}'][f'{p.name}'].append(p.tokens)

                self.time[i].append(self.boinc_net.time)

            ## change probability of pause in each loop; uncomment for this simulation
            # pause_on_probability = np.array(pause_on_probability) - 0.1
            # pause_off_probability = np.array(pause_off_probability) + 0.1

            ## change probability of "project deadline"; uncomment for this simulation
            # job_running_probability = np.array(job_running_probability) - 0.1
            # job_crash_probability = np.array(job_crash_probability) + 0.1

            ## change computation time for "project deadline" simulation
            self.params.compute_1_max_time = np.array(self.params.compute_1_max_time) + 100
            self.params.compute_2_max_time = np.array(self.params.compute_2_max_time) + 100

    # for plotting deadline stats
    def plot_deadline(self):
        mean = []
        std = []
        for i in range(0, self.params.stats_loops):
            mean.append(statistics.mean(self.time[i]))
            std.append(statistics.stdev(self.time[i]))

        ind = np.arange(self.params.stats_loops)
        width = 0.1
        # plot requests for each microservice
        fig, axs = plt.subplots(1, 1, facecolor='w', edgecolor='k', sharex=True)
        fig.subplots_adjust(hspace=.5, wspace=.1)
        fig.suptitle('Duration of project computation', fontsize=16)
        axs.bar(ind, mean, width, yerr=np.array(std), label='time')
        axs.axhline(y=2500, color='k', linestyle='--', label='deadline')
        axs.legend(fontsize=16)
        axs.set_ylabel('time [s]', fontsize=16)

        labels = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]

        axs.set_xticks(ind)
        axs.set_xticklabels(labels, fontsize=16)
        axs.set_xlabel('computation time [s]', fontsize=16)

        axs.grid(axis='y')

    # plot deadline; job pause method
    def plot_pause_deadline(self):
        mean = []
        std = []
        for i in range(0, self.params.stats_loops):
            mean.append(statistics.mean(self.time[i]))
            std.append(statistics.stdev(self.time[i]))

        ind = np.arange(self.params.stats_loops)
        print(mean)
        width = 0.1
        # plot requests for each microservice
        fig, axs = plt.subplots(1, 1, facecolor='w', edgecolor='k', sharex=True)
        fig.subplots_adjust(hspace=.5, wspace=.1)
        fig.suptitle('Duration of project computation', fontsize=16)
        axs.bar(ind, mean, width, yerr=np.array(std), label='time')
        axs.legend(fontsize=16)
        axs.set_ylabel('time [s]', fontsize=16)

        labels = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

        axs.set_xticks(ind)
        axs.set_xticklabels(labels, fontsize=16)
        axs.set_xlabel('probability [%]', fontsize=16)

        axs.grid(axis='y')

    def plot_stats(self):
        ind = np.arange(self.params.loops)
        time = []
        for loop in range(1, self.params.loops + 1):
            time.append(self.stats[f'loop_{loop}']['time'])
        width = 0.1
        # plot requests for each microservice
        fig, axs = plt.subplots(1, 1, facecolor='w', edgecolor='k', sharex=True)
        fig.subplots_adjust(hspace=.5, wspace=.1)
        fig.suptitle('Duration of project computation', fontsize=16)
        axs.bar(ind, time, width, label='time')
        axs.legend()
        axs.set_ylabel('time [s]')
        axs.set_xlabel('loop')

    def plot_gant(self):
        """
            gant plot of basic setup of nets
        """
        fig = plt.figure(figsize=(20, 8))
        ax = fig.add_subplot(111)
        fig.suptitle('Number of results for individual tasks', fontsize=16)

        cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

        for i in range(1, self.params.tasks + 1):
            start_time = 0
            weights = np.arange(0, max(self.place_tokens[f'task{i}_results_counter']))
            print(weights)
            norm = mp.colors.Normalize(vmin=weights.min(), vmax=weights.max())
            cmap = mp.cm.ScalarMappable(norm=norm, cmap=cmaps[i])
            cmap.set_array([])

            for j in range(0, max(self.place_tokens[f'task{i}_results_counter'])):
                idx = max(index for index, item in enumerate(self.place_tokens[f'task{i}_results_counter']) if item == j)
                # idx = np.arange(clients)
                end_time = self.place_time[f'task{i}_results_counter'][idx]
                if start_time > 0:
                    ax.barh(i - 1, end_time - start_time, left=start_time, height=0.3, align='center', alpha=0.8,
                            color=cmap.to_rgba(j))
                else:
                    pass
                start_time = end_time

        ax.axvline(x=self.time_computed[0], color='k', linestyle='-.', label='project computed')
        ax.legend()

        labels = [f'Task {i}' for i in range(1, self.params.tasks + 1)]
        yPos = np.arange(self.params.tasks)
        ax.set_yticks(yPos)
        ax.set_yticklabels(labels)
        ax.set_xlabel('time [s]')
        # ax.set_xlim(xmin = 0, xmax = time_computed + 200)
        # ax.grid(color = 'g', linestyle = ':')

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
    BoincSimulation().main()
