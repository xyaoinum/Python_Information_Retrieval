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

mode = '1'
queryList = ['computer science', 'electrical engineering', 'undergrauate program', 'prospective students', 'scholarships']

term_doc_freq = defaultdict(lambda: defaultdict(int))
doc_term_freq = defaultdict(lambda: defaultdict(int))
doc_term_weight = defaultdict(lambda: defaultdict(int))
doc_length = defaultdict(int)

doc_maxtf = defaultdict(int)

allUrl = []

with open ('umichUrlList')as f:
    text = f.read()
    allUrl = re.findall(r'[^\n]+', text)

for url in allUrl:
    text = ''
    try:
        page = urllib2.urlopen(url)
        text = page.read()
        helper.addIndex(doc_term_freq, term_doc_freq, text, url)
    except:
        text = ''
        helper.addIndex(doc_term_freq, term_doc_freq, text, url)

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



for query in queryList:

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
        if(term_doc_freq.has_key(term)):
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

    i = 0
    print 'query: ' , query
    print 'result: '
    for d in sorted(doc_query_score, key = doc_query_score.get, reverse = True):
        print d
        i += 1
        if i == 10:
            print '\n'
            break







