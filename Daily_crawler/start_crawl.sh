#! /bin/sh

cd /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/log
now_time=`date "+%Y-%m-%d-%H:%M:%S"`
echo $now_time>>run_time.txt
time -a -o run_time.txt /home/johnso/PycharmProjects/News_recommendation/News_scrapy_redis/Daily_crawler/news_crawl.sh
