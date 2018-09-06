import json

from get_stats import get_stats

# Getting the Data

N = 1500
date = '2018-08-27'

players = get_stats(N, date)

# Saving the Data

name = 'atp_python_' + date + '_1-' + str(N) + '.json'

with open(name, 'w') as f:
    for dic in players:
        json.dump(dic, f)
        f.write('\n')

# Opening the Data

# with open(name) as d:
#     contents = [json.loads(line) for line in d]
#
# print(contents)
