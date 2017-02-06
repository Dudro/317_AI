from queue import PriorityQueue


def greedy_search(state, is_goal, trans_op, f, k_limit=20):
    """
    if is_goal(state) then
        return state as a goal state
    else
        candidates = trans_op(state)
        choose (k-1) states, x, from candidates with the lowest f(x) values
        recursively apply local_beam_search on each of those states

    :param state: a current state
    :type state: X, where X is the argument type of is_goal, trans_op, and f
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
    :param k_limit: the number of successor states that will being considered
        minus 1. Default: 20.
    :type k_limit: int
    :rtype: X (a goal state), integral
    """
    return _greedy_search_helper(0, state, is_goal, trans_op, f, k_limit)


def _greedy_search_helper(counter, state, is_goal, trans_op, f, k_limit):
    """
    A helper method that counts the number of nodes expanded, where 'counter'
    records the number of nodes expanded so far.
    """
    counter += 1
    if is_goal(state):
        goal_state = state
        yield goal_state, counter
    else:
        potential_temp = PriorityQueue()
        potential = []
        candidate = trans_op(state)
        for mem in candidate:
            mem_cost = f(mem)
            if not potential_temp.empty():
                found = False
                for tup in potential_temp.queue:
                    if tup[0] == mem_cost:
                        found = True
                        break
                if not found:
                    potential_temp.put((mem_cost, mem))
            else:
                potential_temp.put((mem_cost, mem))

            if k_limit >= len(potential_temp.queue):
                potential = potential_temp.queue
            else:
                potential = potential_temp.queue[0:k_limit]
        for mem in potential:
            for sol, exp in _greedy_search_helper(counter, mem[1], is_goal,
                                                      trans_op, f, k_limit):
                counter = exp
                yield sol, counter


def local_beam_search(state, is_goal, trans_op, f, k_limit=20):
    """
    explore all the nodes of state, using trans_op
    while there is an unvisited node
        find best k_limit number of nodes
        if any of them is a goal node, return that
        explore the k_limit nodes, and store them in priority queue
        return if goal is found


    :param state: a current state
    :type state: X, where X is the argument type of is_goal, trans_op, and f
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
    :param k_limit: the number of successor states that will being considered
        minus 1. Default: 20.
    :type k_limit: int
    :rtype: X (a goal state), integral
    """
    counter = 0
    candidates = PriorityQueue()
    candidates.put((f(state),counter, state))
    while not candidates.empty():
        if len(candidates.queue) > k_limit:
            temp_candidate = PriorityQueue()
            for i in range(0,k_limit):
                temp_candidate.put(candidates.get())
            candidates = temp_candidate
        temp_candidate = PriorityQueue()
        while not candidates.empty():
            s = candidates.get()
            new_candidates = trans_op(s[2])
            for candidate in new_candidates:
                counter += 1
                if is_goal(candidate):
                    yield candidate, counter
                temp_candidate.put((f(candidate),counter, candidate))
        candidates = temp_candidate
