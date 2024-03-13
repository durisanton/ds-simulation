from dataclasses import dataclass
from typing import Dict, List


@dataclass
class NetParams:
    tasks: int
    clients: int
    loops: int
    max_steps: int
    compare_results: int
    stats_loops: int
    # probability and times of transitions for individual clients
    connect_min_time: List
    connect_max_time: List
    pc_initialization_min_time: List
    pc_initialization_max_time: List
    client_running_probability: List
    client_crash_probability: List
    compute_1_min_time: List
    compute_1_max_time: List
    pause_on_probability: List
    pause_off_probability: List
    in_pause_min_time: List
    in_pause_max_time: List
    job_running_probability: List
    job_crash_probability: List
    compute_2_min_time: List
    compute_2_max_time: List
    correct_probability: List
    incorrect_probability: List

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            tasks=data.get('tasks'),
            clients=data.get('clients'),
            loops=data.get('loops'),
            max_steps=data.get('max_steps'),
            compare_results=data.get('compare_results'),
            stats_loops=data.get('stats_loops'),
            connect_min_time=data.get('connect_min_time'),
            connect_max_time=data.get('connect_max_time'),
            pc_initialization_min_time=data.get('pc_initialization_min_time'),
            pc_initialization_max_time=data.get('pc_initialization_max_time'),
            client_running_probability=data.get('client_running_probability'),
            client_crash_probability=data.get('client_crash_probability'),
            compute_1_min_time=data.get('compute_1_min_time'),
            compute_1_max_time=data.get('compute_1_max_time'),
            pause_on_probability=data.get('pause_on_probability'),
            pause_off_probability=data.get('pause_off_probability'),
            in_pause_min_time=data.get('in_pause_min_time'),
            in_pause_max_time=data.get('in_pause_max_time'),
            job_running_probability=data.get('job_running_probability'),
            job_crash_probability=data.get('job_crash_probability'),
            compute_2_min_time=data.get('compute_2_min_time'),
            compute_2_max_time=data.get('compute_2_max_time'),
            correct_probability=data.get('correct_probability'),
            incorrect_probability=data.get('incorrect_probability'),
        )
