from graphs import *
import matplotlib.pyplot as plt
import networkx as nx
from World import World


def show_graph(graph, pairs=None, garage=0):
    """
    Draws the given graph using graphs.draw_graph, and then shows the
    Matplotlib plot.
    :param graph: the graph to draw
    :type graph: NetworkX graph
    :param pairs: source-destination pairs. Default: None.
    :type pairs: list((int, int))
    :param garage: the garage node. Default: 0.
    :type garage: int
    """
    draw_graph(graph, pairs, garage)
    plt.show()


def test_graphs():
    """
    Tests the hardcoded graphs in graphs.py, making sure they are constructed
    as expected.
    """
    # Test the triangle graph.
    graph, pairs = get_triangle_graph()
    show_graph(graph, pairs)
    n = 1
    k = len(pairs)
    m = len(graph.nodes())

    world = World(n, k, m, graph, pairs)
    print("Original map:")
    print(nx.to_dict_of_dicts(graph))
    print("Important vertices:")
    print(world.get_important_vertices())
    world.process_map()
    if 10 != world.get_edge_cost(0, 1):
        print("error")
    if 10 != world.get_edge_cost(1, 0):
        print("error")
    if 20 != world.get_edge_cost(1, 2):
        print("error")
    if 20 != world.get_edge_cost(2, 1):
        print("error")
    if 30 != world.get_edge_cost(0, 2):
        print("error")
    if 30 != world.get_edge_cost(2, 0):
        print("error")
    print("Reduced map:")
    print(nx.to_dict_of_dicts(world.get_reduced_map()))

    # Test the OGG graph.
    graph, pairs = get_ogg_graph()
    show_graph(graph, pairs)
    n = 3
    k = len(pairs)
    m = len(graph.nodes())

    world = World(n, k, m, graph, pairs)
    print("Original map:")
    print(nx.to_dict_of_dicts(graph))
    print("Important vertices: ")
    print(world.get_important_vertices())
    world.process_map()
    if 20 != world.get_edge_cost(0, 1):
        print("error")
    if 14 != world.get_edge_cost(0, 3):
        print("error")
    if 30 != world.get_edge_cost(5, 6):
        print("error")
    if 4 != world.get_edge_cost(5, 4):
        print("error")
    if 68 != world.get_edge_cost(2, 1):
        print("error")
    if 6 != world.get_edge_cost(4, 3):
        print("error")
    print("Reduced map:")
    print(nx.to_dict_of_dicts(world.get_reduced_map()))

    # Test the circle graph.
    graph, pairs = get_circle_graph()
    show_graph(graph, pairs)
    n = 2
    k = len(pairs)
    m = len(graph.nodes())

    world = World(n, k, m, graph, pairs)
    print("Original map:")
    print(nx.to_dict_of_dicts(graph))
    print("Important vertices:")
    print(world.get_important_vertices())
    world.process_map()
    if 5 != world.get_edge_cost(0, 1):
        print("error")
    if 10 != world.get_edge_cost(0, 2):
        print("error")
    if 15 != world.get_edge_cost(0, 3):
        print("error")
    if 20 != world.get_edge_cost(0, 4):
        print("error")
    if 25 != world.get_edge_cost(0, 5):
        print("error")
    if 20 != world.get_edge_cost(0, 6):
        print("error")
    if 15 != world.get_edge_cost(0, 7):
        print("error")
    if 10 != world.get_edge_cost(0, 8):
        print("error")
    if 5 != world.get_edge_cost(0, 9):
        print("error")
    print("Reduced map:")
    print(nx.to_dict_of_dicts(world.get_reduced_map()))

    # Test one random graph.
    graph, pairs = get_random_graph(3, 10, seed=5)
    show_graph(graph, pairs)


if __name__ == "__main__":
    test_graphs()
