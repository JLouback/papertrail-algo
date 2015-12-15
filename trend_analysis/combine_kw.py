__author__ = 'julianalouback'

import csv
import json
import urllib
import re

def clean(word):
    word =  word.lower()
    return re.sub(r"^\W+|\W+$", "", word)

def combine_kw():
    dblp = open('missed.csv', 'r')
    csvfile = open('missed-done.csv', 'wb')
    errorcases = open('misserror.txt', 'wb')
    apikey = '86b1fdd5efa09f899c8cd52a3ca4572f7d1aa1bc'
    reader = csv.reader(dblp, delimiter=',', quotechar='\"')
    writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
    for row in reader:
        abstract = row[7]
        abstract = abstract.replace('&', ' ')
        abstract = abstract.replace(' ', '%20')
        url = 'http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords?apikey={0}&outputMode=json&text={1}'.format(apikey, abstract)
        response = urllib.urlopen(url)
        try:
            data = json.loads(response.read())
            keywords = ''
            try:
                for entry in data['keywords']:
                    keywords += clean(entry['text'].encode('utf-8')) + ':' + entry['relevance'].encode('utf-8') + ';'
                row.append(keywords)
                [x.decode('utf-8') for x in row]
                writer.writerow(row)
            except KeyError:
                errorcases.write(url)
        except ValueError:
            errorcases.write(url)
    csvfile.close()
    dblp.close()
    errorcases.close()

if __name__ == '__main__':
    combine_kw()