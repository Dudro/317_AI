from simulation import *
from State import State
import utils
import argparse

# Default values for command line arguments.
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


def parse_positive_int(value):
    """
    Returns the integer value of the given string, raising an error if the
    string cannot be parsed to an integer, or if the resulting integer is not
    positive.

    :param value: the string to parse
    :rtype: int
    """
    pos = int(value)
    if pos < 1:
        raise argparse.ArgumentTypeError("invalid value: " + value)
    return pos


def parse_bound(value):
    """
    Returns the bound value resulting from parsing the given string, where
    bound is one of the arguments to bounded_a_star, raising an error if the
    value cannot be parsed to an int or a float, or if the value is greater
    than 1, but is not an int.

    :param value: the string to parse
    :rtype: int or float
    """
    b = float(value)
    if b > 1 and not b.is_integer():
        raise argparse.ArgumentTypeError("invalid bound argument: " + value)
    if b.is_integer():
        return int(b)
    else:
        return b


def parse_heuristic(value):
    """
    Returns both the heuristic function and the heuristic function name
    corresponding to the given value, raising an error if the value is not a
    legal heuristic function name.

    :param value: the string to parse
    :return: (State => float, string)
    """
    if value == "zero":
        return State.zero_h, value
    elif value == "undelivered":
        return State.undelivered_h, value
    elif value == "scaled":
        return State.sum_of_package_distance_scaled_h, value
    elif value == "sum":
        return State.sum_of_package_distance_h, value
    else:
        raise argparse.ArgumentTypeError("invalid heuristic argument: " + value)


if __name__ == "__main__":
    # Define command line arguments.
    parser = argparse.ArgumentParser(description="Run simulations of search "
                                                 "for the N-K Problem using "
                                                 "various search algorithms.")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="more verbose output")
    parser.add_argument("-a", "--a-star", action='store_true',
                        help="run simulations using A* Search")
    parser.add_argument("-b", "--bounded-a-star", action='store_true',
                        help="run simulations using Bounded A* Search")
    parser.add_argument("-l", "--local-beam", action='store_true',
                        help="run simulations using Local Beam Search")
    parser.add_argument("--num-sims", type=parse_positive_int,
                        default=defaults['num_sims'],
                        help="total number of simulations to run")
    parser.add_argument("-n", "--vehicles", type=parse_positive_int,
                        default=defaults['n'],
                        help="number of cars for each simulation")
    parser.add_argument("-k", "--packages", type=parse_positive_int,
                        default=defaults['k'],
                        help="number of packages for each simulation")
    parser.add_argument("-m", "--locations", type=parse_positive_int,
                        default=defaults['m'],
                        help="number of locations in the input map")
    parser.add_argument("--heuristic", type=parse_heuristic,
                        default=(defaults['h'], defaults['h_name']),
                        choices=["zero", "undelivered", "scaled", "sum"],
                        help="heuristic function to use")

    parser.add_argument("--bound", type=parse_bound, default=defaults['bound'],
                        help="causes Bounded A* to keep only the best BOUND "
                             "number of successors for any given state; can "
                             "be either a percentage of successors to keep "
                             "(if between 0 and 1, both exclusive), or the "
                             "maximum number of successors to keep (if an "
                             "integer 1 or greater); if 0 or less, keep all "
                             "successors, like regular A*")
    parser.add_argument("--k-limit", type=parse_positive_int,
                        default=defaults['k_limit'],
                        help="causes Local Beam Search to consider only the "
                             "best (K_LIMIT - 1) successors of any given "
                             "state at each level of recursion")

    # Parse command line arguments.
    args = parser.parse_args()
    verbose = args.verbose
    a_star = args.a_star
    bounded_a_star = args.bounded_a_star
    local_beam = args.local_beam
    num_sims = args.num_sims
    n = args.vehicles
    k = args.packages
    m = args.locations
    h, h_name = args.heuristic
    bound = args.bound
    k_limit = args.k_limit

    if not a_star and not bounded_a_star and not local_beam:
        raise parser.error("at least one of -a, -b, or -l must be given")

    # Run the simulations and record simulation results.
    name = "sims" + str(num_sims) + ".n" + str(n) + ".k" + str(k) + ".m" + \
           str(m) + "." + h_name + "."

    if verbose and a_star:
        print("Regular A* simulations.")
    if a_star:
        data_a_star = a_star_simulations(n, k, m, h, num_sims, verbose)
        utils.dump_json_data(name + "a_star", data_a_star)
        utils.plot_results(name + "a_star", data_a_star)

    if verbose and bounded_a_star:
        print("Bounded A* simulations.")
    if bounded_a_star:
        data_bounded_a_star = bounded_a_star_simulations(n, k, m, h, num_sims,
                                                         bound, verbose)
        bound_name = name + "bound" + str(bound) + ".bounded_a_star"
        utils.dump_json_data(bound_name, data_bounded_a_star)
        utils.plot_results(bound_name, data_bounded_a_star)

    if verbose and local_beam:
        print("Local Beam Search simulations.")
    if local_beam:
        data_local_beam = local_beam_simulations(n, k, m, h, num_sims, k_limit,
                                                 verbose)
        local_beam_name = name + "k_limit" + str(k_limit) + ".local_beam"
        utils.dump_json_data(local_beam_name, data_local_beam)
        utils.plot_results(local_beam_name, data_local_beam)
