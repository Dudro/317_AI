from astar import a_star
import networkx as nx

romania = nx.Graph()  # The map of Romania, as shown in AIMA, Ed. 3.
romania.add_nodes_from(range(0, 20), visited=False)
romania.add_edge(0, 1, weight=71)
romania.add_edge(0, 4, weight=151)
romania.add_edge(1, 2, weight=75)
romania.add_edge(2, 3, weight=118)
romania.add_edge(2, 4, weight=140)
romania.add_edge(3, 9, weight=111)
romania.add_edge(4, 5, weight=80)
romania.add_edge(4, 6, weight=99)
romania.add_edge(5, 7, weight=97)
romania.add_edge(5, 12, weight=146)
romania.add_edge(6, 8, weight=211)
romania.add_edge(7, 8, weight=101)
romania.add_edge(7, 12, weight=138)
romania.add_edge(8, 13, weight=90)
romania.add_edge(8, 16, weight=85)
romania.add_edge(9, 10, weight=70)
romania.add_edge(10, 11, weight=75)
romania.add_edge(11, 12, weight=120)
romania.add_edge(14, 15, weight=86)
romania.add_edge(15, 16, weight=98)
romania.add_edge(16, 17, weight=142)
romania.add_edge(17, 18, weight=92)
romania.add_edge(18, 19, weight=87)


class GraphState:  # This is generic and could apply to other graphs, too.
    """
    A GraphState consists of a vertex index in a graph, as well as the
    path and the cost of the path that led from the initial state to the
    this one.
    """

    def __init__(self, vertex, cost_so_far, path_so_far):
        """
        :param vertex: a vertex in a graph
        :type vertex: int
        :param cost_so_far: the total cost so far from the initial state to
            this state
        :type cost_so_far: numeric
        :param path_so_far: the path taken from the initial state to reach
            this state
        :type path_so_far: list(int)
        """
        self._vertex = vertex
        self._cost_so_far = cost_so_far
        self._path_so_far = path_so_far

    def get_vertex(self):
        return self._vertex

    def get_cost_so_far(self):
        return self._cost_so_far

    def get_path_so_far(self):
        return self._path_so_far


def at_bucharest(state):  # Specific goal test for romania map.
    return state.get_vertex() == 8


def trans_op(state):  # Semi-specific to romania map.
    """
    Given a GraphState, returns the neighboring map vertices as GraphStates,
    with updated cost and path so far values. Marks the given state as visited,
    so as to avoid introducing cycles into the search space.

    :param state: the state to which to apply the transition function
    :type state: GraphState
    :rtype: list(GraphState)
    """
    vertex = state.get_vertex()
    romania.node[vertex]['visited'] = True
    neighbors = [v for v in romania.neighbors(vertex)
                 if not romania.node[v]['visited']]
    successors = []
    for neighbor in neighbors:
        new_cost = state.get_cost_so_far() + \
                   romania.edge[vertex][neighbor]['weight']
        new_path = state.get_path_so_far()[:]
        new_path.append(neighbor)
        successors.append(GraphState(neighbor, new_cost, new_path))
    return successors


# Values defining the heuristic function. Specific to romania map.
straight_line_distance_bucharest = {
    0: 380,
    1: 374,
    2: 366,
    3: 329,
    4: 253,
    5: 193,
    6: 176,
    7: 98,
    8: 0,
    9: 244,
    10: 241,
    11: 242,
    12: 160,
    13: 77,
    14: 161,
    15: 151,
    16: 80,
    17: 199,
    18: 226,
    19: 234
}


def f(state):  # Specific to romania. Calculates f(x) = g(x) + h(x) for A*.
    return state.get_cost_so_far() + \
           straight_line_distance_bucharest[state.get_vertex()]


# Generate (lazily) every solution (path) from Arad to Bucharest, with the
# optimal (shortest) path being part of the first solution.
for solution in a_star(GraphState(2, 0, [2]), at_bucharest, trans_op, f):
    print(solution.get_cost_so_far(), solution.get_path_so_far())
