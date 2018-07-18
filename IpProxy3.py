import time

import requests
from bs4 import BeautifulSoup

base_url = 'http://www.66ip.cn/'


class IpProxy:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.iplist = []

    def start(self, file_path):
        f = open(file_path, 'a', encoding='utf-8')
        try:
            for page_num in range(1, 10):
                next_page = base_url + str(page_num) + '.html'
                self.get_ip(next_page)
                time.sleep(5)
        except Exception as e:
            print('出错了' + e)
        f.write('\n'.join(set(self.iplist)) + "\n")
        f.close()

    def get_ip(self, page_url):
        html = self.request(page_url)
        print(page_url, html.status_code)
        tr_list = BeautifulSoup(html.text).find('div', class_='containerbox boxindex').find_all('tr')
        for i in range(1, len(tr_list)):
            tds = tr_list[i].find_all('td')
            self.iplist.append(str(tds[0].get_text()) + ":" + str(tds[1].get_text()))

    def request(self, url):
        return requests.get(url, headers=self.headers)


ip66 = IpProxy()
# file_path = 'E:/python/ip_proxy_' + time.strftime('%Y%m%d') + '.txt'
# ip66.start(file_path)
