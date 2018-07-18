import os

import requests
from bs4 import BeautifulSoup


class mzitu():
    def __init__(self):
        # 浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    def start(self, url):
        all_html = self.request(url)
        a_list = BeautifulSoup(all_html.text).find('ul', class_='archives').find_all("a")
        for a in a_list:
            title = a.get_text()
            folder = str(title).replace('?', '_')
            self.mkdir(folder)
            page_url = a['href']
            try:
                self.inner_page(page_url)
            except AttributeError:
                print("Unexpected error:", AttributeError)

    def inner_page(self, page_url):
        inner_html = self.request(page_url)
        self.headers['referer'] = page_url
        print(page_url, inner_html.status_code)
        max_span = BeautifulSoup(inner_html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page_num in range(1, int(max_span) + 1):
            next_page = page_url + '/' + str(page_num)
            self.get_img(next_page)

    def request(self, url):
        return requests.get(url, headers=self.headers)

    def mkdir(self, folder):
        folder = folder.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", folder))
        folder_path = os.path.join("D:\mzitu", folder)
        if not isExists:
            os.makedirs(folder_path)
        os.chdir(folder_path)

    def save_img(self, src):
        name = src[-9:-4]
        img = self.request(src)
        # print(src, img.status_code)
        file = open(name + '.jpg', 'wb')
        file.write(img.content)
        file.close()

    def get_img(self, page_url):
        img_html = self.request(page_url)
        src = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save_img(src)


Mzitu = mzitu()
Mzitu.start('http://www.mzitu.com/all')
