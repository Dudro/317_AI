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
        self._N = n  # Python style says parameters should be lowercase...
        self._K = k  # ... but internally, the true parameters can all be...
        self._M = m  # ... uppercase, just like in the problem description.
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
        """
        Returns the vertex index of the garage.
        :rtype: int
        """
        return self._G

    def get_number_of_cars(self):
        """
        Returns the total number of cars.
        :rtype: int
        """
        return self._N

    def get_important_vertices(self):
        """
        Returns a list of the important vertices of the original map. These
        correspond to vertices that are a package source and/or a package
        destination and/or or the garage. The resulting list is cached to speed
        up future invocations.
        :rtype: list(int)
        """
        if self._important_vertices is None:
            important = [self._G]  # Garage is always important.
            for src, dest in self._source_dest_pairs:
                if src not in important:
                    important.append(src)
                if dest not in important:
                    important.append(dest)
            self._important_vertices = important
            return important
        else:
            return self._important_vertices

    def get_package_source(self, pkg_id):
        """
        Returns the source vertex of the given package.
        :param pkg_id: the package
        :type pkg_id: int
        :rtype: int
        """
        src, _ = self._source_dest_pairs[pkg_id]
        return src

    def get_package_dest(self, pkg_id):
        """
        Returns the destination vertex of the given package.
        :param pkg_id: the package
        :type pkg_id: int
        :rtype: int
        """
        _, dest = self._source_dest_pairs[pkg_id]
        return dest

    def process_map(self):
        """
        Processes the full map into a reduced map containing only the important
        vertices of the original map. Makes the reduced map a complete graph,
        where each vertex is connected to each other vertex by an edge weighted
        according to the cost of the shortest (i.e. lowest cost) path between
        them.
        """
        # Compute all pairs of paths and their cost.
        paths = nx.floyd_warshall(self._full_map)

        # Create the complete reduced map.
        self.get_important_vertices()
        self._reduced_map = nx.Graph()
        self._reduced_map.add_nodes_from(self._important_vertices)
        for i in self._important_vertices:
            for k, v in paths[i].items():
                if k in self._important_vertices:
                    self._reduced_map.add_edge(i, k, weight=v)

        self._reduced_map_as_dict = nx.to_dict_of_dicts(self._reduced_map)

    def get_edge_cost(self, location, goal):
        """
        Returns the edge cost between any two vertices in the reduced map. The
        reduced map is precomputed if needed.
        :param location: the source vertex
        :param goal: the destination vertex
        :rtype: float
        """
        if self._reduced_map is None:
            self.process_map()
        return self._reduced_map_as_dict[location][goal]['weight']

    def get_reduced_map(self):
        """
        Returns the reduced map. The reduced map is precomputed if needed.
        :rtype: NetworkX Graph
        """
        if self._reduced_map is None:
            self.process_map()
        return self._reduced_map

    def get_shortest_path(self, source, dest):
        """
        Returns the shortest path between any two vertices in the original map.
        :param source: the source vertex
        :param dest: the destination vertex
        :rtype: list(int)
        """
        return self._all_pairs_shortest_paths[source][dest]

    def get_package_cost(self, package):
        """
        Returns the edge cost between the given package's source and
        destination in the reduced map.
        :param package: the package
        :type package: int
        :rtype: float
        """
        return self.get_edge_cost(*self._source_dest_pairs[package])
