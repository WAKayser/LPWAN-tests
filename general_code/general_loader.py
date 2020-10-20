#
#   Library file for unifying interface for both SQL results, storing results
#       and loading stored queries.
#   Also contains code for combining different log files.
#
#   Wouter Kayser 2020
#


from collections import defaultdict
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import pyodbc


def sum_dicts(dicts):
    # Similar to how counters can be summed. But now for the general
    # type of dicts
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


def sql_query(file, key='../default.key', header=True):
    # Executes a query on the server defined by the key
    # Can also skip the header if needed.
    # Operates nicely as a generator to save resources.
    with open(key, 'r') as keyfile:
        conn = pyodbc.connect(keyfile.read())

    with open(file, 'r') as query_file:
        query = query_file.read()

    cursor = conn.cursor()
    cursor.execute(query)

    if header:
        yield [i[0] for i in cursor.description]

    for row in cursor:
        yield(row)


def store_sql(file, key='../default.key', header=True):
    # Used to store the outcome of an SQL query so it can be used later
    # Includes a time stamp
    stamp = datetime.now().strftime('%Y%m%d %H %M %S')
    name = file + stamp + '.bckup'

    with open(name, 'w', newline='') as bckup:
        reader = sql_query(file, key, header)
        writer = csv.writer(bckup)
        for row in reader:
            writer.writerow(row)
            yield row


def csvreader(file, sep='\t', header=True):
    # Simple CSV reader wrapper to handle headers
    # Exposes a nice generator again.
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=sep)
        if not header:
            next(reader)
        while(True):
            try:
                yield next(reader)
            except StopIteration:
                return


def load_dict(reader, max_index=1):
    # Mainly used to load counter values from eNodeBs into dictionaries
    # However is not recommended to use, as more processing often needs to
    # happen on the database.

    # Dictionaries are nested to attempt to gain some structure.

    def convtime(str_date):
        # Function to convert time into the python representation.
        return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.0000000')

    headers = next(reader)
    if max_index == 1:
        timeseries = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for row in reader:
            time, enb = convtime(row[0]), row[1]
            for value, counter in enumerate(headers[2:]):
                if row[value+2] != 'NULL':
                    timeseries[time][enb][counter] = int(row[value+2])
    else:
        timeseries = defaultdict(lambda: defaultdict(
                                 lambda: defaultdict(
                                    lambda: [0 for x in range(max_index)])))
        for row in reader:
            time, enb, index = convtime(row[0]), row[1], int(row[2])
            for value, counter in enumerate(headers[3:]):
                if row[value+3] != 'NULL':
                    timeseries[time][enb][counter][index] = int(row[value+3])

    return timeseries


def print_dict(target):
    # Function that could be used to print a nested dict such
    # such as created by the previous function
    for time in target:
        for enb in target[time]:
            print(time, '||', enb)
            for counter in target[time][enb]:
                print('\t', counter, ': ', target[time][enb][counter])


def read_log(rows, eNodeB, rat=8):
    # Used to load in the AT-AT log of sent messages
    # eNodeB is used to match the dict structure to earlier used methods
    # rat can be used to select only the NB-IoT activity.
    headers = next(rows)
    timeseries = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for row in rows:
        if int(row[-1]) == rat:
            # Again most code is used for time manipulation
            time = datetime(2020,
                            int(row[0]),
                            int(row[1]),
                            hour=int(row[2]),
                            minute=int(row[3])*15)

            timeseries[time][eNodeB]['Payload size'] += int(row[-2])
            timeseries[time][eNodeB]['Occurrence'] += 1
    return timeseries


def combine_ts(sets):
    # Can be used to combine the timeseries dicts created earlier
    # can be used to combine logs and counters
    result = defaultdict(lambda: defaultdict(dict))
    for ts in sets:
        for date in ts.keys():
            for enb in ts[date].keys():
                result[date][enb].update(ts[date][enb])
    return result


def try_store(file):
    # Simple helper function for windows based systems, as some pdf or image
    # readers lock the file while viewing.
    try:
        plt.savefig(file)
        print(f'Saved file as {file}')
    except Exception:
        print("Remember that you are on windows")
        try_store('new_' + file)
