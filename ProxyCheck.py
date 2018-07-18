# encoding=utf8
import socket
import time
import urllib.request
from multiprocessing.pool import Pool

socket.setdefaulttimeout(3)


def use_proxy(proxy_addr):
    url = "http://ip.chinaz.com/getip.aspx"
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf8')
    return data


def getip(file_path):
    f = open(file_path)
    proxys = f.readlines()
    f.close()
    if __name__ == '__main__':
        pool = Pool(10)
        pool.map(check, proxys)
        pool.close()
        pool.join()


def check(proxy_addr):
    try:
        res = use_proxy(proxy_addr.strip())
        print(res)
        n_f = open('E:/python/ip_proxy_' + time.strftime('%Y%m%d') + '_n.txt', 'a')
        n_f.write(proxy_addr)
        n_f.close()
    except Exception as e:
        print(str(e))


def start():
    file_path = 'E:/python/ip_proxy_' + time.strftime('%Y%m%d') + '.txt'
    getip(file_path)


start()
