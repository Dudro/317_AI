from queue import PriorityQueue
from math import *


def a_star(initial_state, is_goal, trans_op, f):
    """
    A generic A* implementation for solving informed search problems. It
    is implemented as a generator, meaning that it yields the first
    solution found, and then backtracks to find other solutions. If h(x),
    the heuristic function that forms part of f(x) is admissible, A* is
    optimal, meaning that the first solution yielded by this algorithm will
    be the best one. Otherwise, more solutions can be yielded (if found),
    until the optimal one is encountered. Because the algorithm is a
    generator, solutions are generated lazily (i.e. only upon request), so
    that the search can be aborted as soon as the desired solution is
    found. For each solution, the value returned is a goal state (i.e. a
    state, G, for which is_goal(G) == True). It is up to the user to
    provide appropriate state objects, and an appropriate transition
    operator so as to ensure that G may record any additional information
    that may be of interest, such as the path taken to reach G from the
    initial state.

    :param initial_state: the initial state of the problem
    :type initial_state: X, where X is the argument type of is_goal, trans_op,
        and f
    :param is_goal: a function that takes a state, x, of type X, and
        returns a boolean indicating whether x is a goal state
    :type is_goal: X => bool, where X is any state type
    :param trans_op: a function that takes a state, x, of type X, and
        returns a iterable over type X containing all successor states of x
    :type trans_op: X => list(X), where X is any state type
    :param f: a function that takes a state, x, of type X, and computes
        f(x) = g(x) + h(x), where g(x) is the cost so far from the initial
        state to x, and h(x) is the estimated remaining cost from x to a
        goal state
    :type f: X => float, where X is any state type
    :rtype: X (returns a goal state)
    """
    for goal, _ in a_star_count_nodes(initial_state, is_goal, trans_op, f):
        yield goal


def a_star_count_nodes(initial_state, is_goal, trans_op, f):
    """
    Like a_star but also counts the number of expanded nodes (number of nodes
    pulled out of the priority queue).

    :rtype: X (a goal state), integral
    """
    return bounded_a_star(initial_state, is_goal, trans_op, f, bound=0)


def bounded_a_star(initial_state, is_goal, trans_op, f, bound):
    """
    Like a_star_count_nodes, but each time a state is expanded using the
    transition operator, the successor states are sorted according to their
    f-values, and only the best (i.e. lowest valued) 'bound' number of states
    are placed back into the priority queue.

    :param initial_state: see a_star
    :param is_goal: see a_star
    :param trans_op: see a_star
    :param f: see a_star
    :param bound: if a float between 0 (exclusive) and 1 (exclusive), then
        interpreted as a percentage, and the best 'bound' %, rounded up of
        the successors are kept; if an int that is 1 (inclusive) or greater,
        then interpreted as the maximum number of successors to keep; if 0
        (inclusive) or less, then keep all successors, like regular a_star.
    :type bound: int or float
    :rtype: X (a goal state), integral
    """
    queue = PriorityQueue()
    counter = 0  # Needed to avoid priority queue trying to compare states.
    queue.put((f(initial_state), counter, initial_state))
    counter += 1
    expanded = 0
    while not queue.empty():
        _, _, next_state = queue.get()
        expanded += 1
        if is_goal(next_state):
            yield next_state, expanded
        else:
            successors = trans_op(next_state)
            if bound > 0:
                tmp_queue = PriorityQueue()
                for successor in successors:
                    tmp_queue.put((f(successor), counter, successor))
                    counter += 1
                if 0 < bound < 1:
                    num_to_keep = int(max(1, ceil(tmp_queue.qsize() * bound)))
                else:
                    num_to_keep = min(int(bound), tmp_queue.qsize())
                for _ in range(num_to_keep):
                    queue.put(tmp_queue.get())
            else:
                for successor in successors:
                    queue.put((f(successor), counter, successor))
                    counter += 1
