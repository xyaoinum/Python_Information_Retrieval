#name: Yao Xiao (xyaoinum)
from __future__ import division
import os
import re
from collections import defaultdict
import operator
import urllib2
import shutil
from stemmer import *
import math
import helper

relevanceUrl = 'http://web.eecs.umich.edu/~mihalcea/courses/498IR/Resources/cranfield.reljudge'
query_doc_set = helper.allPatternsFromUrl(relevanceUrl, r'\w+')
query_doc_table = defaultdict(lambda: defaultdict(int))
i = 0
while i < len(query_doc_set):
    query_doc_table[query_doc_set[i]][query_doc_set[i+1]] = 1
    i += 2

queryUrl = 'http://web.eecs.umich.edu/~mihalcea/courses/498IR/Resources/cranfield.queries'
query_set = helper.allPatternsFromUrl(queryUrl, r'[^\n]+')


#TF/IDF mode without normalization
mode = '1'
term_doc_freq = defaultdict(lambda: defaultdict(int))
doc_term_freq = defaultdict(lambda: defaultdict(int))
doc_term_weight = defaultdict(lambda: defaultdict(int))
doc_length = defaultdict(int)
doc_maxtf = defaultdict(int)

for filename in os.listdir('cranfieldDocs'):
    with open('cranfieldDocs' + '/' + filename) as f:
        text = f.read()
        helper.addIndex(doc_term_freq, term_doc_freq, text, filename)

for doc, terms in doc_term_freq.items():
    for term, f in terms.items():
        if(f > doc_maxtf[doc]):
            doc_maxtf[doc] = f

for term, doc in term_doc_freq.items():
    for docId, f in doc.items():
        tf = term_doc_freq[term][docId]
        if(mode == '2'):
            tf /= doc_maxtf[docId]
        idf = len(doc_term_freq)/len(term_doc_freq[term])
        doc_term_weight[docId][term] = math.log((1+tf),10)*math.log(idf,10)

for docId, terms in doc_term_weight.items():
    for term, weight in terms.items():
        doc_length[docId] += doc_term_weight[docId][term]*doc_term_weight[docId][term]
    doc_length[docId] = math.sqrt(doc_length[docId])


relevant_retrieved_10 = 0
retrieved_10 = 10*225
relevant_retrieved_50 = 0
retrieved_50 = 50*225
relevant_retrieved_100 = 0
retrieved_100 = 100*225
relevant_retrieved_500 = 0
retrieved_500 = 500*225
relevant = 0

queryNumber = 1

for query in query_set:

    term_query_freq = defaultdict(int)
    query_term_weight = defaultdict(int)
    query_length = 0;
    query_maxtf = 1
    
    helper.makeIndex(term_query_freq, query)
    
    for term, f in term_query_freq.items():
        if(f > query_maxtf):
            query_maxtf = f

    for term, f in term_query_freq.items():
        tf = term_query_freq[term]
        if(mode == '2'):
            tf /= query_maxtf
        idf = 0
        if len(term_doc_freq[term]) > 0:
            idf = len(doc_term_freq)/len(term_doc_freq[term])
            query_term_weight[term] = math.log((1+tf),10)*math.log(idf,10)
        else:
            query_term_weight[term] = 0

    for term, f in term_query_freq.items():
        query_length += query_term_weight[term]*query_term_weight[term]
    query_length = math.sqrt(query_length)

    doc_query_score = defaultdict(int)
    doc_list = defaultdict(int)
    for term, w in query_term_weight.items():
        for docId, f in term_doc_freq[term].items():
            doc_list[docId] = 1

    for d, cnt in doc_list.items():
        for term, w in query_term_weight.items():
            doc_query_score[d] += doc_term_weight[d][term]*query_term_weight[term]
        doc_query_score[d] = doc_query_score[d]/(doc_length[d]*query_length)

    relevant += len(query_doc_table[str(queryNumber)])

    count = 0
    for d in sorted(doc_query_score, key = doc_query_score.get, reverse = True):
        count += 1
        if query_doc_table[str(queryNumber)][helper.cutZero(d)] == 1:
            if count <= 10:
                relevant_retrieved_10 += 1
                relevant_retrieved_50 += 1
                relevant_retrieved_100 += 1
                relevant_retrieved_500 += 1
            elif count <= 50:
                relevant_retrieved_50 += 1
                relevant_retrieved_100 += 1
                relevant_retrieved_500 += 1
            elif count <= 100:
                relevant_retrieved_100 += 1
                relevant_retrieved_500 += 1
            elif count <= 500:
                relevant_retrieved_500 += 1                
    queryNumber += 1

p10 = relevant_retrieved_10/retrieved_10
r10 = relevant_retrieved_10/relevant

p50 = relevant_retrieved_50/retrieved_50
r50 = relevant_retrieved_50/relevant

p100 = relevant_retrieved_100/retrieved_100
r100 = relevant_retrieved_100/relevant

p500 = relevant_retrieved_500/retrieved_500
r500 = relevant_retrieved_500/relevant

print "TF/IDF without normalization"
print "top 10 doc, precision, recall: ", p10, r10
print "top 50 doc, precision, recall: ", p50, r50
print "top 100 doc, precision, recall: ", p100, r100
print "top 500 doc, precision, recall: ", p500, r500



#TF/IDF mode without normalization
mode = '2'

doc_term_weight.clear()
doc_length.clear()

for term, doc in term_doc_freq.items():
    for docId, f in doc.items():
        tf = term_doc_freq[term][docId]
        if(mode == '2'):
            tf /= doc_maxtf[docId]
        idf = len(doc_term_freq)/len(term_doc_freq[term])
        doc_term_weight[docId][term] = math.log((1+tf),10)*math.log(idf,10)

for docId, terms in doc_term_weight.items():
    for term, weight in terms.items():
        doc_length[docId] += doc_term_weight[docId][term]*doc_term_weight[docId][term]
    doc_length[docId] = math.sqrt(doc_length[docId])

query_doc_table = defaultdict(lambda: defaultdict(int))
i = 0
while i < len(query_doc_set):
    query_doc_table[query_doc_set[i]][query_doc_set[i+1]] = 1
    i += 2

relevant_retrieved_10 = 0
retrieved_10 = 10*225
relevant_retrieved_50 = 0
retrieved_50 = 50*225
relevant_retrieved_100 = 0
retrieved_100 = 100*225
relevant_retrieved_500 = 0
retrieved_500 = 500*225
relevant = 0

queryNumber = 1

for query in query_set:

    term_query_freq = defaultdict(int)
    query_term_weight = defaultdict(int)
    query_length = 0;
    query_maxtf = 1
    
    helper.makeIndex(term_query_freq, query)
    
    for term, f in term_query_freq.items():
        if(f > query_maxtf):
            query_maxtf = f

    for term, f in term_query_freq.items():
        tf = term_query_freq[term]
        if(mode == '2'):
            tf /= query_maxtf
        idf = 0
        if len(term_doc_freq[term]) > 0:
            idf = len(doc_term_freq)/len(term_doc_freq[term])
            query_term_weight[term] = math.log((1+tf),10)*math.log(idf,10)
        else:
            query_term_weight[term] = 0

    for term, f in term_query_freq.items():
        query_length += query_term_weight[term]*query_term_weight[term]
    query_length = math.sqrt(query_length)

    doc_query_score = defaultdict(int)
    doc_list = defaultdict(int)
    for term, w in query_term_weight.items():
        for docId, f in term_doc_freq[term].items():
            doc_list[docId] = 1

    for d, cnt in doc_list.items():
        for term, w in query_term_weight.items():
            doc_query_score[d] += doc_term_weight[d][term]*query_term_weight[term]
        doc_query_score[d] = doc_query_score[d]/(doc_length[d]*query_length)

    relevant += len(query_doc_table[str(queryNumber)])

    count = 0
    for d in sorted(doc_query_score, key = doc_query_score.get, reverse = True):
        count += 1
        if query_doc_table[str(queryNumber)][helper.cutZero(d)] == 1:
            if count <= 10:
                relevant_retrieved_10 += 1
                relevant_retrieved_50 += 1
                relevant_retrieved_100 += 1
                relevant_retrieved_500 += 1
            elif count <= 50:
                relevant_retrieved_50 += 1
                relevant_retrieved_100 += 1
                relevant_retrieved_500 += 1
            elif count <= 100:
                relevant_retrieved_100 += 1
                relevant_retrieved_500 += 1
            elif count <= 500:
                relevant_retrieved_500 += 1                
    queryNumber += 1

p10 = relevant_retrieved_10/retrieved_10
r10 = relevant_retrieved_10/relevant

p50 = relevant_retrieved_50/retrieved_50
r50 = relevant_retrieved_50/relevant

p100 = relevant_retrieved_100/retrieved_100
r100 = relevant_retrieved_100/relevant

p500 = relevant_retrieved_500/retrieved_500
r500 = relevant_retrieved_500/relevant

print "\nTF/IDF with normalization"
print "top 10 doc, precision, recall: ", p10, r10
print "top 50 doc, precision, recall: ", p50, r50
print "top 100 doc, precision, recall: ", p100, r100
print "top 500 doc, precision, recall: ", p500, r500











