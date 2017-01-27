from State import *
from World import World
import graphs
from astar import a_star


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


def a_star_any_graph(n, k, m, full_map, pairs, f):
    world = World(n, k, m, full_map, pairs)
    world.process_map()
    cars = [[world.get_garage()]] * n
    packages = [False] * k
    initial = State(world, cars, packages, 0)
    for solution in a_star(initial, is_goal, state_transition, f):
        print(solution.get_g(), solution.get_car_locs())


def a_star_triangle_graph(n, k, f):
    print("Starting triangle test", flush=True)
    full_map, pairs = graphs.get_triangle_graph()
    a_star_any_graph(n, k, full_map.number_of_nodes(), full_map, pairs, f)
    print("Done triangle", flush=True)


def a_star_ogg_graph(n, k, f):
    print("Starting OGG test", flush=True)
    full_map, pairs = graphs.get_og_graph()
    a_star_any_graph(n, k, full_map.number_of_nodes(), full_map, pairs, f)
    print("Done OGG", flush=True)


def a_star_circle_graph(n, f):
    print("Starting circle test", flush=True)
    full_map, pairs = graphs.get_circle_graph()
    k = len(pairs)
    #a_star_any_graph(n, k, full_map.number_of_nodes(), full_map, pairs, f)
    print("Done circle", flush=True)


if __name__ == "__main__":
    #a_star_triangle_graph(1, 2, decorating_f(State.zero_h))
    #a_star_ogg_graph(1, 3, decorating_f(State.zero_h))
    a_star_circle_graph(1, decorating_f(State.zero_h))
    # a_star_triangle_graph(2, 2, decorating_f(State.zero_h))
    # a_star_ogg_graph(2, 3, decorating_f(State.zero_h))
