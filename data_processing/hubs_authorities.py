__author__ = 'julianalouback'
""" Implementation of hubs and authorities algorithm (traditional)
    Only authority scores are saved.
"""

import csv
import math

def normalize(scores):
    l2 = math.sqrt(sum(i**2 for i in scores.values()))
    for index in scores:
        scores[index] = scores[index]/l2

def update_authorities(hubs, authorities, associations):
    for index in authorities:
        try:
            references = associations[index]['referencedBy']
            updated = 0.0
            for reference in references.split(';'):
                updated += float(hubs[reference])
            authorities[index] = updated
        except KeyError:
            pass
    normalize(authorities)

def update_hubs(hubs, authorities, associations):
    for index in hubs:
        try:
            references = associations[index]['references']
            updated = 0.0
            for reference in references.split(';'):
                updated += float(authorities[reference])
            hubs[index] = updated
        except KeyError:
            pass
    normalize(hubs)

# Write only authorities scores
def write_authorities(authorities):
    output = open('authorities_scores.csv', 'wb')
    writer = csv.writer(output, delimiter=',')
    for index, score in authorities.iteritems():
        writer.writerow([index,str(score)])


# Hubs & Authorities algorithm
def hubs_authorities():
    k = 5
    dblp = open('data.csv', 'r')
    reader = csv.reader(dblp, delimiter=',', quotechar='\"')
    associations = dict()
    hubs = dict()
    authorities = dict()
    # Initialize citations dict for 'association matrix', ref_num = round 1 of hubs
    reader.next()
    for row in reader:
        index = row[0]
        references = row[5]
        ref_num = row[6]
        associations[index] = {'references': references}
        for reference in references.split(';'):
            authorities[reference] = 0.0
            try:
               associations[reference]['referencedBy'] = associations[reference]['referencedBy'] + ';' + index
            except KeyError:
               associations[reference] = {'referencedBy':index}
        hubs[index] = float(ref_num)

    normalize(hubs)

    # Uptade hubs and authorities score up to k times
    for i in range(0, k):
        update_authorities(hubs, authorities, associations)
        update_hubs(hubs, authorities, associations)

    write_authorities(authorities)


if __name__ == '__main__':
    hubs_authorities()