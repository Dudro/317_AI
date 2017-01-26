from queue import PriorityQueue

def astar(initial_state, is_goal, trans_op, f):
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
    :type state: X, where X is the argument type of is_goal, trans_op and f
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
    queue = PriorityQueue()
    queue.put((f(initial_state), initial_state))
    while not queue.empty():
        _, next_state = queue.get()
        # print("Next state cost: " + str(f(next_state)) + ", " + str(queue.qsize()), flush=True)
        # print("Next state details: ", flush = True)
        # print(next_state.get_car_locs(), flush=True)
        # print(next_state.get_packages(), flush=True)
        if is_goal(next_state):
            #print("Yielding", flush=True)
            yield next_state
        else:
            successors = trans_op(next_state)
            for successor in successors:
                # print("Examining successor: ", flush=True)
                # print(successor.get_car_locs(), flush=True)
                # print(successor.get_packages(), flush=True)
                queue.put((f(successor), successor))


    return None