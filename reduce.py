__author__ = 'julianalouback'

import sys

last = None
count = 0

for line in sys.stdin:

    kw_year = line.strip()

    if not last:
        last = kw_year

    if kw_year == last:
        count += 1
    else:
        result = [last, count]
        kw = last.split('_')[0]
        year = last.split('_')[1]
        print(kw + ',' + year + ',' + str(count))
        last = kw_year
        count = 1

kw = last.split('_')[0]
year = last.split('_')[1]
print(kw + ',' + year + ',' + str(count))