from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class NetParams:
    tasks: int
    clients: int
    loops: int
    max_steps: int
    compare_results: int
    stats_loops: int
    # probability and times of transitions for individual clients
    connect_min_time: list
    connect_max_time: list
    pc_initialization_min_time: list
    pc_initialization_max_time: list
    client_running_probability: list
    client_crash_probability: list
    compute_1_min_time: list
    compute_1_max_time: list
    pause_on_probability: list
    pause_off_probability: list
    in_pause_min_time: list
    in_pause_max_time: list
    job_running_probability: list
    job_crash_probability: list
    compute_2_min_time: list
    compute_2_max_time: list
    correct_probability: list
    incorrect_probability: list
