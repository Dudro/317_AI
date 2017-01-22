import networkx as nx
import matplotlib.pyplot as plt

def get_triangle_graph():
    # Defining small triangle test graph
    triangle_size = 3
    triangle = nx.Graph()

    for i in range(triangle_size):
        triangle.add_node(i)

    triangle.add_edge(0,1, weight=10)
    triangle.add_edge(0,2, weight=30)
    triangle.add_edge(1,2, weight=20)
    
    s1 = 1
    d1 = 2
    s2 = 2
    d2 = 0
    pairs = [(1, 2), (2, 0)]

    return triangle, pairs

def get_og_graph():
    # defining ogg (Original Gangster Graph)
    ogg_size = 9
    ogg = nx.Graph()


    for i in range(ogg_size):
        ogg.add_node(i)
    ogg.add_edge(0,1,weight=20)
    ogg.add_edge(1,8,weight=100)
    ogg.add_edge(1,2,weight=68)
    ogg.add_edge(0,3,weight=14)
    ogg.add_edge(3,4,weight=6)
    ogg.add_edge(4,5,weight=4)
    ogg.add_edge(5,6,weight=30)
    ogg.add_edge(6,0,weight=51)
    ogg.add_edge(0,7,weight=36)
    ogg.add_edge(7,3,weight=15)
    
    s1 = 6
    d1 = 2
    s2 = 3
    d2 = 1
    s3 = 4
    d3 = 5
    pairs = [(6, 2), (3, 1), (4, 5)]

    return ogg, pairs

