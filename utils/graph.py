import osmnx as ox
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def clip_osmnx_graph(graph_name, area_name):
    
    place_graph = ox.graph_from_place(graph_name, network_type="walk")
    area_gpd = ox.geocode_to_gdf(area_name)
    nodes, edges = ox.utils_graph.graph_to_gdfs(place_graph)
    clipped_graph = ox.graph_from_gdfs(gpd.clip(nodes, area_gpd), gpd.clip(edges, area_gpd))
    return clipped_graph


def get_osmnx_graph_from_area_bounds(area_name, network_type='all', simplify=True):
    area = ox.geocode_to_gdf('University Endowment Lands')
    geom = box(*area.total_bounds)
    return ox.graph_from_polygon(geom, network_type=network_type, simplify=simplify)


def plot_osmnx_graph(graph):
    # Define node positions data structure (dict) for plotting
    plt.figure(figsize=(8, 6))
    node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in graph.nodes(data=True)}
    nx.draw(graph, pos=node_positions, node_size=10, node_color='black')
    plt.title('Graph Representation of Pacific Spirit Trail', size=15)
    plt.show()