from astar import astar
import networkx as nx

romania = nx.Graph()
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

class Graph_State:
    def __init__(self, vertex, cost_so_far, path_so_far):
        self._vertex = vertex
        self._cost_so_far = cost_so_far
        self._path_so_far = path_so_far

    def get_vertex(self):
        return self._vertex

    def get_cost_so_far(self):
        return self._cost_so_far

    def get_path_so_far(self):
        return self._path_so_far

def at_bucharest(state):
    return state.get_vertex() == 8

def trans_op(state):
    vertex = state.get_vertex()
    romania.node[vertex]['visited'] = True
    neighbors = [v for v in romania.neighbors(vertex) \
            if romania.node[v]['visited'] == False]
    successors = []
    for neighbor in neighbors:
        new_cost = state.get_cost_so_far() + \
                romania.edge[vertex][neighbor]['weight']
        new_path = state.get_path_so_far()[:]
        new_path.append(neighbor)
        successors.append(Graph_State(neighbor, new_cost, new_path))
    return successors


straight_line_distance_bucharest = {}
straight_line_distance_bucharest[0] = 380
straight_line_distance_bucharest[1] = 374
straight_line_distance_bucharest[2] = 366
straight_line_distance_bucharest[3] = 329
straight_line_distance_bucharest[4] = 253
straight_line_distance_bucharest[5] = 193
straight_line_distance_bucharest[6] = 176
straight_line_distance_bucharest[7] = 98
straight_line_distance_bucharest[8] = 0
straight_line_distance_bucharest[9] = 244
straight_line_distance_bucharest[10] = 241
straight_line_distance_bucharest[11] = 242
straight_line_distance_bucharest[12] = 160
straight_line_distance_bucharest[13] = 77
straight_line_distance_bucharest[14] = 161
straight_line_distance_bucharest[15] = 151
straight_line_distance_bucharest[16] = 80
straight_line_distance_bucharest[17] = 199
straight_line_distance_bucharest[18] = 226
straight_line_distance_bucharest[19] = 234

def f(state):
    return state.get_cost_so_far() + \
            straight_line_distance_bucharest[state.get_vertex()]

for solution in astar(Graph_State(2, 0, [2]), at_bucharest, trans_op, f):
    print solution.get_cost_so_far(), solution.get_path_so_far()

