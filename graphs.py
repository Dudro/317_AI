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
    pairs = [(s1, d1), (s2, d2), (s3, d3)]

    return ogg, pairs

def get_circle_graph():
    size = 10
    circle = nx.Graph()

    for i in range(size):
        circle.add_node(i)
    circle.add_edge(0,1,weight=5)
    circle.add_edge(1,2,weight=5)
    circle.add_edge(2,3,weight=5)
    circle.add_edge(3,4,weight=5)
    circle.add_edge(4,5,weight=5)
    circle.add_edge(5,6,weight=5)
    circle.add_edge(6,7,weight=5)
    circle.add_edge(7,8,weight=5)
    circle.add_edge(8,9,weight=5)
    circle.add_edge(9,0,weight=5)

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

    pairs = [(s1, d1), (s2, d2), (s3, d3), (s4, d4), (s5, d5), \
             (s6, d6), (s7, d7), (s8, d8), (s9, d9), (s10, d10)]
   
    return circle, pairs
