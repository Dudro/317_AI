import networkx as nx
from graphs import generate_random_package_routes


class World:
    """
    A World encompasses an instance of the problem.
    """

    def __init__(self, n, k, m, full_map, source_dest_pairs=None, g=0):
        """
        :param n: the number of cars. Should be positive.
        :type n: int
        :param k: the number of packages. Should equal
            len(source_dest_pairs)
        :type k: int
        :param m: the total number of vertices in the full map. Should
            equal len(full_map.nodes())
        :type m: int
        :param full_map: the full map with K source and K destination
            vertices and 1 garage vertex (not necessarily distinct) and
            exactly M vertices in total
        :type full_map: NetworkX graph
        :param source_dest_pairs: the source and destination pairs for each
            package, given in package order. If None, pairs will be
            generated randomly. Default: None.
        :type source_dest_pairs: list((int, int))
        :param g: the garage node. Default: 0.
        :type g: int
        """
        self._N = n
        self._K = k
        self._M = m
        self._full_map = full_map
        self._all_pairs_shortest_paths = nx.all_pairs_shortest_path(full_map)
        self._reduced_map = None
        self._reduced_map_as_dict = None
        if source_dest_pairs is None:
            self._source_dest_pairs = generate_random_package_routes(k, m)
        else:
            self._source_dest_pairs = source_dest_pairs
        self._important_vertices = None
        self._G = g

    def get_garage(self):
        return self._G

    def get_number_of_cars(self):
        return self._N

    def get_important_vertices(self):
        if self._important_vertices is None:
            important = []
            for src, dest in self._source_dest_pairs:
                if src not in important:
                    important.append(src)
                if dest not in important:
                    important.append(dest)
            if self._G not in important:  # add garage
                important.append(self._G)
            self._important_vertices = important
            return important
        else:
            return self._important_vertices

    def get_package_source(self, pkg_id):
        src, _ = self._source_dest_pairs[pkg_id]
        return src

    def get_package_dest(self, pkg_id):
        _, dest = self._source_dest_pairs[pkg_id]
        return dest

    def process_map(self):
        # Retrieve all pairs paths and distances
        self.get_important_vertices()
        paths = nx.floyd_warshall(self._full_map)

        self._reduced_map = nx.Graph()
        self._reduced_map.add_nodes_from(self._important_vertices)
        for i in self._important_vertices:
            for k, v in paths[i].items():
                if k in self._important_vertices:
                    self._reduced_map.add_edge(i, k, weight=v)

        self._reduced_map_as_dict = nx.to_dict_of_dicts(self._reduced_map)

    def get_edge_cost(self, curr_loc, goal):
        return self._reduced_map_as_dict[curr_loc][goal]['weight']

    def get_reduced_map(self):
        if self._reduced_map is None:
            self.process_map()
        return self._reduced_map

    def get_shortest_path(self, source, dest):
        return self._all_pairs_shortest_paths[source][dest]

    def get_package_cost(self, package):
        """
        Returns the edge cost between the given package's source and
        destination in the map.
        """
        return self.get_edge_cost(*self._source_dest_pairs[package])
