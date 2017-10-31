# coding:utf-8
from gensim import corpora
import jieba
import json
import logging
from collections import defaultdict
import os
from utilities import filter_tags

# logging configuation
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# all titles and contents
titles = []
contents = []
stop_list = []
# loading stop words
with open('stop_words') as f:
    for line in f:
        stop_list.append(f)

stop_list = set(stop_list)


news_dir = '/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/News_data/news_2017-10-25-13:15:47'
for file in os.listdir(news_dir):
    news_file = os.path.join(news_dir, file)
    with open(news_file) as f:
        for line in f:
            news = json.loads(line)
            title = []
            content = []
            # cut words
            title_words = jieba.cut(news['title'])
            content_words = jieba.cut(filter_tags(news['content_code']))
            # remove stop words
            for word in title_words:
                if word not in stop_list:
                    title.append(word)

            for word in content_words:
                if word not in stop_list:
                    content.append(word)

            titles.append(title)
            contents.append(content)


# build dictionary for title and content
frequency_title = defaultdict(int)
frequency_content = defaultdict(int)

for title in titles:
    for token in title:
        frequency_title[token] += 1

for content in contents:
    for token in content:
        frequency_content[token] += 1


# remove tokens only appear once
titles = [[token for token in title if frequency_title[token] > 1] for title in titles]
# remove tokens only appear once
contents = [[token for token in content if frequency_content[token] > 1] for content in contents]

# build dictionaries
dictionary_titles = corpora.Dictionary(titles)
dictionary_contents = corpora.Dictionary(contents)

# save dictionaries
dictionary_titles.save('Model/dict_titles')
dictionary_contents.save('Model/dict_contents')

# build corpus
corpus_titles = [dictionary_titles.doc2bow(title) for title in titles]
corpus_contents = [dictionary_contents.doc2bow(content) for content in contents]

# save corpus
corpora.MmCorpus.serialize('Model/corpus_titles', corpus_titles)
corpora.MmCorpus.serialize('Model/corpus_contents', corpus_contents)


