from app.graph_loader import load_graph_and_kdtree
from app.graph_loader import add_antimeridian_edges
import pickle

def preprocess_network(geojson_path, output_path):
    G, kd_tree, coord_map = load_graph_and_kdtree(geojson_path, True)
    # coord_map is a dict {pt: pt} — but you want the list of coords, which is:
    coords = list(coord_map.keys())
    add_antimeridian_edges(G, coords)
    with open(output_path, 'wb') as f:
        pickle.dump((G, kd_tree, coord_map), f)
    print(f"Preprocessed network saved to {output_path}")

if __name__ == "__main__":
    preprocess_network("data/maritime_network.geojson", "data/preprocessed_network.pkl")

