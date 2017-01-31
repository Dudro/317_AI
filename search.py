import timing
from State import *


def a_star_any_graph(n, k, m, full_map, pairs, h, num_sols=1):
    """
    Runs A* with the specified heuristic on the given problem. The problem
    definition involves n, k, m, a map, and source-destination pairs. The
    number of solutions to generate can be specified, but if the heuristic 'h'
    is admissible, the first solution generated will always be the optimal
    solution. Returns a dictionary of search results. Although, the number of
    solutions to generate can be specified, and some search results will be
    returned regardless, most search results are only given if the number of
    solutions to generate is 1.

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
    :param h: the heuristic function that A* will use
    :type h: State => float
    :param num_sols: the number of solutions that should be generated, or -1 if
        all possible solutions should be generated. Default: 1.
    :type num_sols: int
    :rtype: dict
    """
    from astar import a_star_count_nodes
    return _run_search(n, k, m, full_map, pairs, num_sols, h,
                       a_star_count_nodes)


def local_beam_any_graph(n, k, m, full_map, pairs, h, k_limit, num_sols=1):
    """
    Runs Local Beam Search with the specified heuristic on the given problem.
    The problem definition involves n, k, m, a map, and source-destination
    pairs. Returns a dictionary of search results. Although, the number of
    solutions to generate can be specified, and some search results will be
    returned regardless, most search results are only given if the number of
    solutions to generate is 1.

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
    :param h: the heuristic function that Local Beam Search will use
    :type h: State => float
    :param k_limit: the number of successor states that will being considered
        minus 1
    :type k_limit: int
    :param num_sols: the number of solutions that should be generated, or -1 if
        all possible solutions should be generated. Default: 1.
    :type num_sols: int
    :rtype: dict
    """
    from localbeam import local_beam_search
    return _run_search(n, k, m, full_map, pairs, num_sols, h,
                       local_beam_search, k_limit)


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
    if not _parameters_valid(n, k, m, full_map, pairs, num_sols):
        return None
    initial, time = _create_problem_representation(n, k, m, full_map, pairs)
    data = _do_run_search(num_sols, algorithm, initial, is_goal,
                          state_transition, decorating_f(h), *args, **kwargs)
    data['pre_processing_time'] = time
    return data


def _parameters_valid(n, k, m, full_map, pairs, num_sols):
    """
    Returns True if all parameters are valid, and prints an error message to
    standard error and returns False otherwise.

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
    :rtype: bool
    """
    from networkx import number_of_nodes
    from utils import eprint

    if k != len(pairs):
        eprint("Error: K is not equal to the length of src-dest pairs.")
        return False
    if m != number_of_nodes(full_map):
        eprint("Error: M is not equal to the number of vertices in the graph.")
        return False
    if n < 1:
        eprint("Error: N cannot be less than 1.")
        return False
    if num_sols != -1 and num_sols < 1:
        eprint("Error: The number of desired solutions must be -1 or else",
               "cannot be less than 1.")
        return False
    return True


def _create_problem_representation(n, k, m, full_map, pairs):
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
    timing.start_timer()
    world.process_map()
    pre_processing_time = '{:.4f}'.format(timing.end_timer())
    cars = [[world.get_garage()]] * n
    packages = [False] * k
    initial = State(world, cars, packages, 0)
    return initial, pre_processing_time


def _do_run_search(num_sols, algorithm, *args, **kwargs):
    """
    Runs the given algorithm with the given arguments, and collects the given
    number of solutions. Returns a dictionary of search results, which will be
    non-empty if, and only if, the number of solutions to be generated is 1.

    :param num_sols: the number of solutions that should be generated, or -1 if
        all possible solutions should be generated.
    :type num_sols: int
    :param algorithm: the search algorithm to use; e.g. a_star_count_nodes or
        local_beam_search. It should return both a solution state and a count
        of the number of nodes expanded during the search.
    :type algorithm: (*args, **kwargs) => (State, int)
    :param args: arguments to 'algorithm'
    :param kwargs: arguments to 'algorithm'
    :rtype: dict
    """
    if num_sols == 1:
        timing.start_timer()
        sol, count = next(algorithm(*args, **kwargs))
        data = {
            'node_count': count,
            'cost_sum': sol.get_g(),
            'simulation_time': '{:.4f}'.format(timing.end_timer())
        }
        return data
    elif num_sols == -1:
        for sol, count in algorithm(*args, **kwargs):
            print("count=", count, "cost=", sol.get_g(), recreate_paths(sol))
        return {}
    else:
        for _ in range(num_sols):
            sol, count = next(algorithm(*args, **kwargs))
            print("count=", count, "cost=", sol.get_g(), recreate_paths(sol))
        return {}
