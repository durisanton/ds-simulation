from typing import Union

from petnetsim import Place, TransitionTimed, TransitionStochastic, Transition, Arc, uniform_distribution


class Constants:
    places: list[Place] = [Place(name='waiting'),
                           Place(name='ready'),
                           Place(name='init_crash_decision'),
                           Place(name='running_1'),
                           Place(name='pause_decision'),
                           Place(name='no_pause'),
                           Place(name='pause'),
                           Place(name='crash_decision'),
                           Place(name='running_2'),
                           Place(name='result_decision'),
                           Place(name='correct_result'),
                           Place(name='incorrect_result'),
                           Place(name='new_result')]

    # define transitions; stochastic and timed transitions moved to loop
    transitions: list[Union[TransitionTimed, TransitionStochastic, Transition]] = [
        # for creating new result
        Transition(name='create'),
        Transition(name='merge'),
        Transition(name='running'),
        # for crash decision
        TransitionStochastic(name='client_running', probability=0),
        TransitionStochastic(name='client_crash', probability=0),
        # for pause decision
        TransitionStochastic(name='pause_off', probability=0),
        TransitionStochastic(name='pause_on', probability=0),
        # for crash decision
        TransitionStochastic(name='job_running', probability=0),
        TransitionStochastic(name='job_crash', probability=0),
        # for result decision
        TransitionStochastic(name='correct', probability=0),
        TransitionStochastic(name='incorrect', probability=0),
        # for simulating different time of client connection
        TransitionTimed(name='connect', t_min=0, t_max=0, p_distribution_func=uniform_distribution),
        # for simulating client setup; downloading task, etc
        TransitionTimed(name='pc_initialization', t_min=0, t_max=0, p_distribution_func=uniform_distribution),
        # for simulating computation
        TransitionTimed(name='compute_1', t_min=0, t_max=0, p_distribution_func=uniform_distribution),
        TransitionTimed(name='compute_2', t_min=0, t_max=0, p_distribution_func=uniform_distribution),
        TransitionTimed(name='in_pause', t_min=0, t_max=0, p_distribution_func=uniform_distribution)
    ]

    # define transition input arcs
    input_arcs: list[Arc] = [
        Arc(source='waiting', target='connect'),
        Arc(source='ready', target='pc_initialization'),
        Arc(source='init_crash_decision', target='client_running'),
        Arc(source='init_crash_decision', target='client_crash'),
        Arc(source='running_1', target='compute_1'),
        Arc(source='pause_decision', target='pause_off'),
        Arc(source='pause_decision', target='pause_on'),
        Arc(source='no_pause', target='running'),
        Arc(source='pause', target='in_pause'),
        Arc(source='crash_decision', target='job_running'),
        Arc(source='crash_decision', target='job_crash'),
        Arc(source='running_2', target='compute_2'),
        Arc(source='result_decision', target='correct'),
        Arc(source='result_decision', target='incorrect'),
        Arc(source='new_result', target='create'),
        Arc(source='correct_result', target='merge')
    ]

    # define transition output arcs
    output_arcs: list[Arc] = [
        Arc(source='connect', target='ready'),
        Arc(source='pc_initialization', target='init_crash_decision'),
        Arc(source='client_running', target='running_1'),
        Arc(source='client_crash', target='new_result'),
        Arc(source='compute_1', target='pause_decision'),
        Arc(source='pause_off', target='no_pause'),
        Arc(source='pause_on', target='pause'),
        Arc(source='running', target='crash_decision'),
        Arc(source='in_pause', target='crash_decision'),
        Arc(source='job_running', target='running_2'),
        Arc(source='job_crash', target='new_result'),
        Arc(source='compute_2', target='result_decision'),
        Arc(source='correct', target='correct_result'),
        Arc(source='incorrect', target='incorrect_result'),
        Arc(source='create', target='ready')]

    deadline_plot_labels: list[str] = ['1000', '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900']
    pause_plot_labels: list[str] = ['100', '90', '80', '70', '60', '50', '40', '30', '20', '10']

    cmaps: list[str] = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
