from localbeam import local_beam_search
from test_astar import *

# Generate (lazily) every solution (path) from Arad to Bucharest.
print("Local Beam Search")
for sol, count in local_beam_search(GraphState(2, 0, [2]), at_bucharest,
                                    trans_op, f, 5):
    print(count, sol.get_cost_so_far(), solution.get_path_so_far())
