import random
import time

import requests


# socket.setdefaulttimeout(3)


class Download:

    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"]
        self.iplist = set()
        file_path = 'E:/python/ip_proxy_' + time.strftime('%Y%m%d') + '_n.txt'
        f = open(file_path, 'r')
        for ip in f:
            self.iplist.add(ip)
        f.close()
        self.iplist = list(self.iplist)
        print(self.iplist)

    def build_headers(self, **kwargs):
        headers = {'User_Agent': random.choice(self.user_agent_list)}
        if kwargs:
            headers.update(kwargs)
        return headers

    # 可能会死循环
    def get(self, url, headers, timeout, proxy=True, num_retries=6):
        if proxy:
            ip = str(random.choice(self.iplist)).strip()
            print(ip)
            proxy = {'http': ip}
            try:
                response = requests.get(url, headers=headers, proxies=proxy)
                print(url, response.status_code, '使用代理')
                if response.status_code != 200:
                    if num_retries > 0:
                        return self.get(url, headers, timeout, num_retries=num_retries - 1)
                    else:
                        print(url, '放弃请求！')
                return response
            except:
                print('代理失败，正在重新请求：', num_retries)
                if num_retries > 0:
                    time.sleep(3)
                    return self.get(url, headers, timeout, num_retries=num_retries - 1)
                else:
                    return self.get(url, headers, timeout, False)
        else:
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                print(url, response.status_code, "没有代理")
                if response.status_code != 200:
                    if num_retries > 0:
                        return self.get(url, headers, timeout, False, num_retries=num_retries - 1)
                    else:
                        print(url, '放弃请求！')
                return response
            except:
                print('请求失败，正在重新请求：', num_retries)
                time.sleep(3)
                if num_retries > 0:
                    return self.get(url, headers, timeout, False, num_retries=num_retries - 1)
                else:
                    print(url, '放弃请求！')


request = Download()
