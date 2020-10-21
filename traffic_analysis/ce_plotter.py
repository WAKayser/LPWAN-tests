import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.ticker
rcParams['font.sans-serif'] = ['Arial']

# Will be reused multiple times, as three reappears oftenn. 
x = range(3)

# Values taken from the sums found in the dataset for training the
# cost model for actions.

S1 = [841385, 22316, 18401]
vol = [2418530, 106827, 74495]

# Step used for normalization.
s1norm = [x / sum(S1) for x in S1]
volnorm = [x / sum(vol) for x in vol]

# Simple plotting with lgo scale on y axis. 
# Only label values on x-axis with results.
plt.figure(figsize=(8,4.5))
ax = plt.subplot(121)
plt.yscale('log')
plt.ylabel('Normalized S1 connections')
plt.xticks(x, x)
plt.bar(x, s1norm)
plt.xlabel('CE')
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax = plt.subplot(122)
plt.ylabel('Normalized data volume')
plt.bar(x, volnorm)
plt.xticks(x, x)
plt.xlabel('CE')
plt.yscale('log')
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.tight_layout()
plt.savefig('simpleCEdist.pdf')