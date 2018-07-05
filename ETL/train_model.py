# coding:utf-8
import jieba
import json
import logging
import pandas as pd
from gensim import corpora, models
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from collections import defaultdict

def loading_training_data():
    titles = []
    train_data = pd.read_csv('data/train_data.csv')
    num_titles = len(train_data)
    for i in xrange(num_titles):
        true_words = []
        title = train_data.iloc[i,1]
        title_words = jieba.cut(title)
        for word in title_words:
            if word not in stop_words:
                true_words.append(word)
        titles.append(true_words)
    return titles

def loading_stop_words():
    stop_words = set()
    with open('data/stop_words.txt') as f:
        for line in f:
            word = line.strip('\n')
            stop_words.add(word)
    return stop_words

def remove_low_frequency_words(titles):
    frequency_title = defaultdict(int)
    for title in titles:
        for token in title:
            frequency_title[token] += 1
    processed_titles = [[token for token in title if frequency_title[token] > 5] for title in titles]
    return processed_titles

def build_save_dict(titles):
    # build dictionaries
    dict_titles = corpora.Dictionary(titles)
    # save dictionaries
    dict_titles.save('models/dict_titles')
    return dict_titles

def memory_friendly_dict(data_path):
    # build dicts
    print('build dicts...')
    dict_texts = corpora.Dictionary(line.split(' ')[1:] for line in open(data_path,'r'))
    print('saving dicts')
    # save dictionaries
    dict_texts.save('data/dict_texts')
    return dict_texts

def build_save_corpus(titles):
    # build corpus
    corpus_titles = [dicts.doc2bow(title) for title in titles]
    # save corpus
    corpora.MmCorpus.serialize('models/corpus_titles', corpus_titles)
    return corpus_titles

def build_save_tfidf_model(corpus):
    # build tfidf model
    tfidf_model = models.TfidfModel(corpus)
    # save tfidf model
    tfidf_model.save('models/tfidf_title.model')

if __name__ == '__main__':
    stop_words = loading_stop_words()
    titles = loading_training_data()
    titles = remove_low_frequency_words(titles)
    dicts = build_save_dict(titles)
    corpus = build_save_corpus(titles)
    build_save_tfidf_model(corpus)
