#导入相关的库
import requests
import json,re,os
from bs4 import BeautifulSoup
#获取下载的url，params，hash值
url = 'https://www.kugou.com/yy/rank/home/1-31310.html?from=rank'
html = requests.get(url)
re_com = re.compile('{"Hash":"(.*?)"')
id_com = re.compile('album_id":(.*?),"')
result = re_com.findall(html.text)
id_result = id_com.findall(html.text)
print(result)
print(id_result)
for l in range(0,len(result)):
    params = {
        'r': 'play/getdata',
        'callback': 'jQuery191043723011127866385_1612237828643',
        'hash': 'ECDDB3B5E327B6089F6398CF5BE2C53F',
        'dfid': '0zPVBz2BcM1k3emCSj0pGcpp',
        'mid': '9816b6ce2d573072d8de94dd6eaed190',
        'platid': '4',
        'album_id': '566776',
        '_': '1612237828647'
    }
    url = 'https://wwwapi.kugou.com/yy/index.php'
    html = requests.get(url,params=params).text
    print(html)
#     start = html.find('{"status"')
#     end = html.find('}}')+len('}}')
# #获取下载url和歌曲名称
#     data = json.loads(html[start:end])['data']#!!!!
#     song_name = data['song_name']
#     url = data['play_url']
#     print('正在下载{}'.format(song_name))
#     if not os.path.exists('kugou'):
#         os.makedirs('kugou')
#     with open('kugou/{}.mp3'.format(song_name),'wb') as f :
#         f.write(requests.get(url).content)