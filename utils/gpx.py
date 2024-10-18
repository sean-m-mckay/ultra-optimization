import gpxpy
import osmnx as ox
import networkx as nx
import pandas as pd

def split_gpx(gpx_path):
    map = open(gpx_path, "r")
    data_raw = map.read()
    
    header = data_raw.split("<trkseg>")[0] + "<trkseg>"
    footer = "</trkseg>" + data_raw.split("</trkseg>")[1]
    data = data_raw.split("<trkseg>")[1].split("</trkseg>")[0]
    data = data_raw.split("<trkpt")[1:]
    
    i = 0
    files = 1
    out = []
    while i < len(data):
        coord = "<trkpt" + data[i]
        out.append(coord)
        i += 1
        if i % 400 == 0 or (i == len(data) - 1):
            file_out = header + "".join(out) + footer
            with open(file_name.split("\.")[0] + "_" + str(files) + ".gpx", 'w') as out_file:
                out_file.write(file_out)
            out = []
            files += 1
    return True
    
        
    

def load_gpx_points(gpx_path):
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)
    
    # Convert to a dataframe one point at a time.
    points = []
    for segment in gpx.tracks[0].segments:
        for p in segment.points:
            points.append({
                'time': p.time,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'elevation': p.elevation,
            })
    route_df = pd.DataFrame.from_records(points)
    return route_df


def gpx_points_to_osmnx_route(points_df, graph, threshold_dist):

    route_list = []
    curr_route = []
    curr_node, last_node = None, None
    for id, point in points_df.iterrows():
        curr_point = (point.longitude, point.latitude)
        cand_node, dist_to_node = ox.nearest_nodes(graph, X=curr_point[0], Y=curr_point[1], return_dist=True)
    
        if dist_to_node < threshold_dist:
            if cand_node != curr_node:
                last_node = curr_node
                curr_node = cand_node
                
        if curr_node and last_node and last_node != curr_node:
            if graph.has_edge(last_node, curr_node):
                route = nx.shortest_path(graph, last_node, curr_node, weight='length')    
                curr_route += route[1:] if curr_route else route #Remove the origin node as it's a duplicate of the previous destination node
            else:
                route = ox.routing.shortest_path(graph, [last_node], [curr_node], weight='length')
                print(f"No direct route between nodes {last_node} and {curr_node}, adding path {route}")
                if route:
                    curr_route += route[0][1:] if curr_route else route[0]
                else:
                    #Start a new route
                    print(f"No route between nodes #{last_node} and #{curr_node}")
                    if curr_route:
                        route_list += [curr_route]
                        curr_route = []
            last_node = curr_node
    
    
    route_list += [curr_route]
    return route_list
