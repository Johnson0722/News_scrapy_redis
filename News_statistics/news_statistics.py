# coding:utf-8
import json
import os
import pandas as pd
import datetime
import argparse

def news_count(dir):
    '''
    count news for every websites
    :param dir: a directory contains all crawled news
    :return: type of dictionary, key is web name, value is news counts,
            {'huxiu':231, 'ifeng':213,}
    '''
    results_counts = {}
    for file in os.listdir(dir):
        with open(os.path.join(dir, file), encoding='utf-8') as f:
            counts = 0
            for line in f:                                  # type(line) = str
                line = json.loads(line, encoding='utf-8')    # type(line) = dict
                counts += 1
            name = file.split('.')[0]
            results_counts[name] = counts

    return results_counts


if __name__ == '__main__':
    '''write statistics results into news_cout.json'''
    # get news directory
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='directory news', type=str)
    args = parser.parse_args()
    data_dir = args.dir
    # directory
    statistics_dir = '/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/News_statistics'
    json_file = os.path.join(statistics_dir, 'news_count.json')
    # write to json file
    now_time = str(pd.Timestamp(datetime.datetime.now()))
    now_time = json.dumps(now_time, ensure_ascii=False) + '\n'
    results_counts = news_count(data_dir)
    results_counts = json.dumps(results_counts, ensure_ascii=False) + '\n'
    file = open(json_file, 'a')
    file.write(now_time)
    file.write(results_counts)




