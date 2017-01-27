from State import *
from World import World
import graphs
from astar import *


def is_goal(state):
    """
    Determines whether the given state is a goal state.

    :param state: a particular state
    :type state: State
    :rtype: True if the given state is a goal state, False otherwise.
    """
    return False if False in state.get_packages() else True


def decorating_f(h):
    def true_f(state):
        return state.get_g() + h(state)

    return true_f


def recreate_paths(state):
    world = state.get_world()
    all_paths = []
    for car_stack in state.get_car_locs():
        loc = car_stack.pop()
        this_path = []
        while car_stack:  # Means "while car_stack is not empty"
            prev = car_stack.pop()
            if prev != loc:
                if this_path:  # Means "if this_path is not empty"
                    this_path.pop()  # Remove last item since it's duplicated.
                this_path.extend(world.get_shortest_path(loc, prev))
            loc = prev
        this_path.reverse()
        all_paths.append(this_path)
    return all_paths


def a_star_any_graph(n, k, m, full_map, pairs, f, num_sols=None):
    world = World(n, k, m, full_map, pairs)
    world.process_map()
    cars = [[world.get_garage()]] * n
    packages = [False] * k
    initial = State(world, cars, packages, 0)
    if num_sols is None:
        for sol, count in a_star_count_nodes(initial, is_goal,
                                             state_transition, f):
            print("Count", count, "cost", sol.get_g(), sol.get_car_locs())
    else:
        for i in range(num_sols):
            sol, count = next(a_star_count_nodes(initial, is_goal,
                                                 state_transition, f))
            print("Count", count, "cost", sol.get_g(), sol.get_car_locs())


def a_star_triangle_graph(n, k, f):
    print("Starting triangle test", flush=True)
    full_map, pairs = graphs.get_triangle_graph()
    a_star_any_graph(n, k, full_map.number_of_nodes(), full_map, pairs, f)
    print("Done triangle", flush=True)


def a_star_ogg_graph(n, k, f):
    print("Starting OGG test", flush=True)
    full_map, pairs = graphs.get_og_graph()
    a_star_any_graph(
            n, k, full_map.number_of_nodes(), full_map, pairs, f, num_sols = 1)
    print("Done OGG", flush=True)


def a_star_circle_graph(n, f):
    print("Starting circle test", flush=True)
    full_map, pairs = graphs.get_circle_graph()
    k = len(pairs)
    a_star_any_graph(n, k, full_map.number_of_nodes(), full_map, pairs, f, 1)
    print("Done circle", flush=True)


if __name__ == "__main__":
    a_star_triangle_graph(1, 2, decorating_f(State.zero_h))
    print("ogg zero")
    a_star_ogg_graph(2, 3, decorating_f(State.zero_h))
    print("ogg undelivered")
    a_star_ogg_graph(2, 3, decorating_f(State.undelivered_h))
    print("ogg sum_of_package_distance")
    a_star_ogg_graph(2, 3, decorating_f(State.sum_of_package_distance_h))
    print("ogg scaled")
    a_star_ogg_graph(2, 3, decorating_f(State.sum_of_package_distance_scaled_h))
    print("circle undelivered")
    a_star_circle_graph(2, decorating_f(State.undelivered_h))
    print("circle sum of distance")
    a_star_circle_graph(2, decorating_f(State.sum_of_package_distance_h))
    print("circle scaled")
    a_star_circle_graph(2, decorating_f(State.sum_of_package_distance_scaled_h))
