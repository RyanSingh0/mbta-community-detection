import pandas as pd
import os

os.makedirs('output', exist_ok=True)

#Load GTFS files
stops      = pd.read_csv('data/gtfs/stops.txt')
routes     = pd.read_csv('data/gtfs/routes.txt')
trips      = pd.read_csv('data/gtfs/trips.txt')
stop_times = pd.read_csv('data/gtfs/stop_times.txt')

#Filter subway route_type 0 or 1
subway_routes = routes[routes['route_type'].isin([0,1])]
subway_trips  = trips[trips['route_id'].isin(subway_routes['route_id'])]
subway_times  = stop_times[stop_times['trip_id'].isin(subway_trips['trip_id'])]

#Export stations
station_ids = subway_times['stop_id'].unique()
stations = stops[stops['stop_id'].isin(station_ids)][
    ['stop_id','stop_name','stop_lat','stop_lon']
]
stations.to_csv('output/stations.csv', index=False)

#edges
edges = []
for tid, grp in subway_times.groupby('trip_id'):
    seq = grp.sort_values('stop_sequence')['stop_id'].tolist()
    edges += list(zip(seq, seq[1:]))
edges_df = pd.DataFrame(edges, columns=['u','v']).drop_duplicates()
edges_df.to_csv('output/connections.csv', index=False)

print("Stations:", len(stations), "Connections:", len(edges_df))
