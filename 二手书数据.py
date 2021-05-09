import requests
import csv,re,json
from lxml import etree
import random
import time
number_sum = 0
for rez in range(1,40):
    try:
        url = 'http://item.kongfz.com/Cjiaocai/tag_k33k32k30k32k34w{}/'.format(rez)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
            ,'referer': 'http://item.kongfz.com/'
        }
        html = requests.get(url,headers=headers)
        data = etree.HTML(html.content)
        each_item = data.xpath('//*[@id="listBox"]/div')
        # com_re = re.compile('<a href="(.*?)" target="_blank" class="text">')
        # href = list(set(com_re.findall(html.text)))
        # print(href)
        list = []
        for e in each_item:
            title = e.xpath('./div[2]/div/a/text()')[0]
            new_price = e.xpath('./div[3]/div[1]/div[1]/a/span[2]/text()')[0]
            old_price = e.xpath('./div[3]/div[2]/div[1]/a/span[2]/text()')[0]
            link = e.xpath('./div[2]/div[1]/a/@href')[0]
            # print(link)
            #获取第一个详情页面的累计评价，假设成销量
            url  = requests.get(link,headers=headers)
            inner = etree.HTML(url.content)
            inner_link = inner.xpath('//*[@id="detail-list-con"]/div/ul/li[1]/div[2]/a/@href')[0]
            print(inner_link)
            #获取post参数
            inner_url = requests.get(inner_link,headers=headers)
            com_re = re.compile('"itemId":(.*?),')
            com_rre = re.compile('"userId":(.*?),"')
            userId = com_rre.findall(inner_url.text)[0]
            itemid = com_re.findall(inner_url.text)[0]
            # print(itemid)
            # print(inner_url.text)
            #构建POST请求
            params = {
                'userId': '{}'.format(userId),
                'itemId': '{}'.format(itemid),
                'onlyItem': '0',
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
                ,'Referer': '{}'.format(inner_url)
            }
            #在进一个链接获取评价数据
            url = 'http://book.kongfz.com/Pc/Ajax/getReviewListInfo'
            num_url = requests.post(url,headers=headers,params=params)
            # print(num_url)
            data = json.loads(num_url.text)['result']['reviewTagNum'][0]['num']
            # print(data)
            k = [title,new_price,old_price,data]
            list.append(k)
            number_sum +=1
            print('爬取了：{}本书'.format(number_sum))
    except:
        pass
    #保存数据：
    with open('二手书.csv','a',errors='ignore') as f:
        item = csv.writer(f,delimiter=',')
        for i in list:
            item.writerow(i)

    tim = random.randint(1,6)
    time.sleep(tim)