
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.cuts import cut_size
import time

#Path
stations_fp  = 'output/stations.csv'
connections_fp = 'output/connections.csv'
part_fp      = 'output/mbta_graph.metis.part.3'
out_png      = 'output/partitions_map.png'

#data
stations   = pd.read_csv(stations_fp).set_index('stop_id')
connections= pd.read_csv(connections_fp)
parts      = pd.read_csv(part_fp, header=None, names=['part'])
parts.index = stations.index.tolist()

#graph
G = nx.Graph()
for sid, attrs in stations.iterrows():
    G.add_node(sid, **attrs.to_dict())
for _, r in connections.iterrows():
    G.add_edge(r['u'], r['v'])
nx.set_node_attributes(G, parts['part'].to_dict(), 'part')

n = G.number_of_nodes()
E = G.number_of_edges()
k = parts['part'].nunique()

print(f"\nGraph: {n} stations, {E} edges; partitioning into k={k} parts\n")

#Partition Sizes & Balance
sizes = parts['part'].value_counts().sort_index()
ideal = n // k
sigma = sizes.max() / ideal

print("4.1 Partition Sizes & Balance")
for i, size in sizes.items():
    print(f"  • Partition {i+1}: {size} nodes")
print(f"  • Balance ratio σ = max|Vi|/⌊n/k⌋ = {sizes.max()}/{ideal} ≈ {sigma:.2f}\n")

#Edge-Cut & Cut Ratio
# Sum cut_size over each part, then divide by 2 to correct double count
raw_cut = sum(
    cut_size(G, [node for node,p in parts['part'].items() if p==i])
    for i in range(k)
)
edge_cut = raw_cut // 2
cut_ratio = edge_cut / E

print("4.2 Edge-Cut & Cut Ratio")
print(f"  • Total edge-cut = {edge_cut}")
print(f"  • Cut ratio = {edge_cut} / {E} ≈ {cut_ratio:.3f}\n")

#Edge Weights between Partitions
print("4.3 Edge Weights between Partitions")
print(f"  • (Unweighted graph → same as edge-cut) = {edge_cut}\n")

#Node-Partition Internal Differences
internal = []
for i in range(k):
    sub_nodes = [node for node,p in parts['part'].items() if p==i]
    subG = G.subgraph(sub_nodes)
    internal.append(subG.number_of_edges())
min_vol = min(internal)
diffs   = [vol - min_vol for vol in internal]

print("4.4 Community Volumes (internal edges)")
for i, vol in enumerate(internal):
    print(f"  • Part {i+1}: {vol} internal edges")
print(f"  • Differences from min: {diffs}\n")

#Complexity Analysis (measured)
print("5. Complexity Analysis")
t0 = time.time()

try:
    import nxmetis
    _, _ = nxmetis.partition(G, k)
    t1 = time.time()
    print(f"  • METIS partitioning took {(t1-t0)*1000:.1f} ms on this graph")
except ImportError:
    print("  • (Install nxmetis to measure actual runtime)")
print("  • Theoretical time complexity: O(E) for sparse graphs\n")

#Visualization
pos = {n:(stations.loc[n,'stop_lon'], stations.loc[n,'stop_lat']) for n in G.nodes()}
plt.figure(figsize=(10,8))
colors = ['red','blue','green','orange','purple']
for p in sorted(parts['part'].unique()):
    subset = [n for n in G.nodes() if G.nodes[n]['part']==p]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=subset,
        node_color=colors[p],
        label=f'Partition {p+1}',
        node_size=20
    )
nx.draw_networkx_edges(G, pos, alpha=0.2)

plt.legend()
plt.title('MBTA Subway Network Partitions (METIS)')
plt.axis('off')
plt.tight_layout()
os.makedirs('output', exist_ok=True)
plt.savefig(out_png, dpi=150)
plt.show()

print(f"Partition map saved to {out_png}\n")
