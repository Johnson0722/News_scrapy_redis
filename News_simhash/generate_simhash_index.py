from simhash import Simhash, SimhashIndex
import json
import logging
import os
import pickle
from utilities import get_news_feature


if __name__ == '__main__':

    title_data = []
    content_data = []
    news_id = 1
    news_dir = '/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/news_2017-10-25-13:15:47'
    for file in os.listdir(news_dir):
        news_file = os.path.join(news_dir, file)
        with open(news_file) as f:
            for line in f:
                news = json.loads(line)
                title_features, content_features = get_news_feature(news)
                print(title_features)
                print(content_features)
                title_data.append((str(news_id), Simhash(title_features)))
                content_data.append((str(news_id), Simhash(content_features)))

                news_id += 1
                if news_id % 1000 == 0:
                    logging.info('{} has finished'.format(news_id))

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

