import pickle
from simhash import Simhash
import os
import json
from utilities import get_news_feature
from utilities import loading_models
import argparse




if __name__ == '__main__':

    # loading simhash index
    with open('content_index.pkl','rb') as f:
        content_index = pickle.load(f)
        news_id = pickle.load(f)

    # get news directory
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='directory news', type=str)
    args = parser.parse_args()
    news_dir = args.dir
    # loading tfidf models and dictionaries
    models = loading_models()
    # open crawled json file, add hash value to simhash index
    for file in os.listdir(news_dir):
        news_file = os.path.join(news_dir, file)
        with open(news_file) as f:
            for line in f:
                news = json.loads(line)
                title_features, content_features = get_news_feature(news, models)
                hash_value = Simhash(content_features)
                if len(content_index.get_near_dups(hash_value)) < 1:
                    news_id = int(news_id) + 1
                    content_index.add(str(news_id), hash_value)

    # update simhash index
    with open('content_index.pkl','wb') as f2:
        pickle.dump(content_index, f2)
        pickle.dump(news_id,f2)
