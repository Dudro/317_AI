if __name__ == "__main__":
    import networkx as nx
    import matplotlib.pyplot as plt
    import graphs
    import World

    G, pairs = graphs.get_triangle_graph()
    N = 1
    K = len(pairs)
    M = nx.number_of_nodes(G)

    world = World.World(N, K, M, G, pairs)
    print("Original graph: \n", nx.to_dict_of_dicts(G))
    print("Important nodes: \n", world.get_important_nodes())
    world.process_graph()
    if 10 != world.get_edge_cost(0,1):
        print("error")
    if 10 != world.get_edge_cost(1,0):
        print("error")
    if 20 != world.get_edge_cost(1,2):
        print("error")
    if 20 != world.get_edge_cost(2,1):
        print("error")
    if 30 != world.get_edge_cost(0,2):
        print("error")
    if 30 != world.get_edge_cost(2,0):
        print("error")



    G, pairs = graphs.get_og_graph()
    N = 3
    K = len(pairs)
    M = nx.number_of_nodes(G)

    world = World.World(N, K, M, G, pairs)
    print("Original graph: \n", nx.to_dict_of_dicts(G))
    print("Important nodes: \n", world.get_important_nodes())
    world.process_graph()
    if 20 != world.get_edge_cost(0,1):
        print("error")
    if 14 != world.get_edge_cost(0,3):
        print("error")
    if 30 != world.get_edge_cost(5,6):
        print("error")
    if 4 != world.get_edge_cost(5,4):
        print("error")
    if 68 != world.get_edge_cost(2,1):
        print("error")
    if 6 != world.get_edge_cost(4,3):
        print("error")
    print(nx.to_dict_of_dicts(world._reduced_graph))
