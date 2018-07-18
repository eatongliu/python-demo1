import os
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from Download import request

base_url = 'http://www.ygdy8.net/html/gndy/dyzz/'


def mkdir(folder):
    folder = folder.strip()
    isExists = os.path.exists(os.path.join("E:\python\dyzz", folder))
    folder_path = os.path.join("E:\python\dyzz", folder)
    if not isExists:
        os.makedirs(folder_path)
    os.chdir(folder_path)


class Mzitu2:

    def start(self, url):
        headers = request.build_headers()
        all_html = request.get(url, headers, 10)
        options = BeautifulSoup(all_html.text, 'lxml').find('select', attrs={'name': 'sldd'})
        # options = BeautifulSoup(all_html.text, 'lxml').select('select[name="sldd"]')
        if __name__ == '__main__':
            pool = ThreadPoolExecutor(10)
            pool.map(self.inner_page, options, url)
            pool.shutdown()
            # for option in options:
            #     try:
            #         pool.submit(self.inner_page, option, url)
            #     except AttributeError:
            #         print("inner_page error:", AttributeError)

    def inner_page(self, option, referer):
        print(base_url + option['value'])
        print(referer)
        # try:
        #     headers = request.build_headers(referer=referer)
        #     inner_html = request.get(page_url, headers, 10)
        #     max_span = BeautifulSoup(inner_html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[
        #         -2].get_text()
        #     for page_num in range(1, int(max_span) + 1):
        #         next_page = page_url + '/' + str(page_num)
        #         self.get_img(next_page, page_url)
        # except Exception as e:
        #     print(str(e))

    def save_img(self, src, referer):
        headers = request.build_headers(referer=referer)
        img = request.get(src, headers, 10)
        name = src[-9:-4] + '.' + src[-3:]
        file = open(name, 'ab')
        file.write(img.content)
        file.close()

    def get_img(self, page_url, referer):
        headers = request.build_headers(referer=referer)
        img_html = request.get(page_url, headers, 10)
        src = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save_img(src, referer)


Mzitu = Mzitu2()
Mzitu.start('http://www.ygdy8.net/html/gndy/dyzz/index.html')
