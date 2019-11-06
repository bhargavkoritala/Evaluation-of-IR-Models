# -*- coding: utf-8 -*-


import json
# if you are using python 3, you should 
import urllib.request 
#import urllib2
from nltk.corpus import stopwords
from langdetect import detect


def post(encoded_args,lang,qid,iteration):
    #inurl = 'http://52.14.130.28:8983/solr/BM25/select?q=text_de%3A'+encoded_args+'%0Atext_en%3A'+encoded_args+'%0Atext_ru%3A'+encoded_args+'&fl=id%2Cscore&wt=json&indent=true&rows=20'
    en_inurl = 'http://52.14.130.28:8983/solr/LM/select?q='+encoded_args+'&defType=edismax&qf=text_en^2+text_de+text_ru&fl=id%2Cscore&wt=json&indent=true&rows=20'
    de_inurl = 'http://52.14.130.28:8983/solr/LM/select?q='+encoded_args+'&defType=edismax&qf=text_en+text_de^2+text_ru&fl=id%2Cscore&wt=json&indent=true&rows=20'
    ru_inurl = 'http://52.14.130.28:8983/solr/LM/select?q='+encoded_args+'&defType=edismax&qf=text_en+text_de+text_ru^2&fl=id%2Cscore&wt=json&indent=true&rows=20'
    inurl = 'http://52.14.130.28:8983/solr/LM/select?q='+encoded_args+'&defType=edismax&qf=text_en+text_de+text_ru&fl=id%2Cscore&wt=json&indent=true&rows=20'
    outfn = str(iteration)+'.txt'


    # change query id and IRModel name accordingly
    IRModel='LM'
    outf = open(outfn, 'a+',encoding="utf8")
    print(inurl)
    if lang=='en':
        data = urllib.request.urlopen(en_inurl)
    elif lang=='de':
        data = urllib.request.urlopen(de_inurl)
    elif lang=='ru':
        data = urllib.request.urlopen(ru_inurl)
    else:
        data = urllib.request.urlopen(inurl)
    # if you're using python 3, you should use
    # data = urllib.request.urlopen(inurl)

    docs = json.load(data)['response']['docs']
    print(docs)
    # the ranking should start from 1 and increase
    rank = 0
    for doc in docs:
        outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    outf.close()


def main():
    iteration=0

    f = open(r'E:\Acad\IR\Projects\Project 3 - IR Models Evaluation\project3_data\test_queries.txt','r',encoding="utf8")
    for line in f.readlines():
        #process queries one by one--------------------------------
        iteration=iteration+1
        query=''
        words=line.split()
        qid= words[0]
        for word in words[1:]:
            query= query+word+' '
        query=query[:-1]
        lang = detect(query)
        #query='text_en + text_de + text_ru:'+query
        query_args= {'q':query}
        encoded_args = urllib.parse.quote_plus(query)
        #encoded_args = urllib.parse.urlencode(query)
        post(encoded_args,lang,qid,iteration)
# change the url according to your own corename and query
#inurl = 'http://52.14.130.28:8983/solr/LM/select?'+encoded_args+'&fl=id%2Cscore&wt=json&indent=true&rows=20'

if __name__ == "__main__":
    main()




