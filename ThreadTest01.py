import threading
import time
from concurrent.futures import ThreadPoolExecutor


def test():
    for j in range(5):
        print('running thread id : %s   now=%d' % (threading.currentThread().ident, j))


pool = ThreadPoolExecutor(5)

for i in range(100):
    pool.submit(test())
