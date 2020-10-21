# Uses core traffic logs to determine how often the bearer is adjusted
# Mainly takes specific TEID values as unique sessions. Which should be
# the case.

import sys
sys.path.append('C:\\Users\\woute\\Nextcloud\\Studie\\Afstuderen\\Projects')
from general_loader import *
import matplotlib.pyplot as plt
from math import floor
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['Arial']
x_as = ['< 5 Minutes', '5 Minutes', '< 30 Minutes', '< 1 Hour', '< 2 Hours',
        '< 3 Hours', '< 4 Hours', '< 6 Hours', '< 9 Hours', '< 12 Hours',
        '< 1 Day', '< 2 Days', '> 2 Days']


def period_extractor(reader):
    def axis_mapper(delta):
        # Could also use a loop and another array
        if delta < 270:
            return '< 5 Minutes'
        elif delta < 330:
            return '5 Minutes'
        elif delta < 32 * 60:
            return '< 30 Minutes'
        elif delta < 64 * 60:
            return '< 1 Hour'
        elif delta < 2 * 64 * 60:
            return '< 2 Hours'
        elif delta < 3 * 64 * 60:
            return '< 3 Hours'
        elif delta < 4 * 64 * 60:
            return '< 4 Hours'
        elif delta < 6 * 64 * 60:
            return '< 6 Hours'
        elif delta < 9 * 64 * 60:
            return '< 9 Hours'
        elif delta < 12 * 64 * 60:
            return '< 12 Hours'
        elif delta < 24 * 64 * 60:
            return '< 1 Day'
        elif delta < 2 * 24 * 60 * 60:
            return '< 2 Days'
        else:
            return '> 2 Days'

    def time_stamper(value):
        # Turns a string time value in seconds from the start of the month
        day, time = value.split()[0], value.split()[1].split(':')
        time = [int(x) for x in time]
        return int(day) * 24 * 3600 + time[0] * 3600 + time[1] * 60 + time[2]

    total, updates, status = 0, 0, {}
    periods = {x: 0 for x in x_as}

    for row in reader:
        # Read each modify request and check when the previous message was.
        time = time_stamper(row[0][8:-11])
        TEID = int(row[1][1:-2], 16)
        if TEID in status:
            delta = (time - status[TEID])
            # Increment the appropriate bin
            periods[axis_mapper(delta)] += delta
            total += delta
            updates += 1
        # Set the last used time to the new value
        status[TEID] = time
    return periods, total / updates


fig, ax = plt.subplots()

ax.tick_params(axis='both', which='major', labelsize=10)


# Unfortunately this file will probably not be able to be shared.
# However an MBREQ filter is easy to write.
result, average = period_extractor(csvreader('../../DATA/bigmbreqcsv.csv',
                                             sep=',', header=False))

total = sum(result.values())
print(total)

plt.subplots(figsize=(8, 4.5))

plt.bar(x_as, [x / total * 100 for x in result.values()])
plt.xticks(rotation=45)

plt.tight_layout()
plt.xlabel("Period Bins")
plt.ylabel("Occurrence (%)")
# plt.show()
plt.savefig('periods.pdf', bbox_inches='tight')
