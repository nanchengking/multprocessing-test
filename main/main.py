# coding=utf-8
from multiprocessing import Pool, Process, Queue, Pipe
import time, os


def f(x):
    return x * x


def hello(name):
    print 'hello', name
    info(name)
    time.sleep(3)


def use_pool():
    '''
     parallelizing the execution of a function across multiple input values 
    :return: 
    '''
    p = Pool(5)
    print(p.map(f, [1, 2, 3]))


def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()


def use_process():
    '''
    a multiprocess program
    :return: 
    '''
    p = Process(target=hello, args=('bob',))
    p.start()
    # wait until p was finished
    print 'wait p', time.time()
    p.join()
    print 'p finish', time.time()


def show_process_info():
    info('main line')
    p1 = Process(target=hello, args=('p1',))
    p1.start()
    p2 = Process(target=hello, args=('p2',))
    p2.start()
    # p1.join()


def put_data(q):
    q.put([42, None, 'hello'])


def exchange_by_queue():
    '''
    Queues are thread and process safe.
    if queue is empty, call q.get() will block until there are values,or q.get(False) means get with out wait ,if empty, get a nep
    as the same,q.put(True or False) means put data block or not
    :return: 
    '''
    q = Queue()
    # print q.get()
    p = Process(target=put_data, args=(q,))
    p.start()
    print q.get()  # prints "[42, None, 'hello']"
    p.join()


def send_data(conn):
    conn.send([42, None, 'hello'])
    conn.close()


def exchange_by_pip():
    '''
    The two connection objects returned by Pipe() represent the two ends of the pipe. 
    Each connection object has send() and recv() methods (among others). 
    Note that data in a pipe may become corrupted if two processes (or threads) try to read from or write to the same end of the pipe at the same time.
    Of course there is no risk of corruption from processes using different ends of the pipe at the same time.
    :return: 
    '''
    parent_conn, child_conn = Pipe()
    p = Process(target=send_data, args=(child_conn,))
    p.start()
    print parent_conn.recv()  # prints "[42, None, 'hello']"
    p.join()


if __name__ == '__main__':
    # use_pool()
    # use_process()
    # show_process_info()
    # exchange_by_queue()
    exchange_by_pip()
