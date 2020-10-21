# Used to plot the average payload size per connection for both LTE and
# NB-IoT.

import sys
sys.path.append('C:\\Users\\woute\\Nextcloud\\Studie\\Afstuderen\\Projects')
from general_loader import *
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['Arial']

# results of the query sizedist_areas_lte.sql
reader = csvreader('lte_area_size_hist.tsv', sep='\t', header=False)

# While results per area are interesting, they are not well suited
# for printed graphs.
data = defaultdict(int)
for row in reader:
    data[int(row[1]) - 92] += int(row[2])

# To find the average size
print(sum([size * data[size] for size in data]) / sum(data.values()))

scale = max(data.values())
plt.subplots(figsize=(8, 4.5))


plt.plot(data.keys(), [x / scale for x in data.values()], ':', label='LTE')


reader = csvreader('nbiot_area_size_hist.tsv', sep='\t', header=False)

data = defaultdict(int)
for row in reader:
    data[int(row[1]) - 92] += int(row[2])

print(sum([size * data[size] for size in data]) / sum(data.values()))

scale = max(data.values())

plt.plot(data.keys(), [x / scale for x in data.values()], '-', label='NB-IoT')

plt.xlabel("Payload sizes (bytes)")
plt.ylabel("Indexed Occurrence")
plt.xscale('log')
plt.xlim(32, int(10e5))
plt.legend()

plt.tight_layout()
plt.savefig('LteNbiotSizeDist_combo.pdf')
