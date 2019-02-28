from __future__ import absolute_import, unicode_literals

import time
import random
import uuid

import requests
import gevent
from gevent import monkey

POOL_SIZE = 20
REQUEST_URL = 'http://localhost:8000/'


def req(id_, num, url=REQUEST_URL):
    start = time.time()
    print('\t[{}-{}] starting request'.format(id_, num))
    sleep_secs = float(random.randrange(10)) / random.randrange(1, 10) - 1
    time.sleep(sleep_secs)
    try:
        requests.get(url)
    except Exception:
        print('\t[{}-{}] FAILED request {:0.2f}s'.format(
            id_, num, time.time() - start,
        ))
    else:
        print('\t[{}-{}] finished request {:0.2f}s'.format(
            id_, num, time.time() - start,
        ))


def task(num=5):
    id_ = uuid.uuid4()
    start = time.time()
    print('[{}] starting {:,d} reqs'.format(id_, num))
    for i in range(num):
        req(id_, i)
    print('[{}] finished {:,d} reqs in {:0.2f}s'.format(
        id_, num, time.time() - start
    ))


def main():
    threads = [gevent.spawn(task) for _ in range(POOL_SIZE)]
    gevent.joinall(threads)


if __name__ == '__main__':
    monkey.patch_all()
    main()
