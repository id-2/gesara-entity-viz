from collections import Counter
import json

import networkx as nx
import pandas as pd

import colorcet


# Colors used for different graph modularity classes
COLORS = colorcet.glasbey_dark

OUTPUT_JSON = "../public/dataset_entities.json"

NODE_SCALING = 0.5
# GraphML file generated by Gephi
INPUT_GRAPHML = "data/entity_network_layout.graphml"
CLUSTERS = [
    {"key": "13", "clusterLabel": "US politics"},
    {"key": "0", "clusterLabel": "Covid and social media"},
    {"key": "4", "clusterLabel": "Digital soldiers and world leaders"},
    {"key": "17", "clusterLabel": "US conspiracies"},
    {"key": "19", "clusterLabel": "Elite human trafficking"},
    {"key": "9", "clusterLabel": "Big Tech and technocracy"},
    {"key": "16", "clusterLabel": "Epstein and pedophilia"},
    {"key": "24", "clusterLabel": "Satanic US Cabal"},
    {"key": "8", "clusterLabel": "Global Cabal"},
    {"key": "1", "clusterLabel": "Kennedy and royal conspiracies"},
    {"key": "14", "clusterLabel": "Pharma and Anti-Vax"},
    {"key": "23", "clusterLabel": "US sports and celebrities"},
    {"key": "21", "clusterLabel": "Technological conspiracies"},
    {"key": "25", "clusterLabel": "Fake news media"},
    {"key": "7", "clusterLabel": "Vaccine injuries"},
    {"key": "30", "clusterLabel": "Academia and countries"},
    {"key": "39", "clusterLabel": "BLM/Antifa and Democrats"},
    {"key": "11", "clusterLabel": "Big corporations and airlines"},
    {"key": "15", "clusterLabel": "Alternative doctors"},
    {"key": "2", "clusterLabel": "Conservative legal institutions"},
    {"key": "26", "clusterLabel": "Big Pharma"},
    {"key": "27", "clusterLabel": "Freedom convoys"},
    {"key": "12", "clusterLabel": "US state-level politics"},
    {"key": "34", "clusterLabel": "Chemistry and alternative medicine"},
    {"key": "20", "clusterLabel": "Mass shooters"},
    {"key": "3", "clusterLabel": "Public health"},
    {"key": "10", "clusterLabel": "Right-wing media"},
    {"key": "37", "clusterLabel": "Payment platforms"},
    {"key": "42", "clusterLabel": "Vote audit"},
]
BOUNDING_BOX = {"x": [-300, 400], "y": [-600, 150]}


if __name__ == "__main__":

    G = nx.read_graphml(path=INPUT_GRAPHML)

    _nodes_df = pd.DataFrame.from_dict(
        dict(G.nodes(data=True)), orient="index"
    ).reset_index(drop=True)
    _edges_df = nx.to_pandas_edgelist(G=G)

    nodes_df = _nodes_df[["x", "y", "label", "size", "frequency", "Modularity Class"]]
    edges_df = _edges_df[["source", "target"]]

    clusters_to_combine = {
        k
        for k, v in Counter(nodes_df["Modularity Class"]).items()
        if k not in set([int(c["key"]) for c in CLUSTERS])
    }
    print("clusters_to_combine: ", clusters_to_combine)
    nodes_df["cluster"] = nodes_df["Modularity Class"].apply(
        lambda c: "100" if c in clusters_to_combine else str(c)
    )
    nodes_df.drop("Modularity Class", axis="columns", inplace=True)
    nodes_df["key"] = nodes_df["label"]
    nodes_df["size"] /= NODE_SCALING
    nodes = nodes_df.to_dict(orient="records")

    edges = [[e["source"], e["target"]] for e in edges_df.to_dict(orient="records")]
    data = {
        "nodes": nodes,
        "edges": edges,
        "clusters": [
            {**cluster, "color": COLORS[i]} for i, cluster in enumerate(CLUSTERS)
        ]
        + [{"key": "100", "clusterLabel": "Other", "color": "#999999"}],
        "bbox": BOUNDING_BOX,
    }

    with open(OUTPUT_JSON, "w") as f:
        json.dump(obj=data, fp=f, separators=(",", ":"))
