import sys

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
            remaining = range(numbers.index(num) + 1, len(numbers))
            remaining_numbers = [numbers[i] for i in remaining]
            for comb in combinations_list(remaining_numbers, r - 1):
                ret = [num]
                ret.extend(comb)
                yield ret


def filter_pairs(pairs):
    valid_pairs = []
    for sd in pairs:
        if sd[0] != sd[1]:
            valid_pairs.append(sd)
    return valid_pairs


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def output_plot(path, data):
    from plotly import offline as py
    from plotly import graph_objs as go

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

    to_plot = []
    for k in sorted(plot_data.keys()):
        to_plot.append(go.Scatter(plot_data[k]))

    py.plot(to_plot, filename=path, auto_open=False)
