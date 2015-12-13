__author__ = 'julianalouback'

import sys
import csv
import re

def clean(word):
    word =  word.lower()
    return re.sub(r"^\W+|\W+$", "", word)

# Data: "INDEX","TITLE","AUTHORS","YEAR","PUB_VENUE","REF_ID","REF_NUM","ABSTRACT","KEYWORDS"
csvfile = open('data-kw-216432.csv', 'r')
reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
for line in reader:
    keywords = line[8]
    year = line[3]
    for keyword in keywords.split(";"):
        if keyword is not "":
            relevance = keyword.split(":")[-1]
            keyword = keyword.split(":0")[0]
            keyword = clean(keyword)
            keyword = re.sub(r"^\W+|\W+$", "", keyword)
            key = "\"" + keyword + "\"_" + year
            print(key)