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


dataset = defaultdict(lambda: [])

for filename in os.listdir('bestfriend.deception.training'):
    with open('bestfriend.deception.training' + '/' + filename) as f:
        text = f.read()
        dataset[filename] = helper.preProcess(text)

doc_cnt = 195

correct_cnt = 0

for testfile, testwords in dataset.items():
    lie_cnt = 0
    true_cnt = 0
    n_true = 0
    n_lie = 0
    plie = 0
    ptrue = 0
    vocabularyset = defaultdict(int)
    lievocabset = defaultdict(int)
    truevocabset = defaultdict(int)

    for word in testwords:
        vocabularyset[word] += 1

    for trainfile, trainwords in dataset.items():
        if trainfile != testfile:
            if trainfile[0] == 'l':
                lie_cnt += 1
                for word in trainwords:
                    lievocabset[word] += 1
                    n_lie += 1
            else:
                true_cnt += 1
                for word in trainwords:
                    truevocabset[word] += 1
                    n_true += 1

    plie = lie_cnt/doc_cnt
    ptrue = true_cnt/doc_cnt
    for word, cnt in vocabularyset.items():
        plie *= (lievocabset[word]+1)/(n_lie+len(vocabularyset))
        ptrue *= (truevocabset[word]+1)/(n_true+len(vocabularyset))

    if (plie >= ptrue):
        print 'testfile \'' + testfile + '\' evaluated as lie'
        if (testfile[0] == 'l'):
            correct_cnt += 1
            print 'correct!\n'
        else:
            print 'incorrect!\n'
    else:
        print 'testfile \'' + testfile + '\' evaluated as true'
        if (testfile[0] == 't'):
            correct_cnt += 1
            print 'correct!\n'
        else:
            print 'incorrect!\n'

print 'accuracy is ' + str(correct_cnt/196)








