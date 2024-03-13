from typing import List, Union

from petnetsim import Place, TransitionTimed, TransitionStochastic, Transition, Arc, uniform_distribution


class Constants:
    places: List[Place] = [Place(name='waiting'),
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
    transitions: List[Union[TransitionTimed, TransitionStochastic, Transition]] = [
        # for creating new result
        Transition(name='create'),
        Transition(name='merge'),
        Transition('running'),
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
    input_arcs: List[Arc] = [
        Arc('waiting', 'connect'),
        Arc('ready', 'pc_initialization'),
        Arc('init_crash_decision', 'client_running'),
        Arc('init_crash_decision', 'client_crash'),
        Arc('running_1', 'compute_1'),
        Arc('pause_decision', 'pause_off'),
        Arc('pause_decision', 'pause_on'),
        Arc('no_pause', 'running'),
        Arc('pause', 'in_pause'),
        Arc('crash_decision', 'job_running'),
        Arc('crash_decision', 'job_crash'),
        Arc('running_2', 'compute_2'),
        Arc('result_decision', 'correct'),
        Arc('result_decision', 'incorrect'),
        Arc('new_result', 'create'),
        Arc('correct_result', 'merge')
    ]

    # define transition output arcs
    output_arcs: List[Arc] = [
        Arc('connect', 'ready'),
        Arc('pc_initialization', 'init_crash_decision'),
        Arc('client_running', 'running_1'),
        Arc('client_crash', 'new_result'),
        Arc('compute_1', 'pause_decision'),
        Arc('pause_off', 'no_pause'),
        Arc('pause_on', 'pause'),
        Arc('running', 'crash_decision'),
        Arc('in_pause', 'crash_decision'),
        Arc('job_running', 'running_2'),
        Arc('job_crash', 'new_result'),
        Arc('compute_2', 'result_decision'),
        Arc('correct', 'correct_result'),
        Arc('incorrect', 'incorrect_result'),
        Arc('create', 'ready')]
