import pickle
import networkx as nx
import math
from fastapi import FastAPI, Query
from app.graph_loader import load_graph_and_kdtree
from app.routing import find_shortest_path
from app.routing import wrapped_haversine

app = FastAPI()
#graph, kdtree, node_coords = load_graph_and_kdtree("data/maritime_network.geojson")

# def haversine(lon1, lat1, lon2, lat2):
#     R = 6371000  # meters
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)
#     a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c
# def heuristic(a, b):
#     if a is None or b is None:
#         return float("inf")
#     return find_shortest_path(a[0], a[1], b[0], b[1])

@app.on_event("startup")
def load_graph():
    global graph, kdtree, node_coords
    with open("data/preprocessed_network.pkl", "rb") as f:
        graph, kdtree, node_coords = pickle.load(f)
    print("Graph loaded from pickle")


@app.get("/route")
def route(
    start_lat: float = Query(...),
    start_lon: float = Query(...),
    end_lat: float = Query(...),
    end_lon: float = Query(...)
):
    start_point = (start_lon, start_lat)
    end_point = (end_lon, end_lat)

    # Snap start/end points to nearest graph nodes
    dist_start, idx_start = kdtree.query(start_point)
    dist_end, idx_end = kdtree.query(end_point)

    start_node = list(node_coords.keys())[idx_start]
    end_node = list(node_coords.keys())[idx_end]

    start_coords = (start_lon, start_lat)
    end_coords = (end_lon, end_lat)

    try:
        path_nodes = find_shortest_path(graph, kdtree, node_coords, start_coords, end_coords)
#         path_nodes = nx.astar_path(
#             graph, start_node, end_node,
#             heuristic=lambda a, b: wrapped_haversine(a[0], a[1], b[0], b[1]),
#             weight="weight"
#         )
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No path found between the points")

#     start = (start_lat, start_lon)
#     end = (end_lat, end_lon)
#     path = find_shortest_path(graph, kdtree, node_coords, start, end)
    path = [start_point] + path_nodes[1:-1] + [end_point]
    return {"type": "LineString", "coordinates": path}

@app.get("/health")
def health():
    return {"status": "ok"}
