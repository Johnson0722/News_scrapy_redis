#! /bin/sh
PATH=/home/johnso/anaconda3/bin:/home/johnso/bin:/home/johnso/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
cd /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/Daily_crawler
python push_urls.py
cd /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/News_data
time=`date "+%Y-%m-%d-%H:%M:%S"`
dirname="news_${time}"
mkdir $dirname
cd $dirname

scrapy crawl aliresearch > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl ftchinese > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl caixin > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl cyzone > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl dgtle > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl donews > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl economist > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl guokr > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl huxiu > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl ifeng > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl jiqizhixin > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl lijiresearch > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl neteasetech > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl rsarxiv > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl syncedreview > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl tech2ipo > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl technode > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl techqq > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl techreview > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl techsina > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl techsohu > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl tmtpost > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl vcbeat > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl xtecher > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl zaker > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl zhidx > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl 36dsj > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1
scrapy crawl aitists > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/crawler.log 2>&1


pre_dir=/home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/News_data/
news_dir=${pre_dir}${dirname}
cd /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/ETL
/home/johnso/anaconda3/bin/python auto_embedding_simhash.py --dir $news_dir > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/auto_embedding_simhash.log 2>&1

cd /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/News_statistics
/home/johnso/anaconda3/bin/python news_statistics.py --dir $news_dir > /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log/news_count.log 2>&1

