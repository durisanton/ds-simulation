# DS simulation
This project provides simulation of distributed systems using Petri nets.


Two models are implemented: 
* large grid computing system, more precisely the BOINC platform with the Folding@home
* horizontally scaled web application divided into several services with a distributed database
project


**Still in progress, only backend is done.**

## Usage
### For grid computing system:

1. #### endpoints:
   * [GET] fah/deadline - plot user pause simulation for different transition probabilities (pause_on_probability, pause_off_probability)
   * [GET] fah/pause-deadline - plot subtask deadline simulation for different probabilities (job_running_probability, job_crash_probability)
   * [GET] fah/gant - plot simulation for default settings
   * [GET] fah/params - show current parameters
   * [POST] fah/change-params - change parameters based on provided JSON 
   * [GET] fah/stats - plot statistics

2. #### parameters example
    These are the default settings for Petri net. The _min_time_ and _probability_ lists provides settings for each client, 
    so must have as many items as _clients_ number.  

           {
           "tasks" : 2,
           "clients" : 5,
           "loops" : 10,
           "max_steps" : 50000,
           "compare_results" : 2,
           "stats_loops" : 10,
           "connect_min_time" : [1, 1, 1, 1, 1],
           "connect_max_time" : [100, 100, 100, 100, 100],
           "pc_initialization_min_time" : [0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
           "pc_initialization_max_time" : [1, 1, 1, 1, 1],
           "client_running_probability" : [0.9, 0.9, 0.9, 0.9, 0.9],
           "client_crash_probability" : [0.1, 0.1, 0.1, 0.1, 0.1],
           "compute_1_min_time" : [100, 100, 100, 100, 100],
           "compute_1_max_time" : [1000, 1000, 1000, 1000, 1000],
           "pause_on_probability" : [1, 1, 1, 1, 1],
           "pause_off_probability" : [0, 0, 0, 0, 0],
           "in_pause_min_time" : [100, 100, 100, 100, 100],
           "in_pause_max_time" : [200, 200, 200, 200, 200],
           "job_running_probability" : [0.9, 0.9, 0.9, 0.9, 0.9],
           "job_crash_probability" : [0.1, 0.1, 0.1, 0.1, 0.1],
           "compute_2_min_time" : [200, 200, 200, 200, 200],
           "compute_2_max_time" : [1000, 1000, 1000, 1000, 1000],
           "correct_probability" : [0.85, 0.85, 0.85, 0.85, 0.85],
           "incorrect_probability" : [0.15, 0.15, 0.15, 0.15, 0.15]
           }