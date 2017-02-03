def permutations(n, r):
    """
    Returns a generator of all r-permutations of the numbers 0 to n-1.
    """
    return permutations_list(range(n), r)


def permutations_list(numbers, r):
    """
    Returns a generator of all r-permutations of the given list of numbers.
    If numbers are not unique, this function will give the wrong result.
    """
    if r == 0:
        yield []
    else:
        for num in numbers:
            remaining_numbers = [i for i in numbers if i != num]
            for perm in permutations_list(remaining_numbers, r - 1):
                ret = [num]
                ret.extend(perm)
                yield ret


def permutations_exclude(n, r, exclude=None):
    """
    Returns a generator of all r-combinations of the numbers 0 to n-1,
    excluding any number i for which exclude[i] is True.
    """
    if exclude is None:
        numbers = list(range(n))
    else:
        numbers = [i for i in range(n) if not exclude[i]]
    return permutations_list(numbers, r)


def combinations(n, r):
    """
    Returns a generator of all r-combinations of the numbers 0 to n-1.
    """
    return combinations_list(range(n), r)


def combinations_list(numbers, r):
    """
    Returns a generator of all r-combinations of the given list of numbers.
    If numbers are not unique, this function will give the wrong result.
    """
    if r == 0:
        yield []
    else:
        for num in numbers:
            remaining_numbers = [numbers[i] for i in
                                 range(numbers.index(num) + 1, len(numbers))]
            for comb in combinations_list(remaining_numbers, r - 1):
                ret = [num]
                ret.extend(comb)
                yield ret


def filter_pairs(pairs):
    """
    Returns a list of every source-destination pair in 'pairs' where the source
    is not the same as the destination.

    :param pairs: a list of source-destination pairs for packages
    :type pairs: list((int, int))
    :rtype: list((int, int))
    """
    return [(src, dest) for src, dest in pairs if src != dest]


def eprint(*args, **kwargs):
    """
    Prints to standard error instead of standard output.

    :param args: arguments for print()
    :param kwargs: keyword arguments for print()
    """
    import sys

    print(*args, file=sys.stderr, **kwargs)


def output_bar_multiple(path, data_list):
    """
    Writes bar plots of the given data to the file corresponding to the given
    path.

    :param path: the file path
    :param data_list: the data to plot; data_list should be a list of data
        dictionaries; each data dictionary should have two keys, 'algorithm'
        and 'data'; the value of 'algorithm' should be the name of the
        algorithm used (string); the value of 'data' is a list of dictionaries,
        where each dictionary includes key-value pairs for the types of graph
        you want (pre_processing_time, cost_sum, simulation_time, and
        node_count)
    """
    from plotly import offline as py
    from plotly import graph_objs as go
    cost = []
    pre_processing = []
    simulation = []
    nodes = []
    for dataDict in data_list:
        print(dataDict)
        data = dataDict["data"]
        plot_data = {}
        for key in data[0].keys():
            plot_data[key] = {
                'x': [],
                'y': [],
                # 'mode': 'lines+markers',
                'name': dataDict["algorithm"]
            }
        for i, d in enumerate(data):
            for k, v in d.items():
                plot_data[k]['x'].append(i)
                plot_data[k]['y'].append(v)
        cost.append(go.Bar(plot_data["cost_sum"]))
        pre_processing.append(go.Bar(plot_data["pre_processing_time"]))
        simulation.append(go.Bar(plot_data["simulation_time"]))
        nodes.append(go.Bar(plot_data["node_count"]))

    layout = dict(title='Cost path',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='Cost'),
                  barmode='group')
    fig = dict(data=cost, layout=layout)
    py.plot(fig, filename="cost." + path)

    layout = dict(title='Pre Processing time',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='time'),
                  barmode='group')
    fig = dict(data=pre_processing, layout=layout)
    py.plot(fig, filename="processing.time.." + path)

    layout = dict(title='Simulation time',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='time'),
                  barmode='group')
    fig = dict(data=simulation, layout=layout)
    py.plot(fig, filename="simulation.time" + path)

    layout = dict(title='Node count',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='number'),
                  barmode='group')
    fig = dict(data=nodes, layout=layout)
    py.plot(fig, filename="node.count" + path)


def output_plot_multiple(path, data_list):
    """
    Writes plots of the given data to the file corresponding to the given path.

    :param path: the file path
    :param data_list: the data to plot; data_list should be a list of data
        dictionaries; each data dictionary should have two keys, 'algorithm'
        and 'data'; the value of 'algorithm' should be the name of the
        algorithm used (string); the value of 'data' is a list of dictionaries,
        where each dictionary includes key-value pairs for the types of graph
        you want (pre_processing_time, cost_sum, simulation_time, and
        node_count)
    """
    from plotly import offline as py
    from plotly import graph_objs as go
    cost = []
    pre_processing = []
    simulation = []
    nodes = []
    for dataDict in data_list:
        data = dataDict["data"]
        plot_data = {}
        for key in data[0].keys():
            plot_data[key] = {
                'x': [],
                'y': [],
                'mode': 'lines+markers',
                'name': dataDict["algorithm"]
            }
        for i, d in enumerate(data):
            for k, v in d.items():
                plot_data[k]['x'].append(i)
                plot_data[k]['y'].append(v)
        cost.append(go.Scatter(plot_data["cost_sum"]))
        pre_processing.append(go.Scatter(plot_data["pre_processing_time"]))
        simulation.append(go.Scatter(plot_data["simulation_time"]))
        nodes.append(go.Scatter(plot_data["node_count"]))
    layout = dict(title='Cost path',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='Cost'))
    fig = dict(data=cost, layout=layout)
    py.plot(fig, filename="C" + path)

    layout = dict(title='Pre Processing time',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='time'))
    fig = dict(data=pre_processing, layout=layout)
    py.plot(fig, filename="P" + path)

    layout = dict(title='Simulation time',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='time'))
    fig = dict(data=simulation, layout=layout)
    py.plot(fig, filename="S" + path)

    layout = dict(title='Node count',
                  xaxis=dict(title='Graph number'),
                  yaxis=dict(title='number'))
    fig = dict(data=nodes, layout=layout)
    py.plot(fig, filename="N" + path)

    # py.plot(to_plot, filename=path, auto_open=False)


def output_plot(path, data):
    """
    Writes plots of the given data in the file corresponding to the given path.

    :param path: the file path
    :param data: the data to plot
    """
    from plotly import offline as py
    from plotly import graph_objs as go
    from plotly import tools

    plot_data = {}
    for key in data[0].keys():
        plot_data[key] = {
            'x': [],
            'y': [],
            'mode': 'lines+markers',
            'name': key
        }

    for i, d in enumerate(data):
        for k, v in d.items():
            plot_data[k]['x'].append(i)
            plot_data[k]['y'].append(v)

            #     to_plot = []
            #     for k in sorted(plot_data.keys()):
            #         to_plot.append(go.Scatter(plot_data[k]))

    cost = go.Scatter(plot_data["cost_sum"])
    pre_processing = go.Scatter(plot_data["pre_processing_time"])
    simulation = go.Scatter(plot_data["simulation_time"])
    nodes = go.Scatter(plot_data["node_count"])

    to_plot = tools.make_subplots(rows=3, cols=2,
                                  specs=[[{'colspan': 2}, None], [{}, {}],
                                         [{'colspan': 2}, None]],
                                  subplot_titles=(
                                      'Total Path Cost', 'Pre-processing Time',
                                      'Simulation Time',
                                      'Total Nodes Expanded'))
    to_plot.append_trace(cost, 1, 1)
    to_plot.append_trace(pre_processing, 2, 1)
    to_plot.append_trace(simulation, 2, 2)
    to_plot.append_trace(nodes, 3, 1)

    py.plot(to_plot, filename=path, auto_open=False)


def dump_json_data(name, data):
    """
    Writes the given data to the given file in JSON.

    :param name: the name of the file (".json" will be added as an extension)
    :param data: the data to write
    """
    import json
    file_name = name + ".json"
    with open(file_name, 'w+') as out:
        json.dump(data, out, indent=4)


def read_json_data(name):
    """
    Reads data in JSON from the given file, and returns the resulting data.

    :param name: the name of the JSON file
    :rtype: data
    """
    import json
    with open(name) as data_file:
        data = json.load(data_file)
        if data is None:
            raise FileNotFoundError("File " + str(name) + " was not found.")
        return data


def plot_results(name, data):
    """
    Writes plots of the given data to the given file in HTML.

    :param name: the name of the file (".html" will be added as an extension)
    :param data: the data to write
    """
    plot_name = name + ".html"
    output_plot(plot_name, data)
