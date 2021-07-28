from petnetsim.petnetsim import *
import matplotlib.pyplot as plt
import matplotlib as mp
import statistics
import numpy as np

def make_net(connect_min_time, connect_max_time,pc_initialization_min_time, pc_initialization_max_time, client_running_probability, client_crash_probability, compute_1_max_time, compute_1_min_time, pause_on_probability, pause_off_probability, in_pause_max_time, in_pause_min_time, job_running_probability, job_crash_probability, compute_2_max_time, compute_2_min_time, correct_probability, incorrect_probability):
    global boinc_net

    ## CLIENT NET
    # define places for client net
    places = [Place('waiting'),
              Place('ready'),
              Place('init_crash_decision'),
              Place('running_1'),
              Place('pause_decision'),
              Place('no_pause'),
              Place('pause'),
              Place('crash_decision'),
              Place('running_2'),
              Place('result_decision'),
              Place('correct_result'),
              Place('incorrect_result'),
              Place('new_result')]
    
    # define transitions; stochastic and timed transitions moved to loop
    transitions = [# fo simulating different time of klient connection 
                   TransitionTimed('connect',0,0,uniform_distribution),
                   # for simulating client setup; downloading task, etc
                   TransitionTimed('pc_initialization',0,0,uniform_distribution),
                   # for crash decision
                   TransitionStochastic('client_running',0),
                   TransitionStochastic('client_crash',0),
                   # for simulating computation
                   TransitionTimed('compute_1',0,0,uniform_distribution),
                   # for pause decision
                   TransitionStochastic('pause_off',0),
                   TransitionStochastic('pause_on',0),
                   Transition('running'),
                   TransitionTimed('in_pause',0,0,uniform_distribution),
                   #for crash decision
                   TransitionStochastic('job_running',0),
                   TransitionStochastic('job_crash',0),
                   #for simulating computation 
                   TransitionTimed('compute_2',0,0,uniform_distribution),
                   # for result decision
                   TransitionStochastic('correct',0),
                   TransitionStochastic('incorrect',0),
                   # for creating new result
                   Transition('create'),
                   Transition('merge')]
   
    # define transition input arcs
    input_arcs = [('waiting','connect'),
                  ('ready','pc_initialization'),
                  ('init_crash_decision','client_running'),
                  ('init_crash_decision','client_crash'),
                  ('running_1','compute_1'),
                  ('pause_decision','pause_off'),
                  ('pause_decision','pause_on'),
                  ('no_pause','running'),
                  ('pause','in_pause'),
                  ('crash_decision','job_running'),
                  ('crash_decision','job_crash'),
                  ('running_2','compute_2'),
                  ('result_decision','correct'),
                  ('result_decision','incorrect'),
                  ('new_result','create'),
                  ('correct_result', 'merge')]

    #define transition output arcs
    output_arcs = [('connect','ready'),
                   ('pc_initialization','init_crash_decision'),
                   ('client_running','running_1'),
                   ('client_crash','new_result'),
                   ('compute_1','pause_decision'),
                   ('pause_off','no_pause'),
                   ('pause_on','pause'),
                   ('running','crash_decision'),
                   ('in_pause','crash_decision'),
                   ('job_running','running_2'),
                   ('job_crash','new_result'),
                   ('compute_2','result_decision'),
                   ('correct','correct_result'),
                   ('incorrect','incorrect_result'),
                   ('create','ready')]
    
    # join arcs
    arcs = input_arcs + output_arcs
    
    # making client net
    client_net = PetriNet(places,transitions,arcs)

    ## TASK DISTRIBUTION NET
    # some stuff for cloning client net; transition 'task_distribution' is a statring place for all cloned nets; place 'results' is merging point for all client results
    client_places = [Place('results'), Place('results_counter')]
    client_transitions = [Transition('distribution')]
    client_arcs = []
   
    # cloning clients
    for client_i in range(1, clients + 1):  
        # filling probability and time data to transitions
        for tr in client_net.transitions:
            if tr.name == 'connect':
                tr.t_min = connect_min_time[client_i - 1]
                tr.t_max = connect_max_time[client_i - 1]
            if tr.name == 'pc_initialization':
                tr.t_min = pc_initialization_min_time[client_i - 1]
                tr.t_max = pc_initialization_max_time[client_i - 1]
            if tr.name == 'client_running':
                tr.probability = client_running_probability[client_i -1]
            if tr.name == 'client_crash':
                tr.probability = client_crash_probability[client_i - 1]
            if tr.name == 'compute_1':
                tr.t_min = compute_1_min_time[client_i - 1]
                tr.t_max = compute_1_max_time[client_i - 1]
            if tr.name == 'pause_off':
                tr.probability = pause_off_probability[client_i - 1]
            if tr.name == 'pause_on':
                tr.probability = pause_on_probability[client_i -1]
            if tr.name == 'in_pause':
                tr.t_min = in_pause_min_time[client_i - 1]
                tr.t_max = in_pause_max_time[client_i - 1]
            if tr.name == 'job_running':
                tr.probability = job_running_probability[client_i - 1]
            if tr.name == 'job_crash':
                tr.probability = job_crash_probability[client_i - 1]
            if tr.name == 'compute_2':
                tr.t_min = compute_2_min_time[client_i - 1]
                tr.t_max = compute_2_max_time[client_i - 1]
            if tr.name == 'correct':
                tr.probability = correct_probability[client_i - 1]
            if tr.name == 'incorrect':
                tr.probability = incorrect_probability[client_i - 1]

        prefix = f'client{client_i}_'
        client_net.clone(prefix, client_places, client_transitions, client_arcs)
        client_arcs.append(('distribution', prefix + 'waiting'))
        client_arcs.append((prefix + 'merge', 'results'))
        client_arcs.append((prefix + 'merge', 'results_counter'))

        
    # making task distribution net
    task_net = PetriNet(client_places, client_transitions, client_arcs)

    ## TASK NET
    # some stuff for cloning; place 'project' is a starting place for each task; place 'project_computed' is merging point for all task results
    task_places = [Place('project', 1), Place('project_computed')]
    task_transitions = [Transition('make_tasks'), Transition('merge_tasks')]
    task_arcs = [('project', 'make_tasks'), ('merge_tasks','project_computed')]
    
    # cloning job tasks
    for task_i in range(1, tasks + 1):
        prefix = f'task{task_i}_'
        task_net.clone(prefix, task_places, task_transitions, task_arcs)
        task_places.append(Place('task' + f'{task_i}'))
        task_arcs.append(('task' + f'{task_i}', prefix + 'distribution')) 
        task_arcs.append(('make_tasks', 'task' + f'{task_i}'))
        task_arcs.append(Arc(prefix + 'results', 'merge_tasks', n_tokens = compare_results))
   
    #petri net of whole boinc project
    boinc_net = PetriNet(task_places, task_transitions, task_arcs)

# one run of simulation 
def run():
    #init variables
    global place_tokens
    global place_time  
    global time_computed
    time_computed = [] 
    
    #making empty dictionaries of tokens and time in every places
    place_tokens = dict()
    place_time = dict()
    for p in boinc_net.places:
            place_tokens[p.name] = []
            place_time[p.name] = []
    #main loop
    while not boinc_net.ended and boinc_net.step_num < max_steps: 
        boinc_net.step()        
        #filling dictionaries
        for p in boinc_net.places:
            place_tokens[p.name].append(p.tokens)
            place_time[p.name].append(boinc_net.time)
            if p.name == 'project_computed' and p.tokens == 1:
                time_computed.append(boinc_net.time)

# more runs of simulation, data are saved in stats
def loop_run(connect_min_time, connect_max_time, pc_initialization_min_time, pc_initialization_max_time, client_running_probability, client_crash_probability, compute_1_max_time, compute_1_min_time, pause_on_probability, pause_off_probability, in_pause_max_time, in_pause_min_time, job_running_probability, job_crash_probability, compute_2_max_time, compute_2_min_time, correct_probability, incorrect_probability):
    # defining variables
    global stats
    global time
    stats = dict()
    time = {}
    
    ## used for simulating pause statistics; uncomment for this kind of simulation
    #in_pause_min_time = np.array(in_pause_min_time) * 10   #for better visualization
    #in_pause_max_time = np.array(in_pause_max_time) * 10
    
    # initial setup for deadline simulation
    #job_running_probability = [1, 1, 1, 1, 1]
    #job_crash_probability = [0, 0, 0, 0, 0]

    
    # loop for make some statistics data
    for i in range(0, stats_loops):
        time[i] = []
        # make new net with changed probabilities
        make_net(connect_min_time, connect_max_time, pc_initialization_min_time, pc_initialization_max_time, client_running_probability, client_crash_probability, compute_1_max_time, compute_1_min_time, pause_on_probability, pause_off_probability, in_pause_max_time, in_pause_min_time, job_running_probability, job_crash_probability, compute_2_max_time, compute_2_min_time, correct_probability, incorrect_probability)

        # loop run and filling stats for each loop
        for loop in range(1,loops + 1):
            boinc_net.reset()
            stats[f'loop_{loop}'] = dict()
      
            while not boinc_net.ended and boinc_net.step_num < max_steps:
                boinc_net.step()
   
            for p in boinc_net.places:
                stats[(f'loop_{loop}')][f'{p.name}'] = []            
                stats[(f'loop_{loop}')][f'{p.name}'].append(p.tokens)

            time[i].append(boinc_net.time)
        
        ## change probability of pause in each loop; uncomment for this simulation
        #pause_on_probability = np.array(pause_on_probability) - 0.1
        #pause_off_probability = np.array(pause_off_probability) + 0.1 
    
        ## change probability of "project deadline"; uncomment for this simulation 
        #job_running_probability = np.array(job_running_probability) - 0.1 
        #job_crash_probability = np.array(job_crash_probability) + 0.1
        
        ## change computation time for "project deadline" simulation
        compute_1_max_time = np.array(compute_1_max_time) + 100
        compute_2_max_time = np.array(compute_2_max_time) + 100

# for plotting deadline stats
def plot_deadline():
    mean  = []
    std = [] 
    for i in range(0, stats_loops):
        mean.append(statistics.mean(time[i]))
        std.append(statistics.stdev(time[i]))

    ind = np.arange(stats_loops)
    width = 0.1
    # plot requests for each microservice
    fig, axs = plt.subplots(1, 1, facecolor='w', edgecolor='k', sharex=True)
    fig.subplots_adjust(hspace = .5, wspace=.1)
    fig.suptitle('Duration of project computation', fontsize=16)
    axs.bar(ind, mean, width, yerr=np.array(std),  label = ('time'))
    axs.axhline(y = 2500, color='k', linestyle='--', label =('deadline'))
    axs.legend(fontsize=16)
    axs.set_ylabel('time [s]', fontsize=16)

    labels = [1000,1100,1200,1300,1400,1500,1600,1700,1800,1900]
 
    axs.set_xticks(ind)
    axs.set_xticklabels(labels,fontsize=16)
    axs.set_xlabel('computation time [s]', fontsize=16)

    axs.grid(axis='y')

# plot deadline; job pause method
def plot_pause_deadline():
    mean  = []
    std = [] 
    for i in range(0, stats_loops):
        mean.append(statistics.mean(time[i]))
        std.append(statistics.stdev(time[i]))

    ind = np.arange(stats_loops)
    print(mean)
    width = 0.1
    # plot requests for each microservice
    fig, axs = plt.subplots(1, 1, facecolor='w', edgecolor='k', sharex=True)
    fig.subplots_adjust(hspace = .5, wspace=.1)
    fig.suptitle('Duration of project computation', fontsize=16)
    axs.bar(ind, mean, width, yerr=np.array(std),  label = ('time'))
    axs.legend(fontsize=16)
    axs.set_ylabel('time [s]', fontsize=16)

    labels = [100,90,80,70,60,50,40,30,20,10]
 
    axs.set_xticks(ind)
    axs.set_xticklabels(labels,fontsize=16)
    axs.set_xlabel('probability [%]', fontsize=16)

    axs.grid(axis='y')

def plot_stats():
    ind = np.arange(loops)
    time = []
    for loop in range(1, loops + 1):
        time.append(stats[(f'loop_{loop}')]['time'])
    width = 0.1
    # plot requests for each microservice
    fig, axs = plt.subplots(1, 1, facecolor='w', edgecolor='k', sharex=True)
    fig.subplots_adjust(hspace = .5, wspace=.1)
    fig.suptitle('Duration of project computation', fontsize=16)
    axs.bar(ind, time, width, label = ('time'))
    axs.legend()
    axs.set_ylabel('time [s]')
    axs.set_xlabel('loop')

# gant plot of basic setup of net
def plot_gant():
    fig = plt.figure(figsize=(20,8))
    ax = fig.add_subplot(111)
    fig.suptitle('Number of results for individual tasks', fontsize=16) 
    
    cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'] 

    for i in range(1, tasks + 1):
        start_time =  0
        weights = np.arange(0,max(place_tokens[(f'task{i}_results_counter')]))
        print(weights)
        norm = mp.colors.Normalize(vmin=weights.min(), vmax=weights.max())
        cmap = mp.cm.ScalarMappable(norm=norm, cmap = cmaps[i])
        cmap.set_array([])
        
        for j in range(0, max(place_tokens[(f'task{i}_results_counter')])):
            idx = max(index for index, item in enumerate(place_tokens[(f'task{i}_results_counter')]) if item == j)
            #idx = np.arange(clients)
            end_time = place_time[(f'task{i}_results_counter')][idx]
            if start_time > 0:
                ax.barh( i - 1 , end_time - start_time, left=start_time, height=0.3, align='center', alpha = 0.8, color = cmap.to_rgba(j))
            else: 
                pass
            start_time = end_time
    
    ax.axvline(x = time_computed[0], color='k', linestyle='-.', label = 'project computed')
    ax.legend()

    labels = [(f'Task {i}') for i in range(1, tasks + 1)]
    yPos = np.arange(tasks)
    ax.set_yticks(yPos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('time [s]')
    #ax.set_xlim(xmin = 0, xmax = time_computed + 200)
    #ax.grid(color = 'g', linestyle = ':')

def basic_info():
    print('CONFLICT GROUPS')
    print(boinc_net.conflict_groups_str)
    print('------------------------------------')
    boinc_net.reset()
    print('INITIAL TOKENS:')
    boinc_net.print_places()
    print('------------------------------------')
    print('TRANSITIONS STATS:')
    for t in boinc_net.transitions:
        print(t.name, t.fired_times, sep=': ')
    print('------------------------------------')
    print('PLACES STATS:')
    boinc_net.print_places()

def main():
    # init variables
    globals()['tasks'] = 2
    globals()['clients'] = 5
    globals()['loops'] = 10
    globals()['max_steps'] = 50000
    globals()['compare_results'] = 2
    globals()['stats_loops'] = 10 

    # probability and times of transitions for individual clients
    connect_min_time =  [1, 1, 1, 1, 1]
    connect_max_time = [100, 100, 100, 100, 100]
    pc_initialization_min_time = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001]
    pc_initialization_max_time = [1, 1, 1, 1, 1]
    client_running_probability = [0.9, 0.9, 0.9, 0.9, 0.9]
    client_crash_probability = [0.1, 0.1, 0.1, 0.1, 0.1]
    compute_1_min_time = [100, 100, 100, 100, 100]
    compute_1_max_time = [1000, 1000, 1000, 1000, 1000]
    pause_on_probability = [1, 1, 1, 1, 1]
    pause_off_probability = [0, 0, 0, 0, 0]
    in_pause_min_time = [100, 100, 100, 100, 100]
    in_pause_max_time = [200, 200, 200, 200, 200]
    job_running_probability = [0.9, 0.9, 0.9, 0.9, 0.9]
    job_crash_probability = [0.1, 0.1, 0.1, 0.1, 0.1]
    compute_2_min_time = [200, 200, 200, 200, 200]
    compute_2_max_time = [1000, 1000, 1000, 1000, 1000]
    correct_probability = [0.85, 0.85, 0.85, 0.85, 0.85]
    incorrect_probability = [0.15, 0.15, 0.15, 0.15, 0.15]
 
    make_net(connect_min_time, connect_max_time, pc_initialization_min_time, pc_initialization_max_time, client_running_probability, client_crash_probability, compute_1_max_time, compute_1_min_time, pause_on_probability, pause_off_probability, in_pause_max_time, in_pause_min_time, job_running_probability, job_crash_probability, compute_2_max_time, compute_2_min_time, correct_probability, incorrect_probability)

    run()
    loop_run(connect_min_time, connect_max_time, pc_initialization_min_time, pc_initialization_max_time, client_running_probability, client_crash_probability, compute_1_max_time, compute_1_min_time, pause_on_probability, pause_off_probability, in_pause_max_time, in_pause_min_time, job_running_probability, job_crash_probability, compute_2_max_time, compute_2_min_time, correct_probability, incorrect_probability)
    
    ## uncomment for simulation
    #plot_results()
    #plot_pause_deadline()
    plot_deadline()
    #plot_gant()
    
    plt.show() 

if __name__ == '__main__':
    main()

