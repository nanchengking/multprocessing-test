# coding=utf-8
import os
import gevent
import urllib2
# add this line when use IO operation
from gevent import monkey;

monkey.patch_all()

'''
******************************* Coroutine with gevent*******************************
'''


def f(n):
    for i in range(n):
        print gevent.getcurrent(), i


def run_in_order():
    g1 = gevent.spawn(f, 1)
    g2 = gevent.spawn(f, 2)
    g3 = gevent.spawn(f, 3)
    g1.join()
    g2.join()
    g3.join()


'''
******************************* use  gevent when IO operation*******************************
'''


def use_io(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))


def run_io():
    gevent.joinall([
        gevent.spawn(use_io, 'https://www.python.org/'),
        gevent.spawn(use_io, 'https://www.yahoo.com/'),
        gevent.spawn(use_io, 'https://github.com/'),
    ])


if __name__ == "__main__":
    # run_in_order()
    run_io()
