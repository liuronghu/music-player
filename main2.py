import time
import urllib

import mp3play
from urllib import request
import requests

# 显示进度



def callbackfunc(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print('下载进度' + '%.2f%%' % percent)


def play(event):
    # mp3 = mp3play.load(r'http://music.163.com/song/media/outer/url?id=391568.mp3')
    # mp3 = mp3play.load('http://music.163.com/song/media/outer/url?id=%d.mp3' % self.list_url[sy])
    # time.sleep(1000000)
    url = r'http://music.163.com/song/media/outer/url?id=391568.mp3'
    req = request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
    html = urllib.request.urlopen(req).read()
    with open('liu.mp3','wb') as f:
        f.write(html)
    # filepath, _=request.urlretrieve(r'http://music.163.com/song/media/outer/url?id=391568.mp3', 'six' + '.mp3', callbackfunc)
    # print(filepath)
    # time.sleep(1000000)


play(10)
