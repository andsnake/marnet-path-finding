import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString
import numpy as np
from scipy.spatial import cKDTree
from geopy.distance import geodesic


def load_graph_and_kdtree(filepath, debug=False):
    gdf = gpd.read_file(filepath)
    # Filter out invalid or null geometries
    gdf = gdf[gdf.geometry.notnull() & gdf.geometry.is_valid]

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

#duplicate edges near the antimeridian into their +360 degrees counterparts
def add_antimeridian_edges(G, coords, threshold=179):
     tree = cKDTree(coords)
     added_edges = 0

     for point in coords:
         lon, lat = point
         if lon >= threshold:
             # Wrap east → west
             wrapped_point = (lon - 360, lat)
         elif lon <= -threshold:
             # Wrap west → east
             wrapped_point = (lon + 360, lat)
         else:
             continue

         # Find nearest node to the wrapped point
         _, idx = tree.query(wrapped_point)
         neighbor = coords[idx]

         # Calculate geodesic distance instead of Euclidean
         dist = geodesic((lat, lon), (neighbor[1], neighbor[0])).meters
         G.add_edge(point, neighbor, weight=dist)
         added_edges += 1

     print(f"Added {added_edges} antimeridian-crossing edges.")