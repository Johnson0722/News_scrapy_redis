import pickle
from simhash import Simhash
import os
import json
from utilities import get_news_feature
import logging

if __name__ == '__main__':

    # loading simhash index
    with open('content_index.pkl','rb') as f2:
        content_index = pickle.load(f2)

    news_id = 1
    hash_values = {}
    news_dir = '/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/news_2017-10-25-13:15:47'
    for file in os.listdir(news_dir):
        news_file = os.path.join(news_dir, file)
        with open(news_file) as f:
            for line in f:
                news = json.loads(line)
                title_features, content_features = get_news_feature(news)
                hash_value = Simhash(content_features)
                # build dictionaries, key is obj_id, value is hash_value
                hash_values[str(news_id)] = hash_value

                news_id += 1
                if news_id % 1000 == 0:
                    logging.info("{} has finished".format(news_id))


    count = 1
    # remove near-duplicates news content
    for news_id, hash_value in hash_values.items():
        ans = content_index.get_near_dups(hash_value)

        for obj_id in ans:
            if obj_id != news_id:
                content_index.delete(obj_id, hash_values[obj_id])

        count += 1
        if count % 1000 == 0:
            logging.info("{} has finished".format(count))


    # saving
    with open('content_index.pkl','wb') as f2:
        pickle.dump(content_index, f2)
        pickle.dump(count,f2)
