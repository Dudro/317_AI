from State import *
from World import World
import graphs
from astar import *
import sys


def decorating_f(h):
    def true_f(state):
        return state.get_g() + h(state)

    return true_f


def recreate_paths(state):
    world = state.get_world()
    all_paths = []
    for car_stack in state.get_car_locs():
        if len(car_stack) == 1:  # Car is still at garage
            this_path = [car_stack.pop()]
        else:
            loc = car_stack.pop()
            this_path = []
            while car_stack:  # Means "while car_stack is not empty"
                prev = car_stack.pop()
                if prev != loc:
                    if this_path:  # Means "if this_path is not empty"
                        this_path.pop()  # Remove last item; it's duplicated.
                    this_path.extend(world.get_shortest_path(loc, prev))
                loc = prev
            this_path.reverse()
        all_paths.append(this_path)
    return all_paths


def a_star_any_graph(n, k, m, full_map, pairs, f, num_sols=None, output=None):
    """
    :param n: The number of cars in this problem.
    :type n: int
    :param k: The number of packages in this problem.
    :type k: int
    :param m: The number of vertices in the original graph for this problem.
    :type m: int
    :param full_map: The full graph of the problem.  It could be generated 
        randomly or predefined.
    :type full_map: Graph
    :param pairs: A list of source-destination pairs of all the packages in the 
        problem.
    :type pairs: list(tuple(int,int))
    :param f: The heurisitic function that A* will use.
    :type f: function
    :param num_sols: The number of solutions the user would like to generate.
    :type num_sols: int
    :param output: The name of a file to which output can be redirected.
    :type output: String
    Run A* with a specified heuristic on the a problem.  The problem 
    definition involves n, k, m, the graph, and the src-dest pairs.  The 
    number of solutions to generate can be specified, but if the heurisitic
    provided in 'f' is admissible, the first solution generated will be
    the optimal solution.  Output can be redirected to a file if specified.
    """
    
    # Redirect output to file if specified.
    original_stdout = sys.stdout
    if output is not None:
        opened_file = open(output,'a+')
        sys.stdout = opened_file

    world = World(n, k, m, full_map, pairs)
    world.process_map()
    cars = [[world.get_garage()]] * n
    packages = [False] * k
    initial = State(world, cars, packages, 0)
    if num_sols is None:
        for sol, count in a_star_count_nodes(initial, is_goal,
                                             state_transition, f):
            print("Count", count, "cost", sol.get_g(), recreate_paths(sol))
    else:
        for i in range(num_sols):
            sol, count = next(a_star_count_nodes(initial, is_goal,
                                                 state_transition, f))
            print("Count", count, "cost", sol.get_g(), recreate_paths(sol))
    sys.stdout = original_stdout


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


def known_graphs_test():
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


def simulations(number_of_cars, number_of_packages, number_of_nodes,h, number_of_simulations = 100):
    for i in range(number_of_simulations):
        random_graph, pairs = graphs.get_random_graph(number_of_nodes,number_of_cars,number_of_packages)
        k = len(pairs)
        a_star_any_graph(number_of_cars, number_of_packages, number_of_nodes, random_graph, pairs, h, 1,'output.txt')


if __name__ == "__main__":
    simulations(4,8,20,State.sum_of_package_distance_h)




