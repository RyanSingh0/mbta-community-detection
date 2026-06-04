import os, pandas as pd
python scripts\visualize_partitions_with_labels.py


#Paths
stations_fp    = 'output/stations.csv'
connections_fp = 'output/connections.csv'
out_metis      = 'output/mbta_graph.metis'

#Load data
stations   = pd.read_csv(stations_fp)
connections= pd.read_csv(connections_fp)

#Build index map
nodes   = stations['stop_id'].tolist()
idx_map = {sid: i+1 for i, sid in enumerate(nodes)}

#adjacency
adj = {i+1: set() for i in range(len(nodes))}
for _, row in connections.iterrows():
    u, v = row['u'], row['v']
    if u in idx_map and v in idx_map:
        ui, vi = idx_map[u], idx_map[v]
        adj[ui].add(vi)
        adj[vi].add(ui)

#Count nodes & edges
num_nodes = len(nodes)
num_edges = sum(len(neigh) for neigh in adj.values()) // 2
print(f"Graph: {num_nodes} nodes, {num_edges} edges")

#Write METIS
os.makedirs('output', exist_ok=True)
with open(out_metis, 'w') as f:
    f.write(f"{num_nodes} {num_edges}\n")
    for i in range(1, num_nodes+1):
        line = " ".join(str(nb) for nb in sorted(adj[i]))
        f.write(line + "\n")

print(f"Wrote METIS to {out_metis}")

