import requests
import re
import json

url = 'http://piaofang.maoyan.com/getBoxList?date=1&isSplit=true'
headers = {
    'Cookie':'_lxsdk_cuid=177a9da6ccfc8-0422b73098a692-c791039-1fa400-177a9da6cd0c8; _lxsdk=177a9da6ccfc8-0422b73098a692-c791039-1fa400-177a9da6cd0c8; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=177a9da6cd1-8ae-463-16f%7C%7C7; __mta=251378617.1613462400297.1613462945572.1613462949855.3'
,'Host': 'piaofang.maoyan.com',
'Referer': 'http://piaofang.maoyan.com/box-office?ver=normal',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
html = requests.get(url,headers=headers)
data = json.loads(html.text)['boxOffice']['data']['list']
all_list= []
for d in data:
    lit = []
    for i in d.values():
        try:
            for v in i.values():
                lit.append(v)
        except:
            lit.append(i)
    all_list.append(lit)
print(all_list)