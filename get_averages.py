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
    from plotly import offline as py
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
    """
    import re
    plots = []
    # This is for varying m + preproc
    # get all the files with varying  and static everyting else
    # pass them to plots blah blah blah and 
    # along with y-axis (pre_proc)
    p = re.compile('sims10\.n2\.k5\.m[0-9]+\..+\.json')
    pre_proc_v_m = [ x for x in all_files if p.search(x) is not None ]
    plots.append(make_avg_plots(pre_proc_v_m, 'm', 'pre_proc'))
    """
    p = re.compile('sims')
    time_v_n = [ x for x in all_files if p.search(x) is not None ]
    print(time_v_n)
    plots.append(make_avg_plots(time_v_n, 'n', 'time'))

    p = re.compile('50')
    time_v_k = [ x for x in all_files if p.search(x) is not None ]
    print(time_v_k)
    plots.append(make_avg_plots(time_v_k, 'k', 'time'))

    p = re.compile('50')
    nodes_v_n = [ x for x in all_files if p.search(x) is not None ]
    print(time_v_k)
    plots.append(make_avg_plots(time_v_k, 'n', 'count'))

    p = re.compile('50')
    nodes_v_k = [ x for x in all_files if p.search(x) is not None ]
    print(time_v_k)
    plots.append(make_avg_plots(time_v_k, 'k', 'count'))
    """

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

