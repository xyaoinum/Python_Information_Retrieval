#name: Yao Xiao (xyaoinum)

import sys
import os
import re
from collections import defaultdict
import operator
import urllib2
import shutil
from stemmer import *
import robotparser
import time

#I parse the robots.txt under eecs.umich.edu and apply it to all umich domain
#because first, I couldn't find any robots.txt other than this that has something
#disallow, second, I tried to parse different robots.txt for every webpage.
#But the running speed becomes very slow that I couldn't finish them in an hour.
rp = robotparser.RobotFileParser()
urlRobots = 'http://www.eecs.umich.edu/robots.txt'
rp.set_url(urlRobots)
rp.read()

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

#add www to url without a www, remove www to url with a www
#for the purpose to elimite the same url
def changeWWW(urlIn):
    if re.match(r'^http://www[.].*', urlIn):
        return urlIn.replace('www.', '')
    else:
        return urlIn.replace('http://', 'http://www.')


#return the set of all the htmls in the page source of urlIn
#all the html is in the format http://....html
#remove the html that is robot excluded
#exclude all href other than html, such as .gif, .pdf, ...
#remove all fragment
#remove all duplicate result
#remove all query
def findAllHtml(urlIn):

    pattern = r'a href=\"(.*?)\"'
    urlSet = allPatternsFromUrl(urlIn, pattern)


    for i in range(len(urlSet)):
        #remove #<fragment>
        if urlSet[i].find('#') != -1:
            urlSet[i] = re.sub(r'#.*', '', urlSet[i])
        #remove ?<query> (we do not convert any query url, because it's hard to convert them to html form and is hard to ensure no duplicate urls)
        if urlSet[i].find('?') != -1:
            urlSet[i] = re.sub(r'[?].*', '', urlSet[i])

    frontUrl = re.findall(r'(http://.*?)/', urlIn)[0]
    noTailUrl = re.findall(r'(http://.*/)[^.]+[.][^.]+', urlIn)[0]
    

    for i in range(len(urlSet)):
        #complete the relative address
        if re.match(r'^/.*', urlSet[i]):
            urlSet[i] = frontUrl + urlSet[i]
        elif re.match(r'^\w+.*', urlSet[i]) and not re.match(r'^http.*', urlSet[i]):
            urlSet[i] = noTailUrl + urlSet[i]
        #add index.html to an incomplete path
        if re.match(r'.*/$', urlSet[i]):
            urlSet[i] += 'index.html'
        elif re.match(r'.*/[^.]+$', urlSet[i]) or not re.match(r'http://.+/.+', urlSet[i]):
            urlSet[i] += '/index.html'
    
    #use dictionary to remove duplicate
    d = defaultdict(int)
    for w in urlSet:
        if re.match(r'^http://.*/.*[.]html$', w):
            front = re.findall(r'(http://.*?)/', w)[0]
            #detect if in the umich domain and obey the robot.txt
            if re.match(r'.*umich.*', front) and rp.can_fetch('*', w):
                if not d[w] > 0 and not d[changeWWW(w)] > 0:
                    d[w] = 1
    return d
resultSet = []
urlQueue = []
visitedUrl = defaultdict(int)

initial = 'http://www.eecs.umich.edu/index.html'

urlQueue.append(initial)

if os.path.isfile('hw1ans5'):
    os.remove('hw1ans5')

fw = open('hw1ans5','a')

#applying the breadth first search algorithm
while len(urlQueue) > 0 and len(resultSet) < 1500:
    theUrl = urlQueue[0]
    urlQueue.remove(theUrl)
    #detect if the url has been visited
    if not visitedUrl[theUrl] > 0 and not visitedUrl[changeWWW(theUrl)] > 0:
        visitedUrl[theUrl] = 1
        content = ''
        #add a waiting time 1 second so as to be polite to the sever
        time.sleep(1)
        try:
            content = urllib2.urlopen(theUrl).read()
        except:
            content = ''
        #detect if the url is accessible
        if not re.match(r'.*404 Not Found.*', content) and not re.match(r'.*This page does not seem to exist.*', content): 
            print(theUrl)
            resultSet.append(theUrl)
            fw.write(theUrl + '\n')
            tmpD = findAllHtml(theUrl)
            for w in tmpD:
                urlQueue.append(w)

fw.close()

print 'hw1ans5 done!'





















