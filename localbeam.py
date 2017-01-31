from queue import PriorityQueue


def local_beam_search(state, is_goal, trans_op, f, k_limit=20):
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
    :type: State
    """
    return _local_beam_search_helper(0, state, is_goal, trans_op, f, k_limit)


def _local_beam_search_helper(counter, state, is_goal, trans_op, f, k_limit):
    counter += 1
    if is_goal(state):
        goal_state = state
        yield goal_state, counter
    else:
        # may add a counter here to count how many nodes that we have explored

        potential_temp = PriorityQueue()
        potential = []
        candidate = trans_op(state)
        for mem in candidate:
            mem_cost = f(mem)
            # question : Should we check for duplicates or not
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
        # for mem in candidate:
        #     if mem.get_g() == min(cost) and potential.empty():
        #         potential.put(mem)
        #         state_w_min = mem
        #     elif mem state_w_min

        for mem in potential:
            for sol, exp in _local_beam_search_helper(0, mem[1], is_goal,
                                                      trans_op, f, k_limit):
                counter += exp
                yield sol, counter
