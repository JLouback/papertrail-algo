__author__ = 'julianalouback'

import csv
import sys

csv.field_size_limit(sys.maxsize)

# For a list of keywords, returns a dict with keyword as key and list of doc:relevance_score values
def get_relevance(keywords):
    data = open('keywordscores.csv', 'r')
    reader = csv.reader(data, delimiter=',', quotechar='\"')
    counter = 0
    all_scores = {}
    for row in reader:
        kw = row[0]
        if kw in keywords:
            counter += 1
            scores = row[1].split(';')
            del scores[-1]
            all_scores[kw] = scores
            if counter == len(keywords):
                break
    return all_scores

def get_scores(keywords, authorities):
    docs = {}
    all_scores = get_relevance(keywords)
    # Add doc relevance scores to doc entries
    for keyword in all_scores.keys():
        scores = all_scores[keyword]
        for entry in scores:
            doc = entry.split(':')[0]
            score = entry.split(':')[1]
            try:
                docs[doc] = docs[doc] + float(score)
            except KeyError:
                docs[doc] = float(score)
    # Add authority score to doc entries, remove docs with 0 authority
    for doc in docs.keys():
        try:
            authority = authorities[doc]
            docs[doc] = docs[doc] + (100 * authority)
        except KeyError:
            del docs[doc]
    # Sort and return top 20
    top = {}
    for (key,value) in sorted(docs.iteritems(), key=lambda x:-x[1])[:20]:
        top[key] = value
    return top


def predict_citations(index, candidates, authorities):
    threshold = 0.6
    keywords = []
    for candidate in candidates:
        keyword = candidate.split(':')[0]
        relevance = float(candidate.split(':')[1])
        # Ignore keywords less than threshold
        if relevance < threshold:
            break
        keywords.append(keyword)
    # dictionary of top k recommended documents and a score
    scores = get_scores(keywords, authorities)
    return scores

if __name__ == '__main__':
    predict_citations('134807')