import time

import requests
from bs4 import BeautifulSoup


base_url = 'https://www.kuaidaili.com/free/inha'


class IpProxy:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.iplist = []

    def start(self, file_path):
        f = open(file_path, 'a')
        try:
            for page_num in range(1, 10):
                next_page = base_url + '/' + str(page_num)
                time.sleep(5)
                self.get_ip(next_page)
        except Exception as e:
            print('出错了' + str(e))
        f.write('\n'.join(set(self.iplist)) + "\n")
        f.close()

    def get_ip(self, page_url):
        html = self.request(page_url)
        print(page_url, html.status_code)
        tr_list = BeautifulSoup(html.text).find('div', id='list').find('tbody').find_all('tr')
        for tr in tr_list:
            ip = tr.find('td', attrs={"data-title": "IP"}).get_text()
            port = tr.find('td', attrs={"data-title": "PORT"}).get_text()
            self.iplist.append(str(ip) + ":" + str(port))

    def request(self, url):
        return requests.get(url, headers=self.headers)


kuaidaili = IpProxy()
# file_path = 'E:/python/ip_proxy_' + time.strftime('%Y%m%d') + '.txt'
# kuaidaili.start(file_path)
