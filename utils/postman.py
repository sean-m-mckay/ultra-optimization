import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString


def nodelist_to_gpd(nodes):
    nodes_gdf = gpd.GeoDataFrame(
        nodes.rename(columns={"X": "x", "Y": "y"}), geometry=gpd.points_from_xy(x=nodes.X, y=nodes.Y, crs="EPSG:4326")
    )
    return nodes_gdf.set_index("id")


def construct_graph_for_rpp(nodes, edges):
    g = nx.Graph()

    #Add edge data to graph
    for i, edge in edges.iterrows():
        edge['length'] = edge['distance']
        g.add_edge(edge.iloc[0], edge.iloc[1], **edge.iloc[2:].to_dict())

    #Add node data to graph
    for id, node in nodes.iterrows():
        nx.set_node_attributes(g, {id: node.to_dict()})

    g.graph['crs'] = 'EPSG:4326'
    return nx.MultiDiGraph(g)

def rpp_circuit_to_gpd(circuit, nodes_gdf):
    line_strings = []
    node1s = [] 
    node2s = []
    
    for i in range(0, len(circuit) - 1):
        sid= circuit[i][0]
        eid = circuit[i][1]
        data = circuit[i][3]
        origin_point = nodes_gdf.loc[sid].geometry
        destination_point = nodes_gdf.loc[eid].geometry
        
        line = LineString([origin_point, destination_point])
        line_strings += [line]
        node1s += [sid]
        node2s += [eid]
        datas += [data]
    
    return gpd.GeoDataFrame({'u' : node1s, 'v': node2s, 'geometry': line_strings}, crs="EPSG:4326")
    
def rpp_circuit_to_osmnx_route(circuit):
    shortest_path = [e[0] for e in circuit]
    shortest_path += [circuit[-1][1]]
    return shortest_path
    
def osmnx_route_to_rpp_circuit(path, graph):
    out_circuit = []
    all_edges = set()
    for i in range(0, len(path) - 1):
        new_edge = (path[i], path[i + 1])
        new_edge_data = (new_edge[0], new_edge[1], 0, graph.edges[new_edge[0], new_edge[1], 0])
        if new_edge in all_edges:
            new_edge_data[3]['augmented'] = True
        else:
            all_edges.add(new_edge)
            all_edges.add((new_edge[1], new_edge[0])) #Undirected graph, so we add both directions
        out_circuit += [new_edge_data]  
    return out_circuit

def check_circuit_covers_all_required(circuit, graph):
    all_required = {(edge[0], edge[1]) : 0 for edge in graph.edges(data=True) if edge[2]['required']}

    for e in circuit:
        all_required[(e[0], e[1])] = 1
        all_required[(e[1], e[0])] = 1
    missing_edges = [key for key, val in all_required.items() if val == 0]
    
    return not bool(missing_edges), missing_edges