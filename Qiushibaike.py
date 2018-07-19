# -*- coding:utf-8 -*-
import time

import urllib3
from util.MongoDb import mongoDb
from bs4 import BeautifulSoup
import re


class Qiushibaike:

    def __init__(self):
        self.http = urllib3.PoolManager()
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-agent': user_agent}

    def hot(self):
        hot_url = 'https://www.qiushibaike.com/hot/'
        response = self.http.request('get', hot_url, headers=self.headers)
        content = response.data.decode('utf-8')
        pattern = re.compile(r'<ul.*?pagination.*?>(.*?)</ul>', re.S)
        ul = re.findall(pattern, content)[0]
        href = BeautifulSoup(ul).find_all('li')[-2].find('a').attrs['href']
        max_page = re.findall(r'\d+', href)[0]
        for i in range(int(max_page)):
            self.page_save(i + 1)

    def page_save(self, page):
        url = 'https://www.qiushibaike.com/hot/page/' + str(page) + '/'
        try:
            response = self.http.request('get', url, headers=self.headers)
            page_res = response.data.decode('utf-8')
            pattern = re.compile(r'<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<a href="/article/(.*?)".*?<div.*?>(.*?)</div>(.*?)<div class="stats">.*?"number">(.*?)</i>', re.S)
            items = re.findall(pattern, page_res)
            for item in items:
                joke_id = item[1]
                if mongoDb.find_one({'jokeId': joke_id}):
                    continue
                content = item[2]
                ft_pat = re.compile(r'<span class="contentForAll">查看全文</span>', re.S)
                if re.search(ft_pat, content):
                    full_text_url = 'https://www.qiushibaike.com/article/' + joke_id
                    response = self.http.request('get', full_text_url, headers=self.headers)
                    full_text = response.data.decode('utf-8')
                    joke_pat = re.compile(r'<div class="content">.*?</div>', re.S)
                    joke = re.search(joke_pat, full_text)
                else:
                    joke_pat = re.compile(r'<span>(.*?)</span>', re.S)
                    joke = re.findall(joke_pat, content)[0]
                thumb_pat = re.compile(r'<a.*?target="_blank">(.*?)</a>', re.S)
                imgs = re.findall(thumb_pat, item[3])

                joke_dict = {'username': item[0],
                             'jokeId': joke_id,
                             'joke': joke,
                             'likes': item[4],
                             'crawlDate': int(time.time()*1000),
                             'type': 'hot'}
                if len(imgs):
                    joke_dict['imgs'] = imgs
                mongoDb.save(joke_dict)
        except Exception as e:
            print(e)


qiushibaike = Qiushibaike()
qiushibaike.hot()
