import networkx as nx
from networkx.drawing.layout import circular_layout
import matplotlib.pyplot as plt
import random
import math

def draw_graph(graph, source_dest_pairs=None, garage=0):
    """
    Draw the given graph using Matplotlib.

    :param graph: the graph to draw
    :type graph: NetworkX graph
    :param source_dest_pairs: the source and destination pairs for each
        package, given in package order. If None, nodes are not annotated
        with source and destination labels. Default: None.
    :type source_dest_pairs: list((int, int))
    :param garage: the garage node. Default: 0.
    :type garage: int
    """
    layout = circular_layout(graph)
    nx.draw_networkx(graph, pos=layout, node_color='w')
    n_labels = dict((i, []) for i in graph.nodes())
    n_labels[garage].append('G ')
    if source_dest_pairs is not None:
        i = 0
        for (src, dest) in source_dest_pairs:
            n_labels[src].append('s%d ' % i)
            n_labels[dest].append('d%d ' % i)
            i += 1
        for i in graph.nodes():
            x, y = layout[i]
            label_parts = n_labels[i]
            if label_parts:
                label = ''.join(label_parts).strip()
                y_scale = 1.20  # 1.20 seems to work well.
                x_scale = 1.17 + 1.05 * len(label) / 100.0  # 1.17 works here.
                plt.text(x * x_scale, y * y_scale, s=label, ha='center',
                         va='center')
    e_labels = dict(((v1, v2), weight) for (v1, v2, weight) in
                    graph.edges(data='weight'))
    nx.draw_networkx_edge_labels(graph, pos=layout, edge_labels=e_labels)

def get_triangle_graph():
    """
    Return a small triangle graph with source-destination 
    pairs for testing.
    :rtype: Graph, list((int,int))
    """
    triangle_size = 3
    triangle = nx.Graph()

    for i in range(triangle_size):
        triangle.add_node(i)

    triangle.add_edge(0, 1, weight=10)
    triangle.add_edge(0, 2, weight=30)
    triangle.add_edge(1, 2, weight=20)

    s1 = 1
    d1 = 2
    s2 = 2
    d2 = 0
    pairs = [(s1, d1), (s2, d2)]

    return triangle, pairs


def get_og_graph():
    """
    Return ogg (the Original Gangster Graph) with source-destination pairs
    for testing.
    :rtype: Graph, list((int,int))
    """
    ogg_size = 9
    ogg = nx.Graph()

    ogg.add_nodes_from([i for i in range(ogg_size)])

    ogg.add_edge(0, 1, weight=20)
    ogg.add_edge(1, 8, weight=100)
    ogg.add_edge(1, 2, weight=68)
    ogg.add_edge(0, 3, weight=14)
    ogg.add_edge(3, 4, weight=6)
    ogg.add_edge(4, 5, weight=4)
    ogg.add_edge(5, 6, weight=30)
    ogg.add_edge(6, 0, weight=51)
    ogg.add_edge(0, 7, weight=36)
    ogg.add_edge(7, 3, weight=15)

    s1 = 6
    d1 = 2
    s2 = 3
    d2 = 1
    s3 = 4
    d3 = 5
    pairs = [(s1, d1), (s2, d2), (s3, d3)]

    return ogg, pairs


def get_circle_graph():
    """
    Return a circular graph of size 10 with 
    source-destination pairs for testing.
    :rtype: Graph, list((int,int))
    """
    size = 10
    circle = nx.Graph()
    for i in range(size):
        circle.add_node(i)
    circle.add_edge(0, 1, weight=5)
    circle.add_edge(1, 2, weight=5)
    circle.add_edge(2, 3, weight=5)
    circle.add_edge(3, 4, weight=5)
    circle.add_edge(4, 5, weight=5)
    circle.add_edge(5, 6, weight=5)
    circle.add_edge(6, 7, weight=5)
    circle.add_edge(7, 8, weight=5)
    circle.add_edge(8, 9, weight=5)
    circle.add_edge(9, 0, weight=5)

    s1 = 0
    d1 = 1
    s2 = 1
    d2 = 2
    s3 = 2
    d3 = 3
    s4 = 3
    d4 = 4
    s5 = 4
    d5 = 5
    s6 = 5
    d6 = 6
    s7 = 6
    d7 = 7
    s8 = 7
    d8 = 8
    s9 = 8
    d9 = 9
    s10 = 9
    d10 = 0

    pairs = [(s1, d1), (s2, d2), (s3, d3), (s4, d4), (s5, d5),
             (s6, d6), (s7, d7), (s8, d8), (s9, d9), (s10, d10)]
    return circle, pairs

def get_random_graph(k, m, seed=None):
    """
    :param n: The number of
    :param k: The number of packages for the problem.
    :type k: int
    :param m: The number of vertices to generate the graph with.
    :type m: int
    :param seed: A seed for the random problem generation.
    :type seed: int
    :return: a random ugly graph
    """
    if seed != None:
        random.seed(seed)
    graph = nx.dense_gnm_random_graph(
            m, 
            random.randint(math.ceil(m*0.75), math.floor(m*1.25)), 
            seed=seed)
    connected_components = nx.connected_components(graph)
    first_node = list(next(connected_components))[0]
    for list_of_nodes in connected_components:
        graph.add_edge(first_node,list(list_of_nodes)[0])
    edges = graph.edges()
    for edge in edges:
        graph[edge[0]][edge[1]]['weight'] = random.randint(0,1000)
    pairs = []
    i = 0
    while i < k:
        s = random.randint(0, m-1)
        d = random.randint(0, m-1)
        while d == s :
            d = random.randint(0, m-1)
        if [s,d] not in pairs:
            pairs.append([s,d])
            i = i + 1

    return graph, pairs

