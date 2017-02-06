import search as s
#import timing
from State import *

def vanilla_a_star_any_graph(n, k, m, full_map, pairs, h, num_sols=1):
    from astar import a_star_count_nodes
    return _run_search(n, k, m, full_map, pairs, num_sols, h,
                       a_star_count_nodes)

def vanilla_a_star_triangle(h, num_sols=1):
    from astar import a_star_count_nodes
    from graphs import get_triangle_graph

    full_map, pairs = get_triangle_graph()

    print("Triangle graph: ")
    data = _run_search(1, 2, 3, full_map, pairs, num_sols, h,
                       a_star_count_nodes)
    print("Results: ")
    print(data)

def vanilla_a_star_ogg(h, num_sols=1):
    from astar import a_star_count_nodes
    from graphs import get_ogg_graph
    full_map, pairs = get_ogg_graph()
    print
    print("OG graph: ")
    data = _run_search(2, 3, 9, full_map, pairs, num_sols, h,
                       a_star_count_nodes)
    print("Results: ")
    print(data)

def vanilla_a_star_circle(h, num_sols=1):
    from astar import a_star_count_nodes
    from graphs import get_circle_graph
    full_map, pairs = get_circle_graph()
    print("Circle graph: ")
    data = _run_search(1, 10, 10, full_map, pairs, num_sols, h,
                       a_star_count_nodes)
    print("Results: ")
    print(data)
    return 0

def _run_search(n, k, m, full_map, pairs, num_sols, h, algorithm, *args,
                **kwargs):
    """
    Runs the given search algorithm with the specified heuristic on the given
    problem. The problem definition involves n, k, m, a map, and source-
    destination pairs. Returns a dictionary of search results. The number of
    solutions to generate can be specified, and some search results will be
    returned regardless, however, most search results are only given if the
    number of solutions to generate is 1.

    :param n: the number of cars in this problem
    :type n: int
    :param k: the number of packages in this problem
    :type k: int
    :param m: the number of vertices in the full map for this problem
    :type m: int
    :param full_map: the full map of all locations for the problem. It could be
        generated randomly or predefined.
    :type full_map: NetworkX Graph
    :param pairs: a list of source-destination pairs of all the packages in the
        problem. Each source and each destination must correspond to a location
        in the full map.
    :type pairs: list((int, int))
    :param num_sols: the number of solutions that should be generated, or -1 if
        all possible solutions should be generated.
    :type num_sols: int
    :param h: the heuristic function that 'algorithm' will use
    :type h: State => float
    :param algorithm: the search algorithm to use; e.g. a_star_count_nodes or
        local_beam_search. It should return both a solution state and a count
        of the number of nodes expanded during the search.
    :type algorithm: (*args, **kwargs) => (State, int)
    :param args: arguments to 'algorithm'
    :param kwargs: arguments to 'algorithm'
    :rtype: dict
    """
    if not s._parameters_valid(n, k, m, full_map, pairs, num_sols, 'VanillaState'):
        return None
    initial, time = _create_problem_representation_vanilla(n, k, m, full_map, pairs)
    data = s._do_run_search(num_sols, algorithm, initial, is_goal,
                          state_transition_vanilla, decorating_f(h), *args, **kwargs)
    data['pre_processing_time'] = time
    return data

def _create_problem_representation_vanilla(n, k, m, full_map, pairs):
    """
    Represents the problem with a World and and initial State of search.
    Returns the initial state, and a formatted string representing the process
    execution time taken to pre-process the given map.

    :param n: the number of cars in this problem
    :type n: int
    :param k: the number of packages in this problem
    :type k: int
    :param m: the number of vertices in the full map for this problem
    :type m: int
    :param full_map: the full map of all locations for the problem. It could be
        generated randomly or predefined.
    :type full_map: NetworkX Graph
    :param pairs: a list of source-destination pairs of all the packages in the
        problem. Each source and each destination must correspond to a location
        in the full map.
    :type pairs: list((int, int))
    :rtype: (State, string)
    """
    world = World(n, k, m, full_map, pairs)
    pre_processing_time = '{:.4f}'.format(0)
    cars = [[world.get_garage()]] * n
    packages = [False] * k
    held = [-1] * n
    initial = VanillaState(world, cars, packages, 0, held)
    return initial, 0


vanilla_a_star_triangle(VanillaState.sum_of_estimated_cost_scaled_h, num_sols=1)

vanilla_a_star_ogg(VanillaState.sum_of_estimated_cost_scaled_h, num_sols=1)

vanilla_a_star_circle(VanillaState.sum_of_estimated_cost_scaled_h, num_sols=1)