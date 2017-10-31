# coding:utf-8
import numpy as np
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import logging
import json
import jieba
from gensim import corpora, models
from pymongo import MongoClient
import argparse
from utilities import filter_tags
from utilities import standard_timestamp
from utilities import setence2vec



if __name__ == '__main__':
    """put crawled daily news into a directory,
     and remove HTML tags,extract embeddings， 
    and write to MongoDB Server automatically"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='directory news', type=str)
    args = parser.parse_args()
    news_dir = args.dir
    # setting MongoClient, db and collections
    client = MongoClient("10.18.125.17", 27017)
    db = client.news_test
    table = db.newstable6
    # loading configurations
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # loading dictionaries
    dictionary_titles = corpora.Dictionary.load('Model/dict_titles')
    dictionary_contents = corpora.Dictionary.load('Model/dict_contents')
    # loading models
    lda_title = models.LdaModel.load('Model/lda_title.model')
    lda_content = models.LdaModel.load('Model/lda_content.model')
    tfidf_title = models.TfidfModel.load('Model/tfidf_title.model')
    w2v_model = models.Word2Vec.load('Model/wv.model')
    titles_token2id = dictionary_titles.token2id
    word_list = list(titles_token2id)
    # used as counter
    count = 0
    # open crawled news directory
    for dir_ in os.listdir(news_dir):
        print(dir)
        for file in os.listdir(os.path.join(news_dir,dir_)):
            print(file)
            with open(os.path.join(news_dir,dir_,file), encoding='utf-8') as f:
                for line in f:
                    news = json.loads(line, encoding='utf-8')
                    url = news['url']
                    pub_time = news['pub_time']
                    title = news['title']
                    original_content = news['content_code']
                    content = filter_tags(news['content_code'])
                    # convert title to vec of bow
                    title_bow = dictionary_titles.doc2bow(list(jieba.cut(title)))
                    # convert to vec of lda, type of list
                    title_lda = lda_title[title_bow]
                    # convert title to vec using tf-idf weights * word2vec, type of np.array
                    title_s2v = setence2vec(title_bow, w2v_model, tfidf_title, word_list)
                    # convert content to vec of bow
                    content_bow = dictionary_contents.doc2bow(list(jieba.cut(content)))
                    # convert to vec of lda, type of list
                    content_lda = lda_content[content_bow]
                    # convert to standard_timestamp
                    time_stamp = standard_timestamp(pub_time)
                    # documents
                    doc_info = {
                        'news_url':url, 'news_date':pub_time, 'news_title':title,
                        'news_content':content, 'news_original_content':original_content,
                        'news_title_lda':title_lda,'news_title_s2v':title_s2v.tolist(),
                        'news_content_lda':content_lda, 'news_timestamp':time_stamp,
                        'clicked_amount':0
                    }
                    # insert to mongodb
                    table.insert_one(doc_info)
                    count += 1
                    if count % 1000 == 0:
                        print("{} has finished".format(count))
    print('total {} news'.format(count))