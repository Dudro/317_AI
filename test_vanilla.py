def vanilla_a_star_small_graph(n, h, name='Triangle', num_sols=1):
    """
    Runs Vanilla A* on one of the small graphs defined in graphs.py, and prints
    the resulting data.

    :param n: the number of cars in this problem
    :type n: int
    :param h: the heuristic function that A* will use
    :type h: VanillaState => float
    :param name: the name of the graph. One of 'Triangle', 'OGG', or 'Circle'.
        Default: 'Triangle'.
    :type name: string
    :param num_sols: the number of solutions that should be generated, or -1 if
        all possible solutions should be generated. Default: 1.
    :type num_sols: int
    """
    from search import a_star_any_graph
    import graphs
    if name == 'Triangle':
        print("========== Triangle graph results ==========")
        graph_function = graphs.get_triangle_graph
    elif name == 'OGG':
        print("========== OGG graph results ==========")
        graph_function = graphs.get_ogg_graph
    elif name == 'Circle':
        print("========== Circle graph results ==========")
        graph_function = graphs.get_circle_graph
    else:  # If it's anything else, just go with the default.
        print("Warning! Using Triangle graph due to unrecognized name", name)
        print("========== Triangle graph results ==========")
        graph_function = graphs.get_triangle_graph
    full_map, pairs = graph_function()
    k = len(pairs)
    m = full_map.number_of_nodes()
    print(a_star_any_graph(n, k, m, full_map, pairs, 'VanillaState', h,
                           num_sols))


if __name__ == "__main__":
    from State import VanillaState

    _h = VanillaState.sum_of_estimated_cost_scaled_h
    vanilla_a_star_small_graph(1, _h, name='Triangle', num_sols=1)
    vanilla_a_star_small_graph(2, _h, name='OGG', num_sols=1)
    vanilla_a_star_small_graph(1, _h, name='Circle', num_sols=1)
