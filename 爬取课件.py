import requests
import os
from lxml import etree
import time,re
import random
# 解析初始网页获取响应
flag = 0
agent_pool = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
               ]
url = 'http://www.1ppt.com/kejian/'
headers = {
    'Referer': 'http://www.1ppt.com/kejian/',
    'User-Agent':'{}'.format(agent_pool[random.randint(0,4)])
}
door_response = requests.get(url,headers)
door_response.encoding=door_response.apparent_encoding
# print(door_response.text)


# 获取各个学科的href链接
door_xp = etree.HTML(door_response.content)
data = door_xp.xpath('//*[@id="navMenu"]/ul/li/a/@href')
# print(data)
#循环进入各科主页面
for d in data:
    subject_url = 'http://www.1ppt.com/'+d
    subject_response = requests.get(subject_url,headers=headers)
    subject_response.encoding = subject_response.apparent_encoding
    # print(subject_response.text)
    # 爬取科目下所有版本的链接地址
    level_xp = etree.HTML(subject_response.content)
    level_title = level_xp.xpath('/html/body/div[3]/dl/dd/div/ul/li/a/text()')
    level_date = level_xp.xpath('/html/body/div[3]/dl/dd/div/ul/li/a/@href')
    banben = level_xp.xpath('//*[@class="bookslist"]/h3/text()')
    e = 0
    b = 0
    edition  =level_xp.xpath('//*/h3/text()')
    print(level_title,level_date,banben)
    print('title:{}'.format(len(level_title)),'herf{}.'.format(len(level_date)))
    # 一次访问其中的链接地址
    z = 0
    for d in level_date:
        cell_url = 'http://www.1ppt.com/'+d
        # print(cell_url)
        headers = {
            'User-Agent': '{}'.format(agent_pool[random.randint(0, 4)]),
            'Host': 'www.1ppt.com',
        }
        response = requests.get(cell_url,headers=headers)
        response.encoding = response.apparent_encoding
        # print(response.text)
#         # 进一步访问每个单元的详情页面
        cell_xp = etree.HTML(response.content)
        cell_href = cell_xp.xpath('/html/body/div[4]/div/ul/li/a/@href')
#         # print(cell_href)
#       # 选择页面中第一个PPT地址并访问
        for h in cell_href:
            url = 'http://www.1ppt.com/'+h
            headers = {
                'User-Agent': '{}'.format(agent_pool[random.randint(0, 4)]),
            }
            html = requests.get(url,headers=headers)
            trans = etree.HTML(html.content)
            print(url)
            href= trans.xpath('//dd/ul/li[1]/a/@href')
            ppt_name = trans.xpath('//dd/ul/li[1]/a/@title')
            #访问下载地址：
            for r in range(0,len(href)):
                if 'http://www.1ppt.com/' not in href[r]:
                    url ='http://www.1ppt.com/'+href[r]
                    headers = {
                        'User-Agent': '{}'.format(agent_pool[random.randint(0, 4)])
                    }
                    html = requests.get(url,headers=headers)
                    html.encoding = html.apparent_encoding
                    print(url)
                    try:
                        re_com = re.compile("<li><a href='(.*?)' targe")
                        href = re_com.findall(html.text)[0]
                        url = 'http://www.1ppt.com/'+href
                        html = requests.get(url,headers=headers)
                        trans = etree.HTML(html.content)
                        href = trans.xpath('/html/body/dl/dd/ul[2]/li[1]/a/@href')[0]
                        # 改名并保存
                        print('正在判断文件夹是否存在')
                        if not os.path.exists('PPT/{}/{}.'.format(edition[e],level_title[z])):
                            os.makedirs('PPT/{}/{}'.format(edition[e],level_title[z]))
                            print('正在判断当前文件是否存在')
                        if not os.path.exists('PPT/{}/{}/{}.rar'.format(edition[e], level_title[z], ppt_name[0])):
                            print('当前文件不存在，正在创建文件')
                            with open('PPT/{}/{}/{}.rar'.format(edition[e], level_title[z], ppt_name[0]), 'wb') as f:
                                f.write(requests.get(href).content)
                                ti = random.randint(4, 6) + random.random()
                                print('请稍等\n正在下载{}'.format(ppt_name[0]))
                    except:
                        z += 1
                        break
                else:
                    pass