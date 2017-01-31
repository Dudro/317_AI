from simulation import *
from State import State
import utils
import sys

# Default values.
num_sims = 25
n = 2
k = 5
m = 30
h = State.sum_of_package_distance_h
h_name = "sum"


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
           num_sims)
    eprint("  n        -- The number of cars for each simulation. Default:", n)
    eprint("  k        -- The number of packages for each simulation. Default:",
           k)
    eprint("  m        -- The number of locations in the input map. Default:",
           m)
    eprint("  h        -- The heuristic function to use; one of zero,")
    eprint("              undelivered, scaled, or sum. Default:", h_name)
    sys.exit(1)


if __name__ == "__main__":
    # Parse command line arguments.
    if len(sys.argv) > 1:
        try:
            num_sims = int(sys.argv[1])
        except ValueError:
            usage(sys.argv[0], "Invalid simulation argument.")
    if len(sys.argv) > 2:
        try:
            n = int(sys.argv[2])
        except ValueError:
            usage(sys.argv[0], "Invalid vehicle argument.")
    if len(sys.argv) > 3:
        try:
            k = int(sys.argv[3])
        except ValueError:
            usage(sys.argv[0], "Invalid package argument.")
    if len(sys.argv) > 4:
        try:
            m = int(sys.argv[4])
        except ValueError:
            usage(sys.argv[0], "Invalid location argument.")
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
            usage(sys.argv[0], "Invalid heuristic argument.")

    # Run the simulations and record simulation results.
    name = "n" + str(n) + ".k" + str(k) + ".m" + str(m) + "." + h_name + "."

    # Regular A*.
    data_a_star = a_star_simulations(n, k, m, h, num_sims)
    utils.dump_json_data(name + "a_star", data_a_star)
    utils.plot_results(name + "a_star", data_a_star)

    # Bounded A*.
    data_bounded_a_star = bounded_a_star_simulations(n, k, m, h, num_sims, 0.3)
    utils.dump_json_data(name + "bounded_a_star", data_bounded_a_star)
    utils.plot_results(name + "bounded_a_star", data_bounded_a_star)

    # Local Beam Search.
    data_local_beam = local_beam_simulations(n, k, m, h, num_sims, k_limit=20)
    utils.dump_json_data(name + "local_beam", data_local_beam)
    utils.plot_results(name + "local_beam", data_local_beam)
