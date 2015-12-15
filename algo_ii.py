__author__ = 'julianalouback'
""" The Inverted Index Algorithm
    See documentation for detailed explanation
"""

import csv

csv.field_size_limit( 2**30 )   # was sys.maxsize

# Threshold for relevance of keywords
THRESHOLD = 0.6

keywords_docsrels = {}

# Populates a dictionary with the keywords and corresponding documents/relevance scores
def populate_iks_dict():
    with open( 'keywordscores.csv', 'r' ) as iks_file:
        reader = csv.reader( iks_file, delimiter=',', quotechar='\"' )
        for row in reader:
            docsrels = row[1].split(';')
            del docsrels[-1]
            keywords_docsrels[ row[0] ] = docsrels

# Returns scores for documents based on keyword relevance and authority score.
def get_scores(keywords, authorities):
    # NOTE: What if we see a keyword (in 'keywords') that isn't in the dict?
    # We ignore it. (For now, at least.)
    docs = {}
    # Add doc relevance scores to doc entries
    for keyword in keywords:
        if keyword in keywords_docsrels:
            scores = keywords_docsrels[keyword]
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

# Returns list of recommended citations sorted in descending order of final score
def predict_citations( candidates, authorities ):
    keywords = []
    for candidate in candidates:
        # TODO: We should probably drop keywords that contain ':'
	colon = candidate.rfind(':')
	keyword = candidate[:colon]
	# NOTE: Some keywords don't have a score, e.g. ID 747316's "durp" keyw
	try:
	    relevance = float( candidate[colon+1:] )
        except ValueError:
            break
        # Ignore doc_ids less than threshold
        if relevance < THRESHOLD:
            break
        keywords.append(keyword)
    # dictionary of top k recommended documents and a score
    scores = get_scores(keywords, authorities)
    return scores

if __name__ == '__main__':
    predict_citations('134807')
