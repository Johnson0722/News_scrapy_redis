import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)


dict = {
        "36dsj:start_urls":["http://www.36dsj.com/"],
        "36kr:start_urls":["https://36kr.com/"],
        "aliresearch:start_urls":['http://www.aliresearch.com/'],
        "artists:start_urls":['http://www.aitists.com/'],
        "caixin:start_urls":['http://china.caixin.com/'],
        "cyzone:start_urls":['http://www.cyzone.cn/'],
        "dgtle:start_urls":['http://www.dgtle.com/'],
        "donews:start_urls":['http://www.donews.com/',
                             'http://www.donews.com/idonews/'],
        "economist:start_urls":['https://www.economist.com/'],
        "ftchinese:start_urls":['http://www.ftchinese.com/'],
        "guokr:start_urls":['http://www.guokr.com/scientific/'],
        "huxiu:start_urls":['https://www.huxiu.com'],
        "ifeng:start_urls":['http://tech.ifeng.com/'],
        "finance_ifeng:start_urls":['http://finance.ifeng.com/',
                                    'http://tech.ifeng.com/',
                                     'http://finance.ifeng.com/stock/gstzgc/'],
        "infoq:start_urls":['http://www.infoq.com/cn/'],
        "jiqizhixin:start_urls":['http://www.jiqizhixin.com/'],
        "lijiresearch:start_urls":['http://www.lijiresearch.com/',
                                   'http://www.lijiresearch.com/zixun/'],
        "neteasetech:start_urls":['http://tech.163.com/smart'],
        "rsarxiv:start_urls":['http://rsarxiv.github.io/'],
        "syncedreview:start_urls":['https://syncedreview.com/'],
        "tech2ipo:start_urls":['http://tech2ipo.com/',
                               'http://tech2ipo.com/special/11',
                               'http://tech2ipo.com/special/12',
                               'http://tech2ipo.com/special/13',
                               'http://tech2ipo.com/special/14',
                               'http://tech2ipo.com/special/1',
                               'http://tech2ipo.com/special/6',
                               'http://tech2ipo.com/special/7',
                               'http://tech2ipo.com/special/8',
                               'http://tech2ipo.com/special/9',],
        "technode:start_urls": ['http://cn.technode.com/'],
        


        }

webs = dict.keys()
start_urls = dict.values()