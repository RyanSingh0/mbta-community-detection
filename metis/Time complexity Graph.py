import time
import networkx as nx
import nxmetis
import matplotlib.pyplot as plt


sizes = [500, 1000, 2000, 4000, 8000]

edges = []
times = []

for n in sizes:
    # Build a random sparse graph: tree + 5% extra edges
    G = nx.random_tree(n)
    extra = int(n * 0.05)
    nodes = list(G.nodes())
    rng = nx.utils.default_rng(seed=42)
    for _ in range(extra):
        u, v = rng.choice(nodes), rng.choice(nodes)
        if u != v:
            G.add_edge(u, v)
    
    E = G.number_of_edges()

    # Time METIS partition (k=3)
    t0 = time.time()
    _ = nxmetis.partition(G, 3)
    t1 = time.time()

    elapsed_ms = (t1 - t0) * 1000
    print(f"n={n}, E={E}, time={elapsed_ms:.2f} ms")

    edges.append(E)
    times.append(elapsed_ms)

plt.figure(figsize=(8,5))
plt.loglog(edges, times, marker='o', basex=10, basey=10)
plt.xlabel('Number of edges (E)')
plt.ylabel('Partition time (ms)')
plt.title('METIS Runtime vs. Graph Size (Sparse) [log-log]')
plt.grid(True, which='both', ls='--')
plt.tight_layout()
plt.savefig('output/metis_scaling_loglog.png', dpi=200)
plt.show()

import matplotlib.pyplot as plt


edges = [524, 1045, 2094, 4188, 8380]
times = [10.2, 18.5, 32.1, 58.3, 110.7]

plt.figure(figsize=(8,5))
plt.plot(edges, times, '-o')
plt.xlabel('Number of edges (E)')
plt.ylabel('Partition time (ms)')
plt.title('METIS Partition Time vs. Edge Count')
plt.grid(True)
plt.ylim(0, max(times)*1.2)  # ensure y-axis starts at 0
plt.tight_layout()
plt.show()

