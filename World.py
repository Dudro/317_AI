import networkx as nx
import random as rand
class World:

    def __init__(self, N, K, M, full_graph, source_dest_pairs=None):
        """
        :param source_dest_pairs:
        :type source_dest_pairs: list((int, int))
        """
        self._full_graph = full_graph
        self._reduced_graph = None
        self._graph_as_dict = None
        self._G = 0
        self._N = N
        self._K = K
        self._M = M
        if source_dest_pairs is None:
            self._source_dest_pairs = generate_package_routes()
        else:
            self._source_dest_pairs = source_dest_pairs
        self._important_nodes = []

    def generate_package_routes(self):
        pairs = []
        for i in range(K):
            src = rand.randint(0, self._M-1)
            dest = src
            while dest == src:
                dest = rand.randint(0, self._M-1)
            pairs.append((src, dest))
        return pairs

    def get_important_nodes(self):
        important = []
        for i in range(self._K):
            if self._source_dest_pairs[i][0] not in important:
                important.append(self._source_dest_pairs[i][0])
            if self._source_dest_pairs[i][1] not in important:
                important.append(self._source_dest_pairs[i][1])
        if 0 not in important: # add garage
            important.append(0) 
        return important

    def process_graph(self):
        # Retrieve all pairs paths and distances
        self._important_nodes = self.get_important_nodes() 
        paths = nx.floyd_warshall(self._full_graph)

        self._reduced_graph = nx.Graph()
        for i in self._important_nodes:
            self._reduced_graph.add_node(i)
        for i in self._important_nodes:
            for k, v in paths[i].items():
                if k in self._important_nodes:
                    self._reduced_graph.add_edge(i, k, weight=v)

        self._graph_as_dict = nx.to_dict_of_dicts(self._reduced_graph)

    def get_edge_cost(self, curr_loc, goal):
        if curr_loc >= self._M or goal >= self._M:
            print("error: index out of bounds!")
            return None
        if curr_loc not in self._important_nodes or goal not in self._important_nodes:
            print("error: illegal node!")
            return None
        return self._graph_as_dict[curr_loc][goal]['weight']



