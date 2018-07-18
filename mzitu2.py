import os

from bs4 import BeautifulSoup

from Download import request


class Mzitu2:

    def start(self, url):
        headers = request.build_headers()
        all_html = request.get(url, headers, 10)
        a_list = BeautifulSoup(all_html.text).find('ul', class_='archives').find_all("a")
        for a in a_list:
            title = a.get_text()
            folder = str(title).replace('?', '_')
            self.mkdir(folder)
            page_url = a['href']
            try:
                self.inner_page(page_url, url)
            except AttributeError:
                print("inner_page error:", AttributeError)

    def inner_page(self, page_url, referer):
        headers = request.build_headers(referer=referer)
        inner_html = request.get(page_url, headers, 10)
        max_span = BeautifulSoup(inner_html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page_num in range(1, int(max_span) + 1):
            next_page = page_url + '/' + str(page_num)
            self.get_img(next_page, page_url)

    def mkdir(self, folder):
        folder = folder.strip()
        isExists = os.path.exists(os.path.join("E:/python/picture", folder))
        folder_path = os.path.join("E:/python/picture", folder)
        if not isExists:
            os.makedirs(folder_path)
        os.chdir(folder_path)

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
Mzitu.start('http://www.mzitu.com/all')
