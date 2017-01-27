from graphs import *
import matplotlib.pyplot as plt
import networkx as nx
import graphs
from World import World


def show_graph(graph, pairs):
    draw_graph(graph, pairs)
    plt.show()


def test_graphs():
    graph, pairs = graphs.get_triangle_graph()
    N = 1
    K = len(pairs)
    M = len(graph.nodes())
    # show_graph(graph, pairs)

    world = World(N, K, M, graph, pairs)
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
    # show_graph(world.get_reduced_map(), pairs)

    graph, pairs = graphs.get_og_graph()
    N = 3
    K = len(pairs)
    M = len(graph.nodes())
    show_graph(graph, pairs)

    world = World(N, K, M, graph, pairs)
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
    # show_graph(world.get_reduced_map(), pairs)

    graph, pairs = graphs.get_circle_graph()
    N = 2
    K = len(pairs)
    M = len(graph.nodes())
    # show_graph(graph, pairs)

    world = World(N, K, M, graph, pairs)
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
    # show_graph(world.get_reduced_map(), pairs)

    graph, pairs = get_random_graph(10, 2, 5)
    show_graph(graph, pairs)

test_graphs()


