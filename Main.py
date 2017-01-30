import json
from State import *
from World import World
import graphs
from astar import *
from localbeam import *
import sys
import utils as u
from networkx import number_of_nodes
import matplotlib.pyplot as plt
import timing as timer


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

def localbeam_any_graph(
        n,
        k,
        m,
        full_map,
        pairs,
        h,
        data,
        kLimit,
        num_sols=None,
        t=None,
):
    """
    :param n:
    :param k:
    :param m:
    :param full_map:
    :param pairs:
    :param h:
    :param data:
    :param kLimit:
    :param num_sols:
    :param t:
    :return:

    if k != len(pairs):
        u.eprint("Error: k is not equal to the length of src-dest pairs.")
        return None
    if m != number_of_nodes(full_map):
        u.eprint("Error: m is not equal to the size of the graph.")
        return None
    if n < 1:
        u.eprint("Error: n cannot be less than 1.")
        return None
    if num_sols is not None and num_sols < 1:
        u.eprint("Error: The number of solutions cannot be less than 1.")
        return None

    world = World(n, k, m, full_map, pairs)
    timer.start_timer(t)
    world.process_map()
    s = '{1:.4f}'.format(t, timer.end_timer(t))
    data[t]['preprocessing_time'] = s
    cars = [[world.get_garage()]] * n
    packages = [False] * k
    initial = State(world, cars, packages, 0)

    if num_sols is None:
        timer.start_timer(t)
        sol, count = next(
                local_beam_search(initial, is_goal, state_transition, h, kLimit))
        data[t]['node_count'] = count
        data[t]['cost_sum'] = sol.get_g()
        s = '{1:.4f}'.format(t, timer.end_timer(t))
        data[t]['simulation_time'] = s
        # print(recreate_paths(sol))
    else:
        for i in range(num_sols):
            sol, count = next(local_beam_search(initial, is_goal,
                                                 state_transition, h, kLimit))
            print("count=", count, "cost=", sol.get_g(), recreate_paths(sol))
    """


def a_star_any_graph(
        n, 
        k, 
        m, 
        full_map, 
        pairs, 
        h, 
        data,
        num_sols=None, 
        t=None):
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
    :param h: The heurisitic function that A* will use.
    :type h: function
    :param num_sols: The number of solutions the user would like to generate.
    :type num_sols: int
    :param t: The number of the simulation for the timer.
    :type t: int
    Run A* with a specified heuristic on the a problem.  The problem 
    definition involves n, k, m, the graph, and the src-dest pairs.  The 
    number of solutions to generate can be specified, but if the heurisitic
    provided in 'f' is admissible, the first solution generated will be
    the optimal solution.  Output can be redirected to a file if specified.
    """
    if k != len(pairs):
        u.eprint("Error: k is not equal to the length of src-dest pairs.")
        return None
    if m != number_of_nodes(full_map):
        u.eprint("Error: m is not equal to the size of the graph.")
        return None
    if n < 1:
        u.eprint("Error: n cannot be less than 1.")
        return None
    if num_sols is not None and num_sols < 1:
        u.eprint("Error: The number of solutions cannot be less than 1.")
        return None
    
    
    world = World(n, k, m, full_map, pairs)
    timer.start_timer(t)
    world.process_map()
    s = '{1:.4f}'.format(t, timer.end_timer(t))
    data[t]['preprocessing_time'] = s
    cars = [[world.get_garage()]] * n
    packages = [False] * k
    initial = State(world, cars, packages, 0)
    
    if num_sols is None: 
        timer.start_timer(t)
        sol, count = next(
                a_star_count_nodes(initial, is_goal, state_transition, decorating_f(h)))
        data[t]['node_count'] = count
        data[t]['cost_sum'] = sol.get_g()
        s = '{1:.4f}'.format(t, timer.end_timer(t))
        data[t]['simulation_time'] = s
        # print(recreate_paths(sol))
    else:
        for i in range(num_sols):
            sol, count = next(a_star_count_nodes(initial, is_goal,
                                                 state_transition, decorating_f(h)))
            print("count=", count, "cost=", sol.get_g(), recreate_paths(sol))
    
def astar_simulations(n, k, m, h, num_sims=100, output=None):
    """
    :param n: The number of cars in this problem.
    :type n: int
    :param k: The number of packages in this problem.
    :type k: int
    :param m: The number of vertices in the graph for this problem.
    :type m: int
    :param h: The heurisitic function that A* will use.
    :type h: function
    :param num_sims: The number of graphs to generate, and the number of times
        the simulation will run.
    :type num_sims: int
    :param output: The name of a file to which output can be redirected.
    :type output: String
    Run A* with a specified heuristic on many different problems.  The number
    of times to run the simulation depends on the input 'num_sims'.  The method
    'get_random_graph' will generate a new random problem according to the 
    parameters n, k, and m for as many simulation as specified.  Output from 
    A* will be redirected to a file if provided.
    """
        
    # Initialize dictionaries for data collection
    data = [{} for i in range(num_sims)]
    # Begin running the simulations
    for i in range(num_sims):
        random_graph, pairs = graphs.get_random_graph(k, m)
        pairs = u.filter_pairs(pairs)
        u.eprint("Starting problem " + str(i), flush=True)
        a_star_any_graph(n, k, m, random_graph, pairs, h, data,t=i)
    
    return data


def dump_json_data(name, data):
    file_name = name + ".json"
    with open(file_name, 'w+') as out:
        json.dump(data, out, indent=4)

def plot_results(name, data):
    plot_name = name + ".html"
    u.output_plot(plot_name, data)

if __name__ == "__main__":

    #default values
    sims = 25
    n = 2
    k = 5
    m = 30
    h = State.sum_of_package_distance_h
    h_name = "sum"
    
    #Argument order: filename, number of simulations, n, k, m, heuristic
    if len(sys.argv) > 1:
        try: 
            sims = int(sys.argv[1])
        except ValueError:
            u.eprint("Invalid simulation argument.")
    if len(sys.argv) > 2:
        try: 
            n = int(sys.argv[2])
        except ValueError:
            u.eprint("Invalid vehicle argument.")
    if len(sys.argv) > 3:
        try: 
            k = int(sys.argv[3])
        except ValueError:
            u.eprint("Invalid package argument.")
    if len(sys.argv) > 4:
        try: 
            m = int(sys.argv[4])
        except ValueError:
            u.eprint("Invalid location argument.")
    if len(sys.argv) > 5:
        if sys.argv[5] == "zero":
            h = State.zero_h
            h_name = "zero"
        elif sys.argv[5] == "undelivered":
            h = State.undelivered_h
            h_name = "undelivered"
        elif sys.argv[5] == "scaled":
            h = State.sum_of_package_distance_scaled_h
            h_name = "scaled"
        elif sys.argv[5] == "sum":
            h = State.sum_of_package_distance_h
            h_name = "sum"
        else:
            u.eprint("Invalid heuristic argument.")
    
    data = astar_simulations(
            n, 
            k, 
            m, 
            h, 
            num_sims=sims)
    
    name = "n"+str(n)+".k"+str(k)+".m"+str(m)+"."+h_name
    
    dump_json_data(name, data)

    plot_results(name, data)

