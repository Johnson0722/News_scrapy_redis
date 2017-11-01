爬虫说明文档

功能: 实现了基于scrapy-redis的增量爬取，基于simhash的相似文档的去重，支持分布式。

--Daily_crawler
daily_crawler.cron  crontab的定时文件, 定时运行start_crawl.sh脚本
start_crawl.sh 启动爬虫模块，并将每次爬取所花费的时间 写入 log/run_time.txt
push_urls.py 每次在爬虫之前运行，清空调度队列，并将start_url push到调度队列中
news_crawl.sh 执行爬虫模块（增量爬取）， 并自动进行相似文档去重，ETL, 存入mongodb

--ETL
/Model 存放训练好的词典，语料，TF-IDF，LDA， word2vec模型
auto_embedding.py 新闻语料的清洗，以及自动化生成新闻的标题和内容embedding
auto_embedding_simhash.py 增加了自动化相似文档的去重
stop_words 常用的中文停留词
train_step1 训练LDA模型
train_step2 训练LDA模型

--log
auto_embedding_simhash.log 执行auto_embedding_simhash.py的日志文件
crawler.log 执行scrapy-redis爬虫模块的日志文件
news_count.log 执行news_statistics.py的日志文件
run_time.txt 每次执行爬虫脚本的运行时间

--News_data
每个文件夹是抓每天从各个网站抓取到的新闻

--News_scrapy
基于scrapy-redis的爬虫模块，在scrapy的基础上修改得到

--News_simhash
实现相似文档的去重
automatic_simhash.py 自动实现相似文档的去重（仅基于新闻内容）
content_index.pkl 序列化的新闻内容SimhashIndex类，相当于所有新闻sinhash_value的一张表，
                  并且随着抓取的新闻越来越多，该表会不断增大
title_index.pkl 序列化的新闻标题SimhashIndex类， 未使用
generate_simhash_index.py 初始化这张Simhash_index，生成content和title的Simhash_index
near_duplicates.py 对初始化的Simhash_index进行相似新闻内容的去重
test.py 测试content_index.pkl中content_index类新闻的数量

--News_statistics
news_count.json 每天从各个网站抓取的新闻数量
news_statistics.py  统计新闻增量的脚本

utilities.py 常用的一些函数
scrapy.cfg scrapy爬虫框架配置文件
