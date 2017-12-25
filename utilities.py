import logging
from gensim import corpora, models
import jieba
import re
import datetime
import pandas as pd
import numpy as np
import numpy.linalg as LA



def get_news_feature(news, models):
    """
    get title features and content features of the article
    each feature is a list of tuple, [(word1, weight1),(word2, weight2),...]
    :param article: type of dict
    :param models: type of six-tuple, Ex:
    (dictionary_titles, dictionary_contents, tfidf_title_model, tfidf_content_model, title_word_list, content_word_list)
    :return: title features and content features, type of list
    """
    # loading models
    dictionary_titles, dictionary_contents, tfidf_title_model, \
    tfidf_content_model, title_word_list, content_word_list = models
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

def filter_tags(htmlstr):
    """fileter HTML tag and http link"""
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
    re_br=re.compile('<br\s*?/?>')
    re_h=re.compile('</?\w+[^>]*>')
    re_comment=re.compile('<!--[^>]*-->')
    s=re_cdata.sub('',htmlstr)
    s=re_script.sub('',s)
    s=re_style.sub('',s)
    s=re_br.sub('\n',s)
    s=re_h.sub('',s)
    s=re_comment.sub('',s)
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)
    return s


def standard_timestamp(time_string):
    '''
    process time into standard style, EX: 2017-10-17 09:12:45
    :param time_string: type of string
    :return: standard timestamp
    '''
    start_time = datetime.datetime(1970,1,1,0,0,0)

    try:
        time_stamp = pd.Timestamp(time_string)
        return (time_stamp - start_time).total_seconds()

    except ValueError as e:
        # case1: 更新于2016年11月10日 07:08 or 2016年05月20日
        if u'年' in time_string or u'月' in time_string:
            pattern = re.compile(r'\d+|:')
            time_list = pattern.findall(time_string)
            if len(time_list) == 3:
                time_stamp = '-'.join(time_list)
                time_stamp = pd.Timestamp(time_stamp)
                return (time_stamp - start_time).total_seconds()
            elif len(time_list) == 6 or len(time_list) == 8:
                time_stamp = '-'.join(time_list[:3]) + ' ' + ''.join(time_list[3:])
                time_stamp = pd.Timestamp(time_stamp)
                return (time_stamp - start_time).total_seconds()

        # case2: 16小时前
        if u'小时前' in time_string:
            pattern = re.compile(r'\d+')
            pre_hours = int(pattern.findall(time_string)[0])
            # current time sub pre_hours
            time_ = datetime.datetime.now() - datetime.timedelta(hours=pre_hours)
            time_stamp = time_.strftime('%Y-%m-%d %H:%M:%S')
            return (pd.Timestamp(time_stamp) - start_time).total_seconds()

        # case2: 16分钟前
        if u'分钟前' in time_string:
            pattern = re.compile(r'\d+')
            pre_mins = int(pattern.findall(time_string)[0])
            # current time sub pre_hours
            time_ = datetime.datetime.now() - datetime.timedelta(minutes=pre_mins)
            time_stamp = time_.strftime('%Y-%m-%d %H:%M:%S')
            return (pd.Timestamp(time_stamp) - start_time).total_seconds()

        # case3: 2天前
        if u'天前' in time_string:
            pattern = re.compile(r'\d+')
            pre_days = int(pattern.findall(time_string)[0])
            # current time sub pre_hours
            time_ = datetime.datetime.now() - datetime.timedelta(days=pre_days)
            time_stamp = time_.strftime('%Y-%m-%d %H:%M:%S')
            return (pd.Timestamp(time_stamp) - start_time).total_seconds()

def setence2vec(vec_bow, w2v_model, tfidf_model, word_list):
    '''
    convert any length of string to a vector of fixed dimensions
    :param vec_bow: vector of bag of words
    :param tfidf_model: trained tfidf model
    :param dictionary:  pre-loading dictionary
    :param word_list:  word_list of dictionary
    :return: a fixed dimension vector, type of ndarray
    '''
    vec_tfidf = tfidf_model[vec_bow]
    setence_vec =  np.zeros(256)
    for word_index, weight in vec_tfidf:
        try:
            setence_vec += w2v_model[word_list[word_index]] * weight
        except:
            continue
    if LA.norm(setence_vec) > 0:
        setence_vec = setence_vec/LA.norm(setence_vec)
    return setence_vec

def loading_models():
    # loading cofigurations
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # loading dictionaries   ETL/dict_titles
    dictionary_titles = corpora.Dictionary.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/Model/dict_titles')
    dictionary_contents = corpora.Dictionary.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/Model/dict_contents')
    # loading tfidf models
    tfidf_title_model = models.TfidfModel.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/Model/tfidf_title.model')
    tfidf_content_model = models.TfidfModel.load('/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL/Model/tfidf_content.model')
    # type of dict
    titles_token2id = dictionary_titles.token2id
    content_token2id = dictionary_contents.token2id
    # word list
    title_word_list = list(titles_token2id)
    content_word_list = list(content_token2id)
    return (dictionary_titles, dictionary_contents, tfidf_title_model, tfidf_content_model, title_word_list, content_word_list)

def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                   'lt':'<','60':'<',
                   'gt':'>','62':'>',
                   'amp':'&','38':'&',
                   'quot':'"','34':'"',}

    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()
        key=sz.group('name')
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:

            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr

def repalce(s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)


