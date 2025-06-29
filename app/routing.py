from networkx import Graph, astar_path
from shapely.geometry import Point
from geopy.distance import geodesic
import networkx as nx
import numpy as np

def wrapped_longitude_diff(lon1, lon2):
    diff = abs(lon1 - lon2)
    return min(diff, 360 - diff)

def wrapped_haversine(lon1, lat1, lon2, lat2):
    # Adjust longitudes to handle antimeridian
    dlon = lon2 - lon1
    if abs(dlon) > 180:
        if dlon > 0:
            lon1 += 360
        else:
            lon2 += 360
    return haversine_heuristic(lon1, lat1, lon2, lat2)

def haversine_heuristic(lon1, lat1, lon2, lat2):
    #return geodesic(node1, node2).meters
#     lat1, lon1 = node1[1], node1[0]
#     lat2, lon2 = node2[1], node2[0]

    dlat = np.radians(lat2 - lat1)
    dlon = np.radians((lon2 - lon1 + 540) % 360 - 180)  # Correctly handles wrap
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return 6371000 * c  # meters

def find_shortest_path(G, kd_tree, node_coords, start_coords, end_coords):
    _, start_idx = kd_tree.query(start_coords)
    _, end_idx = kd_tree.query(end_coords)

    start_node = list(G.nodes())[start_idx]
    end_node = list(G.nodes())[end_idx]

    path = astar_path(
        G,
        start_node,
        end_node,
        heuristic=lambda a, b: wrapped_haversine(node_coords[a][0], node_coords[a][1], node_coords[b][0], node_coords[b][1]),
        weight='weight'
    )

    return [node_coords[n] for n in path]
