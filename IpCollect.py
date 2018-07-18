import time

from IpProxy import kuaidaili
from IpProxy2 import xicidaili
from IpProxy3 import ip66
import threading

file_path = 'E:/python/ip_proxy_' + time.strftime('%Y%m%d') + '.txt'
t1 = threading.Thread(target=kuaidaili.start, args=(file_path,))
t2 = threading.Thread(target=xicidaili.start, args=(file_path,))
t3 = threading.Thread(target=ip66.start, args=(file_path,))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()
