import sys
sys.path.append('C:\\Users\\woute\\Nextcloud\\Studie\\Afstuderen\\Projects')
from datetime import datetime
from general_loader import *
from math import floor
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['Arial']

# Code for enabling differing hour labels.
hours = mdates.HourLocator()   # every year
minutes = mdates.MinuteLocator(byminute=[15, 30, 45])  # every month

third_hours = mdates.HourLocator(byhour=range(3, 24, 3))
hour_fmt = mdates.DateFormatter('%H')
# used to remove labels from minor ticks.
minute_fmt = mdates.DateFormatter('')

# Read first half of results from the table with standard counters.
# file: fouroverdayplotsLTE.sql
reader = csvreader('KPIoverday.csv', sep=',', header=False)

results = defaultdict(list)

for row in reader:
    results['vol_dl'].append(float(row[0]))
    results['vol_ul'].append(float(row[1]))
    results['con'].append(float(row[2]))
    results['sr_dl'].append(float(row[3]))
    results['sr_ul'].append(float(row[4]))
    results['sr_ra'].append(float(row[5]))
    results['sr_rrc'].append(float(row[6]))
    # Date is not actually important, but is needed for the library
    results['time'].append(datetime(year=2020, month=6, day=25,
                                    hour=int(row[7]), minute=int(row[8])))


# Read second half of results as, these can only be received from the vector
# counters. So a separate query was used in this case.
reader = csvreader('utiloverdayLTE.csv', sep=',', header=False)

results_use = defaultdict(list)

for row in reader:
    results_use['dl'].append(float(row[0]))
    results_use['ul'].append(float(row[1]))
    # Date is not actually important, but is needed for the library
    results_use['time'].append(datetime(year=2020, month=6, day=25,
                                        hour=int(row[2]), minute=int(row[3])))


#  What will follow is five definitions of plots, which will not be that
#  interesting. Most space is used for selecting the right formatters.

ax = plt.subplot(311)
plt.plot(results['time'], results['vol_ul'], 'v-', label='UL', markevery=8)
plt.plot(results['time'], results['vol_dl'], 'o-', label='DL', markevery=8)
plt.title('Throughput')
plt.ylabel("Volume (kbit)")
plt.xlabel("Time of day")
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hour_fmt)
ax.xaxis.set_minor_locator(minutes)
ax.xaxis.set_minor_formatter(minute_fmt)
plt.legend()

ax = plt.subplot(323)
plt.plot(results['time'], results['con'], label='S1 Connections')
plt.title('S1 Connections')
plt.ylabel("S1 Connections")
plt.xlabel("Time of day")
ax.xaxis.set_major_locator(third_hours)
ax.xaxis.set_major_formatter(hour_fmt)
ax.xaxis.set_minor_locator(hours)
ax.xaxis.set_minor_formatter(minute_fmt)

ax = plt.subplot(324)
plt.plot(results['time'], results['sr_ra'], 'v-',  label='Random Access',
         markevery=8)
plt.plot(results['time'], results['sr_rrc'], 'o-',  label='RRC setup',
         markevery=8)
plt.title('Success rate for attaching')
plt.ylabel("success rate")
plt.xlabel("Time of day")
ax.xaxis.set_major_locator(third_hours)
ax.xaxis.set_major_formatter(hour_fmt)
ax.xaxis.set_minor_locator(hours)
ax.xaxis.set_minor_formatter(minute_fmt)
plt.legend()

ax = plt.subplot(325)
plt.plot(results['time'], results_use['ul'], 'v-', label='Uplink',
         markevery=8)
plt.plot(results['time'], results_use['dl'], 'o-', label='Downlink',
         markevery=8)
plt.title('PRB Usage')
plt.ylabel("percentage")
plt.xlabel("Time of day")
ax.xaxis.set_major_locator(third_hours)
ax.xaxis.set_major_formatter(hour_fmt)
ax.xaxis.set_minor_locator(hours)
ax.xaxis.set_minor_formatter(minute_fmt)
plt.legend()

ax = plt.subplot(326)
plt.plot(results['time'], results['sr_ul'], 'v-', label='Uplink',
         markevery=8)
plt.plot(results['time'], results['sr_dl'], 'o-', label='Downlink',
         markevery=8)
plt.title('Success rate of data transmission')
plt.ylabel("Success rate")
plt.xlabel("Time of day")
ax.xaxis.set_major_locator(third_hours)
ax.xaxis.set_major_formatter(hour_fmt)
ax.xaxis.set_minor_locator(hours)
ax.xaxis.set_minor_formatter(minute_fmt)
plt.legend()

plt.tight_layout()
try_store('LTEoverday.pdf')
