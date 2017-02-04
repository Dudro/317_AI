from simulation import *
from State import State
import utils
import argparse

# Default values for command line arguments.
defaults = {
    'num_sims': 100,
    'n': 2,
    'k': 5,
    'm': 30,
    'h': State.sum_of_package_distance_h,
    'h_name': "sum",
    'state_type': 'State',
    'bound': 1,
    'k_limit': 20
}

# All available heuristics.
heuristics = {
    "zero": State.zero_h,
    "undelivered": State.undelivered_h,
    "scaled": State.sum_of_package_distance_scaled_h,
    "sum": State.sum_of_package_distance_h
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


def get_file_names(num_sims=defaults['num_sims'],  
                   n=defaults['n'],
                   k=defaults['k'], 
                   m=defaults['m'],
                   h_name=defaults['h_name'],
                   state_type=defaults['state_type'], 
                   bound=defaults['bound'],
                   k_limit=defaults['k_limit']):
    """
    Returns a dict where the keys are search algorithm names and the values are
    the bases (i.e. the part before the extension) of the output file names,
    which depend on the values of the given parameters.

    :rtype: dict
    """
    name_base = "sims" + str(num_sims) +".n" + str(n) + ".k" + \
            str(k) + ".m" + str(m) + "." + str(h_name) + "." + \
            str(state_type) + "."
    
    return {
        'a_star': name_base + "a_star",
        'bounded_a_star': name_base + "bound" + str(bound) + ".bounded_a_star",
        'local_beam': name_base + "k_limit" + str(k_limit) + ".local_beam"
    }


if __name__ == "__main__":
    # Define command line arguments.
    _parser = argparse.ArgumentParser(description="Run simulations of search "
                                                  "for the N-K Problem using "
                                                  "various search algorithms.")
    _parser.add_argument("-v", "--verbose", action='store_true',
                         help="more verbose output")
    _parser.add_argument("-a", "--a-star", action='store_true',
                         help="run simulations using A* Search")
    _parser.add_argument("-b", "--bounded-a-star", action='store_true',
                         help="run simulations using Bounded A* Search")
    _parser.add_argument("-l", "--local-beam", action='store_true',
                         help="run simulations using Local Beam Search")
    _parser.add_argument("--num-sims", type=parse_positive_int,
                         default=defaults['num_sims'],
                         help="total number of simulations to run")
    _parser.add_argument("-n", "--vehicles", type=parse_positive_int,
                         default=defaults['n'],
                         help="number of cars for each simulation")
    _parser.add_argument("-k", "--packages", type=parse_positive_int,
                         default=defaults['k'],
                         help="number of packages for each simulation")
    _parser.add_argument("-m", "--locations", type=parse_positive_int,
                         default=defaults['m'],
                         help="number of locations in the input map")
    _parser.add_argument("--heuristic", default=defaults['h_name'],
                         choices=["zero", "undelivered", "scaled", "sum"],
                         help="heuristic function to use")
    _parser.add_argument("--vanilla", action='store_true',
                         help="run simulations with vanilla state transitions")
    _parser.add_argument("--bound", type=parse_bound, default=defaults['bound'],
                         help="causes Bounded A* to keep only the best BOUND "
                              "number of successors for any given state; can "
                              "be either a percentage of successors to keep "
                              "(if between 0 and 1, both exclusive), or the "
                              "maximum number of successors to keep (if an "
                              "integer 1 or greater); if 0 or less, keep all "
                              "successors, like regular A*")
    _parser.add_argument("--k-limit", type=parse_positive_int,
                         default=defaults['k_limit'],
                         help="causes Local Beam Search to consider only the "
                              "best (K_LIMIT - 1) successors of any given "
                              "state at each level of recursion")

    # Parse command line arguments.
    _args = _parser.parse_args()
    _verbose = _args.verbose
    _a_star = _args.a_star
    _bounded_a_star = _args.bounded_a_star
    _local_beam = _args.local_beam
    _num_sims = _args.num_sims
    _n = _args.vehicles
    _k = _args.packages
    _m = _args.locations
    _h_name = _args.heuristic
    _h = heuristics[_h_name]
    _state_type = 'VanillaState' if _args.vanilla else 'State'
    _bound = _args.bound
    _k_limit = _args.k_limit

    if not _a_star and not _bounded_a_star and not _local_beam:
        raise _parser.error("at least one of -a, -b, or -l must be given")

    if _a_star:
        _alg = "a_star"
    elif _bounded_a_star:
        _alg = "bounded_astar"
    elif _local_beam:
        _alg = "local_beam"
    else:
        raise _parser.error("at least one of -a, -b, or -l must be given")

    # Run the simulations and record simulation results.
    _names = get_file_names(_num_sims, _n, _k, _m, _h_name, _state_type,
                            _bound, _k_limit)

    if _verbose and _a_star:
        print("Regular A* simulations.")
    if _a_star:
        data_a_star = a_star_simulations(_n, _k, _m, _h, _num_sims,
                                         _state_type, _verbose)
        data_a_star['h_name'] = _h_name
        utils.dump_json_data(_names['a_star'], data_a_star)
        #utils.plot_results(_names['a_star'], data_a_star)

    if _verbose and _bounded_a_star:
        print("Bounded A* simulations.")
    if _bounded_a_star:
        data_bounded_a_star = bounded_a_star_simulations(_n, _k, _m, _h,
                                                         _num_sims,
                                                         _state_type, _bound,
                                                         _verbose)
        data_bounded_a_star['h_name'] = _h_name
        utils.dump_json_data(_names['bounded_a_star'], data_bounded_a_star)
        # utils.plot_results(_names['bounded_a_star'], data_bounded_a_star)

    if _verbose and _local_beam:
        print("Local Beam Search simulations.")
    if _local_beam:
        data_local_beam = local_beam_simulations(_n, _k, _m, _h, _num_sims,
                                                 _state_type, _k_limit,
                                                 _verbose)
        data_local_beam['h_name'] = _h_name
        utils.dump_json_data(_names['local_beam'], data_local_beam)
        # utils.plot_results(_names['local_beam'], data_local_beam)
