from collections import defaultdict
import matplotlib.pyplot as plt
import statistics
from matplotlib import rcParams
import sys
sys.path.append('C:\\Users\\woute\\Nextcloud\\Studie\\Afstuderen\\Projects')
from general_loader import *

rcParams['font.sans-serif'] = ['Arial']

# Load Counter Data
raw = load_dict(csvreader('../../DATA/raw.tsv'), 1)

# Load test log data
testlog = read_log(csvreader('../AT-AT/autotest.log'), '08N063283')

# Merge data sets
dataset = combine_ts([raw, testlog])
result = defaultdict(list)

for date in dataset:
    for enb in dataset[date]:
        # Check if data for both sets exists
        if "Occurrence" in dataset[date][enb] and \
           "pmRadioThpVolUl" in dataset[date][enb]:
            # read data into the various
            moment = dataset[date][enb]
            vol = moment['pmRadioThpVolUl'] * 128
            payload = moment['Payload size']
            occurrence = moment['Occurrence']
            s1 = moment['pmS1SigConnEstabSucc']
            # Do not continue if any is zero
            if occurrence * vol * s1:
                ratio = vol / s1
                average = int(payload / occurrence)
                if ratio < 2000:
                    result[average].append(ratio)

payloads, means, uppers, lowers = [], [], [], []

# Time for statistical analysis to include error bars
for occurrence in sorted(result):
    if len(result[occurrence]) > 2:
        payloads.append(occurrence)

        lower, mean, upper = statistics.quantiles(result[occurrence])
        means.append(mean)
        uppers.append(upper - mean)
        lowers.append(mean - lower)

plt.subplots(figsize=(8, 4.5))
plt.errorbar(payloads, means, yerr=[lowers, uppers], elinewidth=3,
             label='Measured')
offset = 64+28
plt.plot(range(0, 1088, 64), range(offset, 1088+offset, 64),
         label='Predictor')
plt.xlabel("Payload size per connection")
plt.ylabel("MAC layer volume per connection")
plt.legend()
plt.savefig('payloadmap.pdf', bbox_inches='tight')
