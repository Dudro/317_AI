if __name__ == "__main__":
    import networkx as nx
    import matplotlib.pyplot as plt
    giii_size = 7
    giii = nx.Graph()

    for i in range(giii_size):
        giii.add_node(i)

    giii.add_edge(0,1, weight=10)
    giii.add_edge(0,2, weight=20)
    giii.add_edge(1,2, weight=10)
    giii.add_edge(3,4, weight=15)
    giii.add_edge(1,4, weight=25)
    giii.add_edge(0,3, weight=15)
    giii.add_edge(1,5, weight=10)
    giii.add_edge(2,6, weight=15)
    giii.add_edge(3,6, weight=20)
    giii.add_edge(5,6, weight=10)

#pos = nx.circular_layout(giii, dim=2, scale=1)

#    nx.draw_networkx_nodes(giii, pos, with_labels=True)
#    nx.draw_networkx_edges(giii, pos, giii.edges())
#    nx.draw_networkx_labels(giii, pos)
    
#    plt.show()
    '''
    m = 20

    G = nx.random_geometric_graph(m, 0.25)

    pos = nx.get_node_attributes(G, 'pos')

    dmin = 1
    ncenter = 0
    for n in pos:
            x, y = pos[n]
            d = (x - 0.5)**2 + (y-0.5)**2
            if d  < dmin:
                ncenter = n
                dmin = d

    p = nx.single_source_shortest_path_length(G, ncenter)

    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=p.keys(),
            node_size = 80,
            node_color = p.values(),
            cmap = plt.cm.Reds_r)

    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    plt.show()
    '''

    garage = 0
    s1 = 1
    d1 = 3
    s2 = 4
    d2 = 2
    important_nodes = [0, 1, 2, 3, 4]

    paths = nx.floyd_warshall(giii)
    reduced_graph = nx.Graph()
    
    for i in important_nodes:
        reduced_graph.add_node(i)

    for i in important_nodes:
        for k, v in paths[i].items():
            if k in important_nodes:
                reduced_graph.add_edge(i, k, weight=v) 

    pos = nx.circular_layout(reduced_graph, 2, 1)

    nx.draw_networkx_nodes(reduced_graph, pos, with_labels=True)
    nx.draw_networkx_edges(reduced_graph, pos, reduced_graph.edges())
    nx.draw_networkx_labels(reduced_graph, pos)
    
    plt.show()

