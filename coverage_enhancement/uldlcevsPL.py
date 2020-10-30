import sys
sys.path.append('C:\\Users\\woute\\Nextcloud\\Studie\\Afstuderen\\Projects')
from general_loader import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
from collections import defaultdict
rcParams['font.sans-serif'] = ['Arial']

reader = csvreader('ULDLCEvsPL.sql20200609 15 18 53.bckup', sep=',',
                   header=False)

results = defaultdict(list)

# sql contains data on per coverage enhancement level
# but this is in the end not plotted for clarity
for row in reader:
    results['ratio_0'].append(float(row[0]))
    results['ratio_1'].append(float(row[1]))
    results['ratio_2'].append(float(row[2]))
    results['ratio_3'].append(float(row[3]))
    results['ratio_4'].append(float(row[4]))
    results['ratio_5'].append(float(row[5]))
    results['ratio_6'].append(float(row[6]))
    results['ratio_7'].append(float(row[7]))
    results['pathloss'].append(float(row[8]))

# Half size figures
fig, ax = plt.subplots(figsize=(8*0.49, 4.5))

# Plot just the total values.
plt.plot(results['pathloss'], results['ratio_7'], 'v-',
         label='NB-IoT UL', markevery=5)
plt.plot(results['pathloss'], results['ratio_3'], 'o-',
         label='NB-IoT DL', markevery=5)

# Add lines to show the average value for LTE.
# Comparison per path loss is odd, as different modulation
plt.axhline(0.950, ls=":", label='Mean LTE UL')
plt.axhline(0.930, ls="-.", label='Mean LTE DL')

plt.legend()
plt.xlabel("Path loss (dB)")
plt.ylabel("Probability")
plt.tight_layout()
try_store('pathloss_dlul_noce.pdf')
