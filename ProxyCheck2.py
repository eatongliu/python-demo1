# encoding=utf8
import socket
import threading
import time
import urllib.request

socket.setdefaulttimeout(3)
iplist = []


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
    for proxy_addr in proxys:
        try:
            res = use_proxy(proxy_addr.strip())
            # print(res)
            print(proxy_addr)
            iplist.append(proxy_addr.strip())
        except Exception as e:
            # print(proxy_addr, str(e))
            continue
    f.close()


def start():
    threads = []
    t1 = threading.Thread(target=getip, args=('D:/kuaidaili_' + time.strftime('%Y%m%d') + '.txt',))
    t2 = threading.Thread(target=getip, args=('D:/xicidaili_' + time.strftime('%Y%m%d') + '.txt',))
    t3 = threading.Thread(target=getip, args=('D:/66ip_' + time.strftime('%Y%m%d') + '.txt',))
    t1.start()
    t2.start()
    t3.start()
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)

    for t in threads:
        t.join()

    n_f = open("E:/python/ip_list20180612_n.txt", 'w')
    n_f.write('\n'.join(set(iplist)))
    n_f.close()


start()
