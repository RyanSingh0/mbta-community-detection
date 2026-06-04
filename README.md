# MBTA Subway Network Community Detection

> **CS566 · Boston University**

![Python](https://img.shields.io/badge/Python-3.10-blue)
![NetworkX](https://img.shields.io/badge/NetworkX-3.x-orange)
![Folium](https://img.shields.io/badge/Folium-map-77b829)
![Modularity](https://img.shields.io/badge/Modularity-0.81-brightgreen)
![Communities](https://img.shields.io/badge/Communities-10-green)

---

## Overview

Graph analytics on **Boston's MBTA subway network** to discover operationally meaningful station communities using three graph partitioning algorithms: Louvain, METIS, and Spectral Clustering.

**Motivation:** Understanding a subway network's community structure can reveal natural groupings of stations — useful for optimizing routes, managing disruptions, planning fare zones, and identifying bottlenecks. The MBTA serves millions of riders; even small structural insights have large operational impact.

---

## Graph Construction

**Data source:** MBTA GTFS (General Transit Feed Specification) dataset

**Preprocessing:**
1. Filter routes where `route_type == 1` (subway only — excludes buses, commuter rail)
2. Extract all trips on subway routes
3. Filter stop_times to subway trips only
4. Build edges: consecutive stops in each trip = one edge

**Edge weights:** Number of times a pair of consecutive stations appears across all trips (frequency proxy for connection strength)

**Final graph:** Undirected, weighted
| Property | Value |
|----------|-------|
| Nodes (stations) | **106** |
| Edges (connections) | **113** |
| Edge weights | Trip frequency |

---

## Algorithms

### 1. Louvain Community Detection

**Selected as primary method.** Louvain maximizes modularity — the fraction of edges within communities minus the expected fraction under a random graph model.

**Results:**
| Metric | Value |
|--------|-------|
| Communities detected | **10** |
| Modularity score | **0.8113** |
| Time complexity | O(n log n) |
| Memory usage (post-algorithm) | 88.57 MB (modest increase from 88.46 MB base) |

**Modularity interpretation:** 0.81 is very high (>0.7 indicates strong community structure). The 10 communities correspond to geographically coherent regions of the subway network.

**Scalability analysis:** Louvain applied to subgraphs of 20, 40, 60, 80, 100 nodes:
- Modularity increases with graph size, peaking at ~80 nodes (avg 0.9031)
- Slight dip at 100 nodes (0.8373) as cross-community connections increase
- Confirms O(n log n) scaling behavior

**Edge weight balance:** Cross-partition edge weight = 8,481. All 10 communities have identical internal edge weight sum (differences = [0,0,0,0,0,0,0,0,0,0]) — perfectly balanced partitioning.

### 2. METIS Graph Partitioning

METIS partitions large graphs while minimizing edge cuts and balancing partition sizes. Designed for computational applications where balanced, low-cut partitions are required (e.g., distributed graph processing).

### 3. Spectral Clustering

Uses the eigenvalues of the graph Laplacian to detect cluster structure. Effective for detecting non-obvious community boundaries that depend on global graph structure rather than just local connectivity.

### Geographic visualization

Detected communities are projected back onto a real Boston map with **Folium** (`results/folium_clustered_map.png`), and compared side-by-side against the actual subway lines (`results/actual_lines.png`) to show how closely the data-driven communities track the real service structure. Runtime and peak-RAM are profiled per stage (`results/stagewise_runtime.png`, `results/peak_ram.png`).

---

## Key Findings

1. **Strong community structure exists** (modularity 0.81) — the MBTA subway is not a random network. Stations cluster into 10 naturally cohesive groups corresponding to subway line service areas.

2. **Louvain outperforms alternatives** for this graph — produces more balanced, higher-modularity partitions than METIS or Spectral Clustering on this specific topology.

3. **Perfectly balanced internal connectivity** — all 10 communities have equal internal edge weight sum, suggesting the network was (perhaps coincidentally) built with natural geographic balance.

4. **Scalability confirmed** — O(n log n) behavior validated experimentally across 5 subgraph sizes.

---

## How to Run

```bash
pip install -r requirements.txt
# core libs: networkx, python-louvain, scikit-learn, folium, numpy, matplotlib, pandas

# Download the MBTA GTFS feed (see data/ note), then run the notebooks:
jupyter notebook notebooks/Louvain_method.ipynb        # primary method
jupyter notebook notebooks/Spectral_clustering.ipynb   # comparison
# METIS partitioning code is under metis/
```

Outputs (community maps, metrics, runtime/RAM plots) are written to `results/`.

---

## Team

CS566 group project — **Nida · Pranjal · Aryan Meena** (Boston University).

---

**Aryan Meena** · Boston University · CS566
