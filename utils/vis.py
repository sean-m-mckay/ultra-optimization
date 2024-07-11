import numpy as np
import pandas as pd
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib import animation as ani
from matplotlib.collections import LineCollection
from functools import partial

def animate_segments_circuit(graph, circuit, scat, line, i):
    x, y, colors = [], [], []
    for edge in circuit[:i]:
        (u, v, _, data) = edge
        x.extend((graph.nodes[u]["x"], graph.nodes[v]["x"]))
        y.extend((graph.nodes[u]["y"], graph.nodes[v]["y"]))
        color = 'r' if data['required'] else 'b'
        color = 'y' if 'augmented' in data else color
        colors.extend(color)

    segments = np.array([x, y]).T.reshape(-1, 2, 2)
    line.set_segments(segments)
    line.set_colors(colors)
    scat.set_offsets(np.array([x, y]).T)
    return (scat, line)

def animate_circuit(graph, circuit, animation_func=animate_segments_circuit):
    plt.figure(figsize=(20,10))
    fig, ax = ox.plot_graph(graph, show=False, figsize=(20, 20))   
    line = LineCollection([])
    ax.add_collection(line)
    #line.set_segments([])
    x = (graph.nodes[circuit[0][0]]["x"], graph.nodes[circuit[-1][0]]["x"])
    y = (graph.nodes[circuit[0][0]]["y"], graph.nodes[circuit[-1][0]]["y"])
    scat = ax.scatter(x, y, s=30, c="r", alpha=0.5)
    return ani.FuncAnimation(fig, partial(animation_func, graph, circuit, scat, line), frames=range(1, len(circuit)))
