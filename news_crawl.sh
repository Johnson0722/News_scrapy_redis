#! /bin/sh

cd /home/johnso/PycharmProjects/News_recommendation/News_scrapy
time=`date "+%Y-%m-%d-%H:%M:%S"`
dirname="news_${time}"
mkdir $dirname
cd $dirname

scrapy3 runspider a.py.


time -o run_time.txt  nohup scrapy crawl aliresearch 1> /dev/null 2> /dev/null
time -a -o run_time.txt  nohup scrapy crawl ftchinese 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl caixin 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl cyzone 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl dgtle 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl donews 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl economist 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl guokr 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl huxiu 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl ifeng 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl jiqizhixin 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl lijiresearch 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl neteasetech 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl rsarxiv 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl syncedreview 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl tech2ipo 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl technode 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl techqq 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl techreview 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl techsina 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl techsohu 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl tmtpost 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl vcbeat 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl xtecher 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl zaker 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl zhidx 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl 36dsj 1> /dev/null 2> /dev/null
time -a -o run_time.txt nohup scrapy crawl aitists 1> /dev/null 2> /dev/null
