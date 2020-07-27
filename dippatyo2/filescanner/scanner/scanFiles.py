#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir,remove
import sys
import ijson
#import operator
from pprint import pprint
import string
import nltk
import re
from api.models import Word, WordRelation, WordDistance, NicknameOfPoster, DateOfPost
from .keywords import illness_list, treatment_list, death_list, social_list, financial_list

stopwords_file = open("filescanner/scanner/finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()

keyword_list = [illness_list, treatment_list, death_list, social_list, financial_list]

wordcount = {}

data = {"threads" : 0,
        "comments" : 0,
        "wordpairs" : 0}



#check if one of the keywords exist in the given string
def search_keywords(string):
    for num, wordlist in enumerate(keyword_list, start=1):
        for word in wordlist:
            if word in string:
                return num
    return 0

#helper function to add word into the dictionary
def addword(word,dist):
    if word not in wordcount:
        wordcount[word] = addDistance(dist)
    else:
        vals = addDistance(dist)
        obj = wordcount[word]
        for k in vals:
            obj[k] += vals[k]

def createWordDistance(dist):
    wd = WordDistance.objects.createWD(dist)
    return wd

def createWord(word):
    w = Word.objects.createWord(word)
    return w

def createWordPair(word1, word2, dist, date):
    wp = WordRelation.objects.createWordRelation(
            createWord(word1), 
            createWord(word2), 
            createWordDistance(dist), 
            date
        )
    return wp

"""
#writing out to log-file the current contents of wordcount
def writeToFile():
    try:
        remove("logs.txt")
    except OSError:
        pass
    #print(wordcount)
    #sorted_wc = sorted(wordcount.items(),key=operator.itemgetter(1),reverse=True)
    #pprint(wordcount)

    with open("logs.txt","a") as f:
        f.write("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
        f.write("Most common wordpairs in text: \n\n")
        #r= 250 if len(sorted_wc) > 250 else len(sorted_wc)
        #for i in range(0, r):
        i = 0
        for key,val in sorted(wordcount.items(), key=lambda i:sum(i[1].values()),reverse=True):
            #print(key,val)
            f.write("%s,%s,\n\t\t'total': %i,\n\t\t'1-2': 
            %i, \n\t\t'3-5': %i, \n\t\t'6-8': %i,\n\t\t'8-14': %i,\n\t\t'15+': %i'\n\n" %
            (key[0],key[1],sum(val.values()),val['1-2'],val['3-5'],val['6-8'],val['8-14'],val['15+']))
            if (i>300):
                break
            i+=1
        f.close()
"""
#writing out to log-file the current contents of wordcount
def writeToFile():
    try:
        remove("logs.txt")
    except OSError:
        pass
    #print(wordcount)
    #sorted_wc = sorted(wordcount.items(),key=operator.itemgetter(1),reverse=True)
    #pprint(wordcount)

    with open("logs.txt","a") as f:
        f.write("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
        f.write("Most common wordpairs in text: \n\n")
        #r= 250 if len(sorted_wc) > 250 else len(sorted_wc)
        #for i in range(0, r):
        i = 0
        for key,val in sorted(wordcount.items(), key=lambda i:sum(i[1].values()),reverse=True):
            #print(key,val)
            f.write("%s,%s,\n\t\t'total': %i,\n\t\t'1-2': %i, \n\t\t'3-5': %i, \n\t\t'6-8': %i,\n\t\t'8-14': %i,\n\t\t'15+': %i'\n\n" %
            (key[0],key[1],sum(val.values()),val['1-2'],val['3-5'],val['6-8'],val['8-14'],val['15+']))
            if (i>300):
                break
            i+=1
        f.close()


def checkTopic(topics,righttopics):
    for topic in topics:
        if topic["title"] in righttopics:
            return True
    return False

def addSentence(w, nickname, date):
    wordlist=[word.lower() for word in w.split() if not any(word in s for s in stopwords)]
    for i in range(len(wordlist)):
        for j in range(i+1,len(wordlist)):
            if len(wordlist[i]) >= 2 and len(wordlist[j]) >= 2 and wordlist[i]!=wordlist[j] and wordlist[i] != " " and wordlist[j] != " " and j-i < 20:
                dateofpost = DateOfPost.objects.createDateOfPost(date)
                wordPair = createWordPair(wordlist[i], wordlist[j], j-i, dateofpost)
                nickname = NicknameOfPoster.objects.createNickname(nickname, wordPair)    


regexp = re.compile(r'[^a-zA-Z0-9åäöÅÄÖ]')

def checkWord(word):
    return regexp.search(word)
"""
#Helper function to remove odd characters from single words
def checkWord(wrd):
    return re.sub(r'[^a-zA-Z0-9åäöÅÄÖ]','',wrd)
"""
def checkSentence(string):
    ret = []
    sents = nltk.sent_tokenize(string)
    flag = False
    for s in sents:
        tmp = ""
        if "http" in s:
            #print("http")
            continue
        tokens = nltk.word_tokenize(s)
        for w in tokens:
            if len(w)<2 or checkWord(w):
                continue
            keyword_type = search_keywords(w)

            #TODO: record keyword_type
            if (keyword_type != 0):
                flag = True
            tmp += w + " "
        ret.append(tmp)
    return ret if flag else ""

def convertToConllu(sent):
    #sent = sent,"utf-8".rstrip()
    tokens = sent.split()
    newSent=""
    for tIdx,t in enumerate(tokens):
         newSent+=(u"%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\n"%(tIdx+1,t)) #.encode("utf-8")
    return newSent



def scan():
    righttopics = ["Paikkakunnat","Terveys"]

    #location of json folder to read data from
    files = listdir("filescanner/uploadFiles/")

    for fileN in files:
        if fileN.endswith(".json"):
            filename="filescanner/uploadFiles/{}".format(fileN)
        else:
            continue
        with open(filename) as f:
            try:
                items = ijson.items(f,"item")
                for o in items:
                    if not checkTopic(o["topics"],righttopics) or o["deleted"]:
                        continue
                    body = o["body"]
                    nick = o["anonnick"]
                    date = o["created_at"]
                    newbody = checkSentence(body)
                    for sentence in newbody:
     
                        addSentence(sentence, nick, date)

                    """    
                    for c in o["comments"]:
                        if c["deleted"]:
                            continue
                        sent = c["body"]
                        sent = checkSentence(sent)
                        for s in sent:
                            data["comments"]+=1
                            #cleanC = [word for word in body.split() if word.lower() not in stopwords]
                            addSentence(s)
                    """
            except ValueError:
                print("ValueError")
                continue
            except ijson.common.IncompleteJSONError:
                print("IncompleteJSONError")
                continue
            writeToFile()

#pprint(data)
