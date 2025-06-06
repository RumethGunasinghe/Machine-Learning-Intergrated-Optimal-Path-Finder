import pandas as pd
import numpy as np
import re
from collections import defaultdict
from sklearn.neighbors import KDTree
from itertools import combinations  

scats_df = pd.read_csv("./csv/Scats.csv")
unique_nodes = scats_df[["SCATS Number", "NB_LATITUDE", "NB_LONGITUDE"]].drop_duplicates(subset="SCATS Number")

directions_with_spaces = [' NE ', ' NW ', ' SE ', ' SW ', ' N ', ' S ', ' E ', ' W ']
pattern = r' (' + '|'.join([d.strip() for d in directions_with_spaces]) + r') '

def process_location(location):
    location = str(location)
    for spaced_dir in directions_with_spaces:
        if spaced_dir in location:
            direction = spaced_dir.strip()  # e.g. ' N ' → 'N'
            before, after = location.split(spaced_dir, 1)
            before = before.strip()  # remove outer whitespace
            # Clean " of " from beginning of the after part
            after_clean = re.sub(r'^of ', '', after.strip(), flags=re.IGNORECASE)
            return pd.Series([direction, before, after_clean])
    return pd.Series([None, location.strip(), None])

# Get unique rows by location
unique_locations = scats_df[["SCATS Number", "Location", "NB_LATITUDE", "NB_LONGITUDE"]].drop_duplicates(subset="Location")

# Apply parsing logic
unique_locations[['Direction', 'LocatedOn#street', 'DirectionComparedTo']] = unique_locations['Location'].apply(process_location)

# Save to CSV
unique_locations.to_csv('locationSummary.csv', index=False)
print("Processed and saved to locationSummary.csv")



def importData():
    scats_df = pd.read_csv("./csv/ScatsReformed.csv")
    traffic_df = pd.read_csv("./csv/TrafficCounts.csv")

    nodes = {
        int(row["SCATS Number"]): (row["NB_LATITUDE"], row["NB_LONGITUDE"])
        for _, row in scats_df.drop_duplicates(subset="SCATS Number").iterrows()
    }

    road_map = defaultdict(set)

    for _, row in traffic_df.iterrows():
        tfm_id = int(row["TFM_ID"])
        site_desc = str(row["SITE_DESC"])

        if '&' in site_desc:
            roads = [r.strip().upper() for r in site_desc.split('&')]
            for road in roads:
                road_map[road].add(tfm_id)

    edges = set()
    for tfm_ids in road_map.values():
        for a, b in combinations(tfm_ids, 2):
            edges.add((a, b))
            edges.add((b, a))

    return nodes, edges






        


