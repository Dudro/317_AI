from Queue import PriorityQueue

def astar(initial_state, is_goal, trans_op, f):
    """
    :param f: a function that takes a state, x, and computes
    f(x) = g(x) + h(x), where g is the cost so far from the initial state
    to x, and h is the estimated remaining cost from x to the goal
    :type f: state => float
    """
    queue = PriorityQueue()
    queue.put((f(initial_state), initial_state))
    while not queue.empty():
        _, next_state = queue.get()
        if is_goal(next_state):
            yield next_state
        else:
            for successor in trans_op(next_state):
                queue.put((f(successor), successor))

