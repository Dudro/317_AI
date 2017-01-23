from graphs import *
import matplotlib.pyplot as plt

def show_graph(graph, pairs):
    draw_graph(graph, pairs)
    plt.show()

show_graph(*get_triangle_graph())
show_graph(*get_ogg_graph())
show_graph(*get_circle_graph())

