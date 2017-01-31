from simulation import *
from State import State
import utils
import sys

defaults = {
    'num_sims': 25,
    'n': 2,
    'k': 5,
    'm': 30,
    'h': State.sum_of_package_distance_h,
    'h_name': "sum",
    'bound': 0.01,
    'k_limit': 20
}


def usage(program_name, msg):
    """
    Prints the program name and the message (as well as a generic usage
    message) to standard error, and then exits the program with status 1.

    :param program_name: the name of the program
    :param msg: the message to print
    """
    from utils import eprint
    eprint(program_name, ":", msg)
    eprint("  num_sims -- The total number of simulations to run. Default:",
           defaults['num_sims'])
    eprint("  n        -- The number of cars for each simulation. Default:",
           defaults['n'])
    eprint("  k        -- The number of packages for each simulation. Default:",
           defaults['k'])
    eprint("  m        -- The number of locations in the input map. Default:",
           defaults['m'])
    eprint("  h        -- The heuristic function to use; one of zero,")
    eprint("              undelivered, scaled, or sum. Default:",
           defaults['h_name'])
    eprint("  bound    -- Causes Bounded A* to keep only the best 'bound'")
    eprint("              number of successors for any given state. Can be")
    eprint("              either a percentage of successors to keep (if")
    eprint("              between 0 and 1, both exclusive), or the maximum")
    eprint("              number of successors to keep (if an integer 1 or")
    eprint("              greater). If 0 or less, keep all successors, like")
    eprint("              regular A*. Default:", defaults['bound'])
    eprint("  k_limit  -- Causes Local Beam Search to consider only the best")
    eprint("              (k_limit - 1) successors of any given state at each")
    eprint("              level of recursion. Default:", defaults['k_limit'])
    sys.exit(1)


if __name__ == "__main__":
    # Set variables to default values.
    num_sims = defaults['num_sims']
    n = defaults['n']
    k = defaults['k']
    m = defaults['m']
    h = defaults['h']
    h_name = defaults['h_name']
    bound = defaults['bound']
    k_limit = defaults['k_limit']

    # Parse command line arguments.
    if len(sys.argv) > 1:
        try:
            num_sims = int(sys.argv[1])
            if num_sims < 1:
                raise ValueError
        except ValueError:
            usage(sys.argv[0], "Invalid simulation argument: " + sys.argv[1])
    if len(sys.argv) > 2:
        try:
            n = int(sys.argv[2])
            if n < 1:
                raise ValueError
        except ValueError:
            usage(sys.argv[0], "Invalid vehicle argument: " + sys.argv[2])
    if len(sys.argv) > 3:
        try:
            k = int(sys.argv[3])
            if k < 1:
                raise ValueError
        except ValueError:
            usage(sys.argv[0], "Invalid package argument: " + sys.argv[3])
    if len(sys.argv) > 4:
        try:
            m = int(sys.argv[4])
            if m < 1:
                raise ValueError
        except ValueError:
            usage(sys.argv[0], "Invalid location argument: " + sys.argv[4])
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
            usage(sys.argv[0], "Invalid heuristic argument: " + sys.argv[5])
    if len(sys.argv) > 6:
        try:
            bound = float(sys.argv[6])
            if bound > 1 and not isinstance(bound, int):
                raise ValueError
        except ValueError:
            usage(sys.argv[0], "Invalid bound argument: " + sys.argv[6])
    if len(sys.argv) > 7:
        try:
            k_limit = int(sys.argv[7])
            if k_limit < 1:
                raise ValueError
        except ValueError:
            usage(sys.argv[0], "Invalid k limit argument: " + sys.argv[7])

    # Run the simulations and record simulation results.
    name = "n" + str(n) + ".k" + str(k) + ".m" + str(m) + "." + h_name + "."

    print("Regular A* simulations.")
    data_a_star = a_star_simulations(n, k, m, h, num_sims)
    utils.dump_json_data(name + "a_star", data_a_star)
    utils.plot_results(name + "a_star", data_a_star)

    print("Bounded A* simulations.")
    data_bounded_a_star = bounded_a_star_simulations(n, k, m, h, num_sims,
                                                     bound)
    utils.dump_json_data(name + "bounded_a_star", data_bounded_a_star)
    utils.plot_results(name + "bounded_a_star", data_bounded_a_star)

    print("Local Beam Search simulations.")
    data_local_beam = local_beam_simulations(n, k, m, h, num_sims, k_limit)
    utils.dump_json_data(name + "local_beam", data_local_beam)
    utils.plot_results(name + "local_beam", data_local_beam)
