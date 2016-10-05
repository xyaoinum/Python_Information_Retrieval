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

def allPatternsFromUrl(urlIn, patternIn):
    url = urlIn
    content = []
    try:
        page = urllib2.urlopen(url)
        content = page.read()
        return re.findall(patternIn, content)
    except:
        return content

def tokenization(data):

    #eliminates SGML tags
    data = re.sub(r'<.*>', ' ', data)

    #we only consider the folllowing patterns:
    #(1) word: apple
    #(2) phrase: mother-in-law
    #(3) abbreviation: Mr.
    #(4) acronym: U.S.A.
    #(5) number: "-3.14", "-12,345,67"
    #(6) date: "02/20/2014", "Feb. 20, 2014", "Feburary 20, 2014", "20 Feburary 2014", "2014-02-20" (dates such as 02/02/02 is confusing 
    #    and it's impossible to differentiate between mm/dd/19yy or dd/mm/20yy, so we must make some assumtions. Here we assume the date
    #    follows american standard "mm/dd/yyyy", and we neglect other such as "mm/dd/yy", "dd/mm/yy", "dd/mm/yyyy" ...)
    #(7) possessive: boy's, boys'

    #first, we extract all the date patterns and replace them with a space

    #match "mm/dd/yyyy"
    allDate = re.findall(r'\d\d/\d\d/\d\d\d\d', data)
    data = re.sub(r'\d\d/\d\d/\d\d\d\d', r' ', data)

    #match "MMM dd, yyyy", "mmmm dd, yyyy"
    allDate += re.findall(r'(?:Jan[.]|January|Feb[.]?|Feburary|Mar[.]|March|Apr[.]\
    |April|May[.]|May|Jun[.]|June|Jul[.]|July|Aug[.]|August|Sep[.]|September|Oct[.]\
    |October|Nov[.]|November|Dec[.]|December)[ ]?\d\d, \d\d\d\d', data)
    data = re.sub(r'(?:Jan[.]|January|Feb[.]?|Feburary|Mar[.]|March|Apr[.]\
    |April|May[.]|May|Jun[.]|June|Jul[.]|July|Aug[.]|August|Sep[.]|September|Oct[.]\
    |October|Nov[.]|November|Dec[.]|December)[ ]?\d\d, \d\d\d\d', r' ', data)

    #match "dd mmmm, yyyy"
    allDate += re.findall(r'\d\d[ ](?:January|Feburary|March|April|May|June|July\
    |August|September|November|December), \d\d\d\d', data)
    data = re.sub(r'\d\d[ ](?:January|Feburary|March|April|May|June|July\
    |August|September|November|December), \d\d\d\d', r' ', data)

    #match "yyyy-mm-dd"
    allDate += re.findall(r'\d\d\d\d-\d\d-\d\d', data)
    data = re.sub(r'\d\d\d\d-\d\d-\d\d', r' ', data)

    #second, we extract all the number patterns and replace them with a space

    #match patterns like "12,345,678"
    allNum = re.findall(r'[-]?\d+(?:,\d\d\d)+', data)
    data = re.sub(r'[-]?\d+(?:,\d\d\d)+', r' ', data)

    #match patterns like "123", "123.456", "-123.456"
    allNum += re.findall(r'[-]?\d+(?:[.]\d+)?', data)
    data = re.sub(r'[-]?\d+(?:[.]\d+)?', r' ', data)

    #third, we extract all acronyms and replace them with a space
    allAcro = re.findall(r'\w+(?:[.]\w)+', data)
    data = re.sub(r'\w+(?:[.]\w)+', r' ', data)

    #fourth, we extract all phrases and replace them with a space
    allPhrase = re.findall(r'\w+(?:-\w+)+', data)
    data = re.sub(r'\w+(?:-\w+)+', r' ', data)

    #fifth, we extract all possessive and replace them with a space

    #match patterns like boy's
    allPoss = re.findall(r'([a-zA-Z]+)\'s', data)
    data = re.sub(r'[a-zA-Z]+\'s', r' ', data)

    #match patterns like boys'
    allPoss += re.findall(r'([a-zA-Z]+s)\'', data)
    data = re.sub(r'([a-zA-Z]+s)\'', r' ', data)

    #sixth, we extract all other words, possibly having a "'" in the middle
    #standing for the form: he's, I'm, haven't ... I treat this form as one token. 
    allResult = re.findall(r'\w+[\'\w]*', data)
    data = re.sub(r'\w+[\'\w]*', r' ', data)

    allTokens = allResult + allDate + allNum + allAcro + allPhrase + allPoss

    return allTokens


def lowercase(allTokens):
    return [s.lower() for s in allTokens]

def makeDict(allTokens):
    tokenDict = defaultdict(int)
    for w in allTokens:
        tokenDict[w] += 1
    return tokenDict

stopWordsUrl = 'http://web.eecs.umich.edu/~mihalcea/courses/498IR/Resources/stopwords'
allStopWords = allPatternsFromUrl(stopWordsUrl, r'\w+')
stopWordsDict = makeDict(allStopWords)

def stopwordRemoval(allTokens):
    result = []
    for w in allTokens:
        if(stopWordsDict[w] != 1):
            result.append(w)
    return result

def stemmer(allTokens):
    p = PorterStemmer()
    return [p.stem(w, 0,len(w)-1) for w in allTokens]

def preProcess(s):
    w = tokenization(s)
    w = lowercase(w)
    w = stopwordRemoval(w)
    return stemmer(w)

def addIndex(index, invindex, text, docId):
    allTokens = preProcess(text)
    for w in allTokens:
        invindex[w][docId] += 1
        index[docId][w] += 1

def makeIndex(index, text):
    allTokens = preProcess(text)
    for w in allTokens:
        index[w] += 1

def cutZero(text):
    return re.sub(r'cranfield[0]+', '', text)



