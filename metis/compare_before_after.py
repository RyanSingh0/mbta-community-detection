import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#Paths
stations_fp   = 'output/stations.csv'
connections_fp= 'output/connections.csv'
part_fp       = 'output/mbta_graph.metis.part.3'
out_png       = 'output/after_metis_highres.png'

#Load data
stations    = pd.read_csv(stations_fp).set_index('stop_id')
connections = pd.read_csv(connections_fp)
parts       = pd.read_csv(part_fp, header=None, names=['part'])
parts.index = stations.index.tolist()

#Build graph & positions
G = nx.Graph()
for sid, attrs in stations.iterrows():
    G.add_node(sid, name=attrs['stop_name'])
for _, r in connections.iterrows():
    G.add_edge(r['u'], r['v'])

pos = {
    n: (stations.loc[n,'stop_lon'], stations.loc[n,'stop_lat'])
    for n in G.nodes()
}

#Prepare colors & labels
partition = parts['part'].to_dict()
colors    = ['red','blue','green','orange','purple']
node_colors = [colors[partition[n]] for n in G.nodes()]
labels    = {n: G.nodes[n]['name'] for n in G.nodes()}

#Plot side changez because points not visible
fig = plt.figure(figsize=(40,24), dpi=150)
ax  = fig.add_subplot(1,1,1)
ax.set_aspect('equal', 'box')

#Draw edges
nx.draw_networkx_edges(G, pos, ax=ax,
                       edge_color='lightgray', width=0.5)

#Draw nodes by partition
for p in sorted(set(partition.values())):
    nodes_p = [n for n in G.nodes() if partition[n]==p]
    nx.draw_networkx_nodes(
        G, pos, nodelist=nodes_p,
        node_color=colors[p],
        node_size=80,
        label=f'Partition {p+1}',
        ax=ax
    )

#Draw labels (tiny font)
nx.draw_networkx_labels(
    G, pos, labels=labels,
    font_size=5,
    font_color='black',
    verticalalignment='center_baseline',
    horizontalalignment='left',
    ax=ax
)

#Title & legend
ax.set_title('MBTA Subway Network — After METIS (k=3)', fontsize=32)
ax.legend(scatterpoints=1, frameon=True, fontsize=20, loc='upper left')

ax.axis('off')
plt.tight_layout()
os.makedirs('output', exist_ok=True)
fig.savefig(out_png, dpi=150)
plt.close(fig)

print(f" Saved high-res After-METIS map to {out_png}")
