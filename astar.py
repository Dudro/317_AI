from queue import PriorityQueue

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
        print("State cost: " + str(f(next_state)) + ", " + str(queue.qsize()), flush=True)
        if is_goal(next_state):
            print("Yielding", flush=True)
            yield next_state
        else:
            successors = trans_op(next_state)
            #print(str(len(successors)), flush=True)
            for successor in successors:
                #print("Hey")
                print(successor.get_car_locs(), flush=True)
                print(successor.get_packages(), flush=True)
                queue.put((f(successor), successor))


    return None