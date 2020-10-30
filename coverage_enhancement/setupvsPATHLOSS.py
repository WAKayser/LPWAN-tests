import sys
sys.path.append('C:\\Users\\woute\\Nextcloud\\Studie\\Afstuderen\\Projects')
from general_loader import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
from collections import defaultdict
rcParams['font.sans-serif'] = ['Arial']

reader = csvreader('setupvsPATHLOSS.sql20200610 09 45 33.bckup', sep=',',
                   header=False)

results = defaultdict(list)

# Not all bins are nice enough to report good values.
# Loading in is some extra work.
for row in reader:
    if row[0]:
        results['pathloss_0'].append(float(row[8]))
        results['ratio_0'].append(float(row[0]))
    if row[1]:
        results['pathloss_1'].append(float(row[8]))
        results['ratio_1'].append(float(row[1]))
    if row[2]:
        results['pathloss_2'].append(float(row[8]))
        results['ratio_2'].append(float(row[2]))
    if row[3]:
        results['pathloss_3'].append(float(row[8]))
        results['ratio_3'].append(float(row[3]))
    if row[4]:
        results['pathloss_4'].append(float(row[8]))
        results['ratio_4'].append(float(row[4]))
    if row[5]:
        results['pathloss_5'].append(float(row[8]))
        results['ratio_5'].append(float(row[5]))
    if row[6]:
        results['pathloss_6'].append(float(row[8]))
        results['ratio_6'].append(float(row[6]))
    if row[7]:
        results['pathloss_7'].append(float(row[8]))
        results['ratio_7'].append(float(row[7]))

# Half page size plot
fig, ax = plt.subplots(figsize=(8*0.49, 4.5))

# plot just the total values for clarity
plt.plot(results['pathloss_7'], results['ratio_7'], 'v-',
         label='Random Access', markevery=20)
plt.plot(results['pathloss_3'], results['ratio_3'], 'o-',
         label='RRC', markevery=20)

# Plot the average values found for LTE
plt.axhline(0.885, ls=":", label='Mean LTE RA')
plt.axhline(0.985, ls="-.", label='Mean LTE RRC')

plt.legend()
plt.xlabel("Path loss (dB)")
plt.ylabel("Probability")
plt.tight_layout()
try_store('pathloss_setup.pdf')
