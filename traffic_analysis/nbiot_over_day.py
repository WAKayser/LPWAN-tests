import sys
sys.path.append('C:\\Users\\woute\\Nextcloud\\Studie\\Afstuderen\\Projects')
from datetime import datetime
from general_loader import *
from math import floor
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['Arial']

# Enable the different hour based axis labels
hours = mdates.HourLocator()   # every year
minutes = mdates.MinuteLocator(byminute=[15, 30, 45])  # every month

third_hours = mdates.HourLocator(byhour=range(3, 24, 3))
hour_fmt = mdates.DateFormatter('%H')
minute_fmt = mdates.DateFormatter('')

reader = csvreader('fiveoverdayplots.sql20200610 15 31 04.bckup', sep=',',
                   header=False)

results = defaultdict(list)

for row in reader:
    # Some brilliant code to convert all to float and in the right columns
    # Later on more often pandas will be used to fix this.
    results['vol_dl'].append(float(row[0]))
    results['vol_ul'].append(float(row[1]))
    results['con'].append(float(row[2]))
    results['use_dl'].append(float(row[3]))
    results['use_ul'].append(float(row[4]))
    results['sr_dl'].append(float(row[5]))
    results['sr_ul'].append(float(row[6]))
    results['sr_ra'].append(float(row[7]))
    results['sr_rrc'].append(float(row[8]))
    results['time'].append(datetime(year=2020, month=6, day=25,
                                    hour=int(row[9]), minute=int(row[10])))


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
plt.plot(results['time'], results['use_ul'], 'v-', label='Uplink',
         markevery=8)
plt.plot(results['time'], results['use_dl'], 'o-', label='Downlink',
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
try_store('overdayNBIOT.pdf')
