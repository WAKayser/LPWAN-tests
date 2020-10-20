# Turns location data into data on the distances between cells
# A slightly different SQL based method will be used for later plots
# Rijksdriehoekcoordinaten are used, which provide an orthogonal system
# Distance and angle calculations are thus simplified. 

from tqdm import tqdm
from numpy import sqrt, arctan2
import json

# This CSV file is an export of the similarly named table.
reader = csvreader('sitelocationandazimut.csv', sep=';', header=False)

locs = {}
distances = {}

for row in reader:
    if row[3][0:3] == '08L':
        locs[row[3]] = [row[0], int(row[1]), int(row[2]), int(row[4])]

# Certainly not really optimized, but is not that important
for cell_a in tqdm(locs):
    # Arbitrary upper limit
    distance = 20000
    for cell_b in locs:
        # Cell should not have the same Site ID
        if locs[cell_a][0] == locs[cell_b][0]:
            continue

        # Find the distance in X and Y values between the cells.
        vec_diff_y = locs[cell_b][2] - locs[cell_a][2]
        vec_diff_x = locs[cell_b][1] - locs[cell_a][1]

        # Determine the angle between north and the difference vector
        angle_diff = (arctan2(vec_diff_y, vec_diff_x) - locs[cell_a][3]) % 360

        # Check if the cell is in the right sector.
        if angle_diff > 60 and angle_diff < 300:
            continue
        # Simple Pythagoras due to nice orthogonal system
        distance_new = sqrt((vec_diff_x)**2 + (vec_diff_y)**2)
        distance = min(distance, distance_new)
    # Insert the distance if needed
    distances[cell_a] = distance

with open('dists.json', 'w') as f:
    json.dump(distances, f)
