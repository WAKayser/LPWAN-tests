# Takes results from the created JSON and makes an histogram.

import matplotlib.pyplot as plt
from matplotlib import rcParams
import json

rcParams['font.sans-serif'] = ['Arial']

# Ingest data from json file.
dists = json.load(open('dists.json', 'r'))

# Remove all values that could not find a close  cell.
[dists.pop(key) for key in [key for key in dists if dists[key] == 20000]]

# calculate average and print it.
print(f'The average distance is {sum(dists.values()) / len(dists.values())}')

plt.subplots(figsize=(4.5*1.4, 4.5))
# Truncate to 10 km, as only few cells are outside this window
plt.hist(dists.values(), bins=100, range=(0, 10000))
plt.xlim(0, 10000)
plt.xlabel('Inter Site Distance (m)')
plt.ylabel('Occurrence')
plt.savefig('disthist.pdf')
