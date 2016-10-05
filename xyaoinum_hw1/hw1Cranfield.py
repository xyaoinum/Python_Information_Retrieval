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


#given a url and a pattern, find all the patterns in the source of the webpage for
#this url, return a list of intented patterns
def allPatternsFromUrl(urlIn, patternIn):
    url = urlIn
    content = []
    try:
        page = urllib2.urlopen(url)
        content = page.read()
        return re.findall(patternIn, content)
    except:
        return content

#tokenize the content of all the files in the path, return a list
#of tokens
def allTokensFromPath(pathIn):
    allTokens = []
    for filename in os.listdir(pathIn):
        filedir = pathIn
        with open(filedir + '/' + filename) as f:
            data = f.read()
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

            allTokens += allResult + allDate + allNum + allAcro + allPhrase + allPoss

            for i in range(len(allPoss)):
                allTokens.append('\'s')

    return allTokens

#change the token collection into vocabulary collection, with their frequency
def makeDict(allTokens):
    tokenDict = defaultdict(int)
    for w in allTokens:
        tokenDict[w] += 1
    return tokenDict


#code for question 1############################################################################
if os.path.isfile('hw1ans1'):
    os.remove('hw1ans1')

fw = open('hw1ans1','a')

allTokens = allTokensFromPath('cranfieldDocs')
for w in allTokens:
    fw.write(w + '\n')

fw.close()

print 'hw1ans1 done!'

#code for question 2############################################################################
if os.path.isfile('hw1ans2'):
    os.remove('hw1ans2')

fw = open('hw1ans2','a')

tokenDict = makeDict(allTokens)
tokenCount = len(allTokens)

#total number of words
fw.write('(a): ' + str(tokenCount) + '\n\n')

#vocabulary size
fw.write('(b): ' + str(len(tokenDict)) + '\n\n')

#top 20 words
fw.write('(c): \n')

fw.write('token | occurence\n')

fw.write('--------------------\n')

topTwenty = []
i = 0
for token in sorted(tokenDict, key = tokenDict.get, reverse = True):
    if i < 20:
        fw.write(str(token) + '    ' + str(tokenDict[token]) + '\n')
        topTwenty.append(token)
        i += 1
    else:
        break

#stopwords in those top 20 words
fw.write('\n(d): \n')
url = 'http://web.eecs.umich.edu/~mihalcea/courses/498IR/Resources/stopwords'
allStopWords = allPatternsFromUrl(url, r'\w+')
stopWordsDict = makeDict(allStopWords)
for w in topTwenty:
    if stopWordsDict[w] > 0:
        fw.write(w + '\n')

#number of unique words accounting for 25% of the total number of words
tmpSum = 0
numVocab = 0
for token in sorted(tokenDict, key = tokenDict.get, reverse = True):
    tmpSum += tokenDict[token]
    numVocab += 1
    if tmpSum >= tokenCount/4:
        break
    
fw.write('\n(e): ' + str(numVocab) + '\n')

fw.close()

print 'hw1ans2 done!'

#code for question 3############################################################################

if os.path.isfile('hw1ans3'):
    os.remove('hw1ans3')

fw = open('hw1ans3','a')

#I pick two subset:
#subset100: contain cranfield0001 - cranfield0100
#subset500: contain cranfield0201 - cranfield0700
#create a directory 'subset100', copy cranfield0001 - cranfield0100
#into the directory and rename by 0001 - 0100

if os.path.exists('subset100'):
    shutil.rmtree('subset100')

os.makedirs('subset100')

fourDigit = '0000'
for i in range(100):
    src = 'cranfieldDocs/cranfield'
    if i < 9:
        fourDigit = '000' + str(i + 1)
    elif i < 99:
        fourDigit = '00' + str(i + 1)
    elif i < 999:
        fourDigit = '0' + str(i + 1)
    else:
        fourDigit = str(i + 1)
    src += fourDigit

    dst = 'subset100/' + fourDigit
    shutil.copyfile(src, dst)

#create a directory 'subset500', copy cranfield0201 - cranfield0700
#into the directory and rename by 0201 - 0700
if os.path.exists('subset500'):
    shutil.rmtree('subset500')

os.makedirs('subset500')

for i in range(500):
    src = 'cranfieldDocs/cranfield'
    if i + 200 < 9:
        fourDigit = '000' + str(i + 201)
    elif i + 200 < 99:
        fourDigit = '00' + str(i + 201)
    elif i + 200 < 999:
        fourDigit = '0' + str(i + 201)
    else:
        fourDigit = str(i + 201)
    src += fourDigit

    dst = 'subset500/' + fourDigit
    shutil.copyfile(src, dst)

#calculate the number of word and vocabulary for each subset

allTokens100 = allTokensFromPath('subset100')
allTokens500 = allTokensFromPath('subset500')
tokenDict100 = makeDict(allTokens100)
tokenDict500 = makeDict(allTokens500)
n1 = len(allTokens100)
v1 = len(tokenDict100)
n2 = len(allTokens500)
v2 = len(tokenDict500)

beta = math.log(v1/v2)/math.log(n1/n2)
k = v1/(math.pow(n1, beta))

fw.write('beta = ' + str(beta) + '\n')
fw.write('K = ' + str(k) + '\n\n')

fw.close()

if os.path.exists('subset100'):
    shutil.rmtree('subset100')
if os.path.exists('subset500'):
    shutil.rmtree('subset500')


print 'hw1ans3 done!'

#code for question 4############################################################################
if os.path.isfile('hw1ans4'):
    os.remove('hw1ans4')

fw = open('hw1ans4','a')

#apply stemmer and stopword eliminator, I firstly eliminate the stop word, and then convert all
#to stem. This is because stopword is meaningless only in the context of original text,
#it's possible that some meaningful text is stemmed into a stopword, so we don't want to
#eliminate those word

newAllTokens = []
p = PorterStemmer()

for w in allTokens:
    if stopWordsDict[w] != 1:
        newAllTokens.append(p.stem(w, 0,len(w)-1))


tokenDict = makeDict(newAllTokens)
tokenCount = len(newAllTokens)

#total number of words
fw.write('(a): ' + str(tokenCount) + '\n\n')

#vocabulary size
fw.write('(b): ' + str(len(tokenDict)) + '\n\n')

#top 20 words
fw.write('(c): \n')

fw.write('token | occurence\n')

fw.write('--------------------\n')

topTwenty = []
i = 0
for token in sorted(tokenDict, key = tokenDict.get, reverse = True):
    if i < 20:
        fw.write(str(token) + '    ' + str(tokenDict[token]) + '\n')
        topTwenty.append(token)
        i += 1
    else:
        break

#stopwords in those top 20 words
fw.write('\n(d): \n')
cnt = 0
for w in topTwenty:
    if stopWordsDict[w] > 0:
        fw.write(w + '\n')
        cnt += 1
if cnt == 0:
    fw.write('no stopwords in the top 20 words\n')

fw.close()

print 'hw1ans4 done!'
        
