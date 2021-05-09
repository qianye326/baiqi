import requests
import json
import os
count = 0
print('此文件将保存在当前文件中的baidutupian里面')
title = input('你想要搜索的名称是：')
page = input('你想要多少页的图片：')
if not os.path.exists('biadutupian'):
    os.makedirs('biadutupian')
for i in range(30,int(page),30):
    params = {
         'tn': 'resultjson_com',
        'logid': '6041931799708604536',
        'ipn': 'rj',
        'fp': 'result',
        'queryWord': '火影忍者',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'word': title,  #搜索名称
        '1612164485343':'1',
        'pn': i,         #翻页
        'rn': '60',      #每页展示多少张图片
        'gsm': '3f'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Referer': 'https://image.baidu.com/search/index?ct=201326592&z=9&tn=baiduimage&word=%E7%81%AB%E5%BD%B1%E5%BF%8D%E8%80%85&pn=0&ie=utf-8&oe=utf-8&cl=2&lm=-1&fr=&se=&sme=&width=0&height=0'
    }

    url = 'https://image.baidu.com/search/acjson'
    html = requests.get(url,params=params,headers=headers).text
    try:
        data = json.loads(html)['data']
        for d in data:
            try:
                pic_url = d['thumbURL']
                print(pic_url)
                with open('biadutupian/{}.jpg'.format(count),'wb') as f :
                    f.write(requests.get(pic_url).content)
                count+=1
                print(count)
            except:
                pass
    except:
        print(html)

