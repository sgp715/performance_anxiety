import os
import sys
import time
import cv2
from multiprocessing import Pool
import numpy as np
from PIL import Image
import asyncio
import aiofiles
import requests
import aiohttp

def dumby(files):
    start = time.time()
    for f in files:
        with open(f,'r') as fim:
            fim.read()
    return time.time() - start

def dumby_requests(urls):
    start = time.time()
    for url in urls:
        # print(url)
        requests.get(url)
    return time.time() - start

def list_helper(l):
    for i in l:
        for i in l:
            for i in l:
                x = 1

def dumby_list(lists):
    start = time.time()
    for l in lists:
        list_helper(l)
    return time.time() - start

async def change_color__async(f):
    async with aiofiles.open(f,'r') as fim:
        im = await fim.read()

def process_async(files):
    start = time.time()
    tasks = [asyncio.ensure_future(change_color__async(f)) for f in files]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    return time.time() - start

async def async_requests_helper(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()

def async_requests(urls):
    start = time.time()
    tasks = [asyncio.ensure_future(async_requests_helper(url)) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    return time.time() - start

def change_color_thread(f):
    with open(f, 'r') as fim:
        im = fim.read()

def process_thread(files, threads=3):
    start = time.time()
    p = Pool(threads)
    p.map(change_color_thread, files)
    return time.time() - start

def thread_requests_helper(url):
    requests.get(url)

def thread_requests(urls, threads=3):
    start = time.time()
    p = Pool(threads)
    p.map(thread_requests_helper, urls)
    return time.time() - start

def thread_lists(lists, threads=3):
    start = time.time()
    p = Pool(threads)
    p.map(list_helper, lists)
    return time.time() - start

def test_fun(input, fun):
    # data = []
    data_file = "test_fun_" + fun.__name__ + ".csv"
    with open(data_file, 'w') as f:
        f.write("input,time\n")
    for i in range(len(input)):
        d = fun(input[:i])
        print(str(i) + " input: " + str(d))
        with open(data_file, 'a+') as f:
            f.write(str(i) + ',' + str(d) + '\n')
        # time.sleep(2)
        # data.append(d)
    # return data

def test_threads(files, fun, threads=100):
    # data = []
    data_file = "test_threads_" + fun.__name__ + ".csv"
    with open(data_file, 'w') as f:
        f.write("threads,time\n")
    for i in range(1, threads + 1):
        d = fun(files[:20], i)
        print(str(i) + " threads: " + str(d))
        with open(data_file, 'a+') as f:
            f.write(str(i) + ',' + str(d) + '\n')
        # time.sleep(2)
        # data.append()
    return data

def get_files(dir_path):
    for root, dirs, files in os.walk(dir_path):
        return [root + '/' + f for f in files]

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Must dir name as cli")
    # files = ["/home/seb/Downloads/house-s1-e1.txt" for i in range(50)]
    if args[1] == "-t":
        test_threads(files, process_thread, 20)
        exit()

    # open file
    files = get_files(args[1])
    test_fun(files, dumby)
    test_fun(files, process_async)
    test_fun(files, process_thread)

    # make requests
    urls = ["http://rentashare.com" for i in range(50)]
    test_fun(urls, dumby_requests)
    test_fun(urls, async_requests)
    test_fun(urls, thread_requests)

    # computation
    lists = [[i for i in range(200)] for i in range(50)]
    test_fun(lists, dumby_list)
    test_fun(lists, thread_lists)
