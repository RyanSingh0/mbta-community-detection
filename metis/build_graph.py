
import os, sys
import pandas as pd

#paths
stations_fp    = os.path.join('output', 'stations.csv')
connections_fp = os.path.join('output', 'connections.csv')
out_metis      = os.path.join('output', 'mbta_graph.metis')

#Check inputs
for fp in (stations_fp, connections_fp):
    if not os.path.exists(fp):
        print(f"ERROR: Missing {fp}")
        sys.exit(1)
print("Found stations & connections CSVs")

#Load
stations   = pd.read_csv(stations_fp)
connections= pd.read_csv(connections_fp)
print(f"Loaded {len(stations)} stations, {len(connections)} connections")

#Map stop_id 1‑based idx
nodes = stations['stop_id'].tolist()
idx_map = {sid: i+1 for i, sid in enumerate(nodes)}

#adjacency
adj = {i+1: set() for i in range(len(nodes))}
for _, r in connections.iterrows():
    u, v = r['u'], r['v']
    if u in idx_map and v in idx_map:
        ui, vi = idx_map[u], idx_map[v]
        adj[ui].add(vi)
        adj[vi].add(ui)

num_nodes = len(nodes)
num_edges = sum(len(nbrs) for nbrs in adj.values())//2
print(f"→ Graph: {num_nodes} nodes, {num_edges} edges")

#METIS
os.makedirs('output', exist_ok=True)
with open(out_metis, 'w') as f:
    f.write(f"{num_nodes} {num_edges}\n")
    for i in range(1, num_nodes+1):
        f.write(" ".join(str(nb) for nb in sorted(adj[i])) + "\n")

print(f"Wrote METIS to {out_metis}")
