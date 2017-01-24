import networkx as nx
import random as rand

class World:
    """
    A World encompasses an instance of the problem.
    """
    def __init__(self, N, K, M, full_map, source_dest_pairs=None, G=0):
        """
        :param N: the number of cars
        :type N: int
        :param K: the number of packages. Should equal
            len(source_dest_pairs)
        :type K: int
        :param M: the total number of vertices in the full map. Should
            equal len(full_map.nodes())
        :param full_map: the full map with K source and K destination
            vertices and 1 garage vertex (not necessarily distinct) and
            exactly M vertices in total
        :type full_map: NetworkX graph
        :param source_dest_pairs: the source and destination pairs for each
            package, given in package order. If None, pairs will be
            generated randomly. Default: None.
        :type source_dest_pairs: list((int, int))
        :param G: the garage node. Default: 0.
        :type G: int
        """
        self._N = N
        self._K = K
        self._M = M
        self._full_map = full_map
        self._reduced_map = None
        self._reduced_map_as_dict = None
        if source_dest_pairs is None:
            self._source_dest_pairs = generate_random_package_routes()
        else:
            self._source_dest_pairs = source_dest_pairs
        self._important_vertices = None
        self._G = G

    def generate_random_package_routes(self):
        pairs = []
        for i in range(self._K):
            src = rand.randint(0, self._M-1)
            dest = src
            while dest == src:
                dest = rand.randint(0, self._M-1)
            pairs.append((src, dest))
        return pairs

    def get_important_vertices(self):
        if self._important_vertices is None:
            important = []
            for i in range(self._K):
                if self._source_dest_pairs[i][0] not in important:
                    important.append(self._source_dest_pairs[i][0])
                if self._source_dest_pairs[i][1] not in important:
                    important.append(self._source_dest_pairs[i][1])
            if self._G not in important: # add garage
                important.append(self._G) 
            self._important_vertices = important
            return important
        else:
            return self._important_vertices

    def get_package_source(pkg_id):
	pkg = self._source_dest_pairs[pkg_id]
	return pkg[0]
	
    def get_package_dest(pkg_id):
	pkg = self._source_dest_pairs[pkg_id]
	return pkg[1]		

    def get_important_nodes(self):
        important = []
        for i in range(self._K):
            if self._source_dest_pairs[i][0] not in important:
                important.append(self._source_dest_pairs[i][0])
            if self._source_dest_pairs[i][1] not in important:
                important.append(self._source_dest_pairs[i][1])
        if self._G not in important: # add garage
            important.append(self._G) 
        return important

    def process_map(self):
        # Retrieve all pairs paths and distances
        self._important_vertices = self.get_important_vertices() 
        paths = nx.floyd_warshall(self._full_map)

        self._reduced_map = nx.Graph()
        self._reduced_map.add_nodes_from(self._important_vertices)
        for i in self._important_vertices:
            for k, v in paths[i].items():
                if k in self._important_vertices:
                    self._reduced_map.add_edge(i, k, weight=v)

        self._reduced_map_as_dict = nx.to_dict_of_dicts(self._reduced_map)

    def get_edge_cost(self, curr_loc, goal):
        if curr_loc >= self._M or goal >= self._M:
            print("error: index out of bounds!")
            return None
        if (curr_loc not in self._important_vertices) \
                or (goal not in self._important_vertices):
            print("error: illegal node!")
            return None
        return self._reduced_map_as_dict[curr_loc][goal]['weight']

    def get_reduced_map(self):
        if self._reduced_map is None:
            process_map()
        return self._reduced_map

