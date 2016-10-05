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

def makeBigramDict(s):
    result = defaultdict(int)
    allWords = re.findall(r'[a-zA-Z]+',s)
    for word in allWords:
        i = 0
        while i < len(word) - 1:
            result[word[i:i+2].lower()] += 1
            i += 1
    return result

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

test = []
solution = []
engDict = defaultdict(int)
freDict = defaultdict(int)
itaDict = defaultdict(int)

with open('language.identification' + '/' + 'test') as f:
    text = f.read()
    test = re.split(r'[\n\r]+', text)
while len(test) > 300:
    del test[300]

with open('language.identification' + '/' + 'solution') as f:
    text = f.read()
    solution = re.split(r'[\n\r]+', text)
while len(solution) > 300:
    del solution[300]

with open('language.identification/training' + '/' + 'English') as f:
    text = f.read()
    engDict = makeBigramDict(text)

with open('language.identification/training' + '/' + 'French') as f:
    text = f.read()
    freDict = makeBigramDict(text)

with open('language.identification/training' + '/' + 'Italian') as f:
    text = f.read()
    itaDict = makeBigramDict(text)

eng_cnt = file_len('language.identification/training' + '/' + 'English')
fre_cnt = file_len('language.identification/training' + '/' + 'French')
ita_cnt = file_len('language.identification/training' + '/' + 'Italian')
total_cnt = eng_cnt + fre_cnt + ita_cnt
peng = eng_cnt/total_cnt
pfre = fre_cnt/total_cnt
pita = ita_cnt/total_cnt

i = 0
correct_cnt = 0
for sentence in test:
    peng = eng_cnt/total_cnt
    pfre = fre_cnt/total_cnt
    pita = ita_cnt/total_cnt
    sentenceDict = defaultdict(int)
    sentenceDict = makeBigramDict(sentence)
    for word, freq in sentenceDict.items():
        peng *= (engDict[word]+1)/(freq+len(sentence))
        pfre *= (freDict[word]+1)/(freq+len(sentence))
        pita *= (itaDict[word]+1)/(freq+len(sentence))
    if(peng >= pfre and peng >= pita):
        print 'sentence ' + str(i+1) + ' evaluated as English'
        if(solution[i] == str(i+1) + ' English'):
            correct_cnt += 1
            print 'correct!\n'
        else:
            print 'incorrect!\n'
    elif(pfre>=pita):
        print 'sentence ' + str(i+1) + ' evaluated as French'
        if(solution[i] == str(i+1) + ' French'):
            correct_cnt += 1
            print 'correct!\n'
        else:
            print 'incorrect!\n'
    else:
        print 'sentence ' + str(i+1) + ' evaluated as Italian'
        if(solution[i] == str(i+1) + ' Italian'):
            correct_cnt += 1
            print 'correct!\n'
        else:
            print 'incorrect!\n'
    i += 1

print 'accuracy is ' + str(correct_cnt/300)













