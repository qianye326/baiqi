import scrapy
from amaz.items import AmazItem

# 修改成分布式爬虫
# ------1:导入库
from scrapy_redis.spiders import RedisSpider
# 继承类
# 设置锁
# 注销起始域名
# def __init__创建域名

class AmSpider(RedisSpider):
    name = 'AM'
    # 3:-----注销allowed_domains和start_urls
    # allowed_domains = ['amazon.com','www.amazon.cnnone','www.amazon.cn','www.amazon.cnNone','www.amazon.cnNone']
    # start_urls = ['https://www.amazon.cn/s?i=computers&rh=n%3A106200071&fs=true&page=2&qid=1622023319&ref=sr_pg_2']
    # 4：设置redis-key
    redis_key = 'py21'

    # 是设置___init__

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(AmSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        temp = response.xpath('//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div')
        for d in temp:
            item = AmazItem()
            item['link'] = d.xpath('./div/span/div/div/span/a/@href').extract_first()
            item['price'] = str(d.xpath('*//span[@class="a-price"]/span/text()').extract_first()).strip().replace(' ','').replace('\r','').replace('\t','').replace('\n','')
            item['name'] = str(d.xpath('./div/span/div/div/div[2]/h2/a/span/text()').extract_first()).strip().replace(' ','').replace('\r','').replace('\t','').replace('\n','')
            yield scrapy.Request(
                url='https://www.amazon.cn'+str(item['link']),
                callback=self.info,
                meta={'item': item}
            )

        next_url = response.xpath('//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[25]/span/div/div/ul/li[@class="a-last"]/a/@href').extract_first()
        if next_url!=None :
            yield scrapy.Request(
                url = 'https://www.amazon.cn'+next_url,
                callback=self.parse
            )

    def info(self, response):
        item = response.meta['item']
        item['stork'] = response.xpath('//*[@id="availability"]/span/text()').extract_first()
        print(item)
        yield item

