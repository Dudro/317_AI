from localbeam import local_beam_search
from test_astar import *

if __name__ == "__main__":
    # Generate (lazily) every solution (path) from Arad to Bucharest.
    print("Local Beam Search")
    for sol, count in local_beam_search(GraphState(2, 0, [2]), at_bucharest,
                                        trans_op, f):
        print(count, sol.get_cost_so_far(), sol.get_path_so_far())
