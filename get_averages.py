from utils import *


def get_averages(data_list, n):
    """
    """

    cost_sum = 0
    pre_proc_sum = 0
    node_count_sum = 0
    time_sum = 0

    for dataDict in data_list:
        cost_sum += dataDict['cost_sum']
        pre_proc_sum += float(dataDict['pre_processing_time'])
        node_count_sum += dataDict['node_count']
        time_sum += float(dataDict['simulation_time'])

    cost_avg = cost_sum / n
    pre_proc_avg = pre_proc_sum / n
    node_count_avg = node_count_sum / n
    time_avg = time_sum / n

    averages = {
            'cost'      : cost_avg,
            'pre_proc'  : pre_proc_avg,
            'count'     : node_count_avg,
            'time'      : time_avg
        }

    return averages


def get_plot(averages, y_axis):
    from plotly import graph_objs as go
   
    plot_data = {}
    plot_data['x'] = []
    plot_data['y'] = []
    for k, v in sorted(averages.items()):
        plot_data['x'].append(k)
        plot_data['y'].append(v[y_axis])

    return go.Scatter(plot_data)


def make_avg_plots(file_names, x_axis, y_axis):
    """
    Uses JSON data in files given by 'file_names' to average values and write
    them to plots.
    """
    averages = {}
    for file in file_names:
        data = read_json_data(file)
        n = data['num_sims']
        data_list = data['data']
        new_average = get_averages(data_list, n)
        new_average['h_name'] = data['h_name']
        new_average['algorithm'] = data['algorithm']
        
        averages[data[x_axis]] = new_average

    return get_plot(averages, y_axis)


def make_all_the_plots(all_files):
    """
    Change and add dictionaries and their regex expressions to add
    files to average plots.
    """
    from plotly import offline as py
    import re
    
    plots = []
    plot_types = []
    m_v_pre_proc = {
            'x':    'm',
            'y':    'pre_proc',
            'reg':  'sims10\.n2\.k5\.m[0-9]+\.sum\.State\.a_star\.json'
            }
    plot_types.append(m_v_pre_proc)
    n_v_time = {
            'x':    'n',
            'y':    'time',
            'reg':  'sims10\.n([0-9]+)\.k\1\.m10\.sum\.State\.a_star\.json'
            }
    plot_types.append(n_v_time)
    k_v_time = {
            'x':    'k',
            'y':    'time',
            'reg':  'sims10\.n2\.k[0-9]+\.m30\.sum\.State\.a_star\.json'
            }
    plot_types.append(k_v_time)
    n_v_count = {
            'x':    'n',
            'y':    'count',
            'reg':  'sims10\.n[0-9]+\.k2\.m10\.sum\.State\.a_star\.json'
            }
    plot_types.append(n_v_count)
    k_v_count = {
            'x':    'k',
            'y':    'count',
            'reg':  'sims10\.n1\.k[0-9]+\.m10\.sum\.State\.a_star\.json'
            }
    plot_types.append(k_v_count)

    for params in plot_types:
        # Here, match simulation of constant n, k, and varying m 
        p = re.compile(params['reg'])
        matching_files = [ x for x in all_files if p.search(x) is not None ]
        print(matching_files)
        if matching_files:
            plots.append(
                    make_avg_plots(matching_files, params['x'], params['y']))
    
    py.plot(plots)
    

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        eprint("usage:", sys.argv[0], "<json-file_name> ...")
        eprint("  Makes plots from the average values calculated for" + 
                " pre-processing time, the number of nodes expanded," + 
                " total costs, simulation times, etc.")
        sys.exit(1)
    else: 
        make_all_the_plots(sys.argv[1:])

