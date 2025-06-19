import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString
import numpy as np
from scipy.spatial import cKDTree

def load_graph_and_kdtree(filepath, debug=False):
    gdf = gpd.read_file(filepath)
    G = nx.Graph()
    coords = []
    total_lines = len(gdf)
    processed_lines = 0

    for line in gdf.geometry:
        processed_lines += 1
        if isinstance(line, LineString):
            pts = list(line.coords)
            for i in range(len(pts) - 1):
                a, b = pts[i], pts[i+1]
                dist = np.linalg.norm(np.array(a) - np.array(b))
                G.add_edge(a, b, weight=dist)
                if a not in coords: coords.append(a)
                if b not in coords: coords.append(b)

        if debug:
            if processed_lines % 100 == 0 or processed_lines == total_lines:
                print(f"Processed {processed_lines}/{total_lines} geometries...")

    kd_tree = cKDTree(coords)
    coord_map = {pt: pt for pt in G.nodes()}
    return G, kd_tree, coord_map

def add_antimeridian_edges(G, coords, threshold=179.9):
    for point in coords:
        lon = point[0]
        if lon >= threshold:
            wrapped_point = (lon - 360, point[1])
        elif lon <= -threshold:
            wrapped_point = (lon + 360, point[1])
        else:
            continue

        # Find nearest real node to the wrapped point
        _, idx = cKDTree(coords).query(wrapped_point)
        neighbor = coords[idx]
        dist = np.linalg.norm(np.array(point) - np.array(neighbor))
        G.add_edge(point, neighbor, weight=dist)