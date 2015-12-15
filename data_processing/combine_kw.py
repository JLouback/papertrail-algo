__author__ = 'julianalouback'
""" Script to process the abstracts using alchemy and add the results from the Keyword Extractor to the dataset.
    Must have authority scores file and data file in same directory.
"""

import csv
import json
import urllib
import re
import os

def clean(word):
    word =  word.lower()
    return re.sub(r"^\W+|\W+$", "", word)

def combine_kw():
    db = open('data.csv', 'r')
    csvfile = open('data-kw.csv', 'wb')
    errorcases = open('data-error.txt', 'wb')
    apikey = os.environ.get('ALCHEMY_KEY')
    reader = csv.reader(db, delimiter=',', quotechar='\"')
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
    db.close()
    errorcases.close()

if __name__ == '__main__':
    combine_kw()