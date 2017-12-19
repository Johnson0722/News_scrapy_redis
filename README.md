
## 爬虫说明文档

### 1.功能: 实现了基于scrapy-redis的增量爬取，基于simhash的相似文档的去重，支持分布式。

### 2. 各模块说明
#### Daily_crawler
* daily_crawler.cron  crontab的定时文件, 定时运行start_crawl.sh脚本
* start_crawl.sh 启动爬虫模块，并将每次爬取所花费的时间 写入 log/run_time.txt
* push_urls.py 每次在爬虫之前运行，清空调度队列，并将start_url push到调度队列中
* news_crawl.sh 执行爬虫模块（增量爬取）， 并自动进行相似文档去重，ETL, 存入mongodb

#### ETL
* /Model 存放训练好的词典，语料，TF-IDF，LDA， word2vec模型
* auto_embedding.py 新闻语料的清洗，以及自动化生成新闻的标题和内容embedding
* auto_embedding_simhash.py 增加了自动化相似文档的去重
* stop_words 常用的中文停留词
* train_step1 训练LDA模型
* train_step2 训练LDA模型

#### log
* auto_embedding_simhash.log 执行auto_embedding_simhash.py的日志文件
* crawler.log 执行scrapy-redis爬虫模块的日志文件
* news_count.log 执行news_statistics.py的日志文件
* run_time.txt 每次执行爬虫脚本的运行时间

#### News_data
* 每个文件夹是抓每天从各个网站抓取到的新闻

#### News_scrapy
* 基于scrapy-redis的爬虫模块，在scrapy的基础上修改得到

#### News_simhash
* 实现相似文档的去重
* automatic_simhash.py 自动实现相似文档的去重（仅基于新闻内容）
* content_index.pkl 序列化的新闻内容SimhashIndex类，相当于所有新闻sinhash_value的一张表，并且随着抓取的新闻越来越多，该表会不断增大
* title_index.pkl 序列化的新闻标题SimhashIndex类， 未使用
* generate_simhash_index.py 初始化这张Simhash_index，生成content和title的Simhash_index
* near_duplicates.py 对初始化的Simhash_index进行相似新闻内容的去重
* test.py 测试content_index.pkl中content_index类新闻的数量

#### News_statistics
* news_count.json 每天从各个网站抓取的新闻数量
* news_statistics.py  统计新闻增量的脚本


**utilities.py 常用的一些函数**

**scrapy.cfg scrapy爬虫框架配置文件**

**_模块中的所有文件使用的都是绝对路径，本地配置时需要修改_**

### ３.开发过程中遇到的一些坑以及处理办法
* 使用scrapy爬虫框架时，编写spiders可以使用xpath进行网页内容的提取，google浏览器有xpath helper插件，大幅度提高编程效率
* 将scrapy爬虫改写成spider-redis时，要注意一下问题：
  * scrapy-redis维护两个队列，一个判重池和调度队列，判重池用于存储爬取过的url, 调度队列存储待爬取的url，这两个队列都存在redis中（每个待爬取网站都有这两个队列）
  
  * scrapy-redis有空跑问题，即调度队列为空时爬虫程序仍然执行，需要修改scrapy-redis中的源码，主要就是修改site-packages/scrapy_redis中spiders,在def next_requests(self)中加几行代码，具体google
　
  * 使用scrapy-redis定时增量抓取时，每次抓取之前需要先清空调度池，然后向调度池push各个网站的start_urls


* 导入自定义模块时报错　可以在代码最开始加上

    ```python
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)
    ```
* 定时任务执行报错（模块导入问题），但是手动执行任务可以跑通
  * crontab 环境变量的问题，解决方法：
   
   １．gedit /etc/crontab　修改环境变量path, 具体地，查看当前项目下的环境变量os.environ，用os.environ的环境变量path覆盖 
        
   ２．将path（os.environ）添加到每天执行的shell脚本中  
