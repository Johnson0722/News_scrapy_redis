from simhash import Simhash, SimhashIndex
import json
from data_preprocess import filter_tags
import logging
from gensim import corpora, models
import jieba
import os
import pickle

def get_news_feature(news):
    """
    get title features and content features of the article
    each feature is a list of tuple, [(word1, weight1),(word2, weight2),...]
    :param article: type of dict
    :return: title features and content features, type of list
    """
    # get title and content
    title = news['title']
    content = filter_tags(news['content_code']).strip()
    # convert title to vec of bow
    title_bow = dictionary_titles.doc2bow(list(jieba.cut(title)))
    # convert content to vec of bow
    content_bow = dictionary_contents.doc2bow(list(jieba.cut(content)))
    # get article feature, type of list
    vec_title_tfidf = tfidf_title_model[title_bow]
    vec_content_tfidf = tfidf_content_model[content_bow]
    # sorting
    vec_title_tfidf.sort(key=lambda x:x[1], reverse = True)
    vec_content_tfidf.sort(key=lambda x:x[1], reverse = True)
    # get top 20 tfidf-weights words
    vec_title_tfidf = vec_title_tfidf[:20]
    vec_content_tfidf = vec_content_tfidf[:20]
    # get title and content features
    title_fectures = [(title_word_list[word_index], tfidf_weights)
                      for word_index, tfidf_weights in vec_title_tfidf]
    content_fectures = [(content_word_list[word_index], tfidf_weights)
                        for word_index, tfidf_weights in vec_content_tfidf]

    return title_fectures, content_fectures


if __name__ == '__main__':
    # loading cofigurations
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # loading dictionaries   ETL/dict_titles
    dictionary_titles = corpora.Dictionary.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/dict_titles')
    dictionary_contents = corpora.Dictionary.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/dict_contents')
    # loading tfidf models
    tfidf_title_model = models.TfidfModel.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/tfidf_title.model')
    tfidf_content_model = models.TfidfModel.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/tfidf_content.model')
    # type of dict
    titles_token2id = dictionary_titles.token2id
    content_token2id = dictionary_contents.token2id
    # word list
    title_word_list = list(titles_token2id)
    content_word_list = list(content_token2id)

    title_data = []
    content_data = []
    count = 1
    news_dir = '/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/news_2017-10-25-13:15:47'
    for file in os.listdir(news_dir):
        news_file = os.path.join(news_dir, file)
        with open(news_file) as f:
            for line in f:
                news = json.loads(line)
                title_features, content_features = get_news_feature(news)
                title_data.append((str(count), Simhash(title_features)))
                content_data.append((str(count), Simhash(content_features)))
                count += 1

                if count % 1000 == 0:
                    logging.info('{} has finished'.format(count))

    title_index = SimhashIndex(title_data)
    content_index = SimhashIndex(content_data)
    # saving
    with open('title_index.pkl', 'wb') as f1:
        pickle.dump(title_index, f1)
    with open('content_index.pkl','wb') as f2:
        pickle.dump(content_index, f2)

    # loading
    # with open('title_index.pkl','rb') as f1:
    #     title_index = pickle.load(f1)
    # with open('content_index.pkl','rb') as f2:
    #     content_index = pickle.load(f2)
    #
    # print(title_index.bucket_size)
    # print(content_index.bucket_size)

