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
    preprocessing = go.Scatter(plot_data["preprocessing_time"])
    simulation = go.Scatter(plot_data["simulation_time"])
    nodes = go.Scatter(plot_data["node_count"])

    to_plot = tools.make_subplots(rows=3, cols=2,
                                  specs=[[{'colspan': 2}, None], [{}, {}],
                                         [{'colspan': 2}, None]],
                                  subplot_titles=(
                                      'Total Path Cost', 'Preprocessing Time',
                                      'Simulation Time',
                                      'Total Nodes Expanded'))
    to_plot.append_trace(cost, 1, 1)
    to_plot.append_trace(preprocessing, 2, 1)
    to_plot.append_trace(simulation, 2, 2)
    to_plot.append_trace(nodes, 3, 1)

    py.plot(to_plot, filename=path, auto_open=False)
