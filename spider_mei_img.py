# coding: utf-8
import os
import math
import requests
from time import time
from datetime import datetime
from bs4 import BeautifulSoup
from concurrent import futures

# 初始化一个线程池，最大线程为5
executor = futures.ThreadPoolExecutor(max_workers=2)


class Image_Download():
    def __init__(self, start_url, page_u_want=1):
        # 所有图集列表页的链接
        self.url_list = [(start_url + 'index_%s.html' % str(tmp) if tmp else start_url) for tmp in range(26)]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        self.sesn = requests.Session()
        self.sesn.headers.update(headers)
        self.page_u_want = page_u_want
        self.setup_time = datetime.now().strftime('%Y{}%m{}%d{}%H{}%M{}%S{}').format('年', '月', '日', '时', '分', '秒')
        self.path1 = './%s' % (self.setup_time)
        os.makedirs(self.path1)

    # 获取某一列表页所有图集连接，过程函数等待多线程调用
    def Tmp_get_list_url(self, tmp_url):
        res_text = self.sesn.get(tmp_url).text
        tmp_list = BeautifulSoup(res_text, 'html.parser').select('li>a')
        list = [tmp['href'] for tmp in tmp_list][8:]
        return list

    # 调用多线程获取所有图集连接
    def get_list_url(self):
        fs = []
        print('正在调用多线程获取所有的图集连接,请稍后。。。。。。')
        for tmp in self.url_list[:self.page_u_want]:
            f = executor.submit(self.Tmp_get_list_url, tmp)
            fs.append(f)
        futures.wait(fs)
        res = []
        for f in fs:
            res += f.result()
        return res

    # 获取某一图集的所有分页链接，过程函数等待线程调用
    def Tmp_get_page_url(self, url):
        tt = self.sesn.get(url).text
        soup = BeautifulSoup(tt, 'html.parser')
        # 计算图集中图片数量
        count = soup.select('div.tuji p')[1].text[-4:-1].strip()
        # 获取图集分页链接
        page_list = [(url + '%s.html' % str(tmp + 1) if tmp else url) for tmp in range(math.ceil(int(count) / 5))]
        return page_list

    # 调用多线程获取所有分页链接
    def get_page_url(self):
        urls_list = self.get_list_url()
        print('正在调用多线程获取所有图集的所有分页链接，请稍后。。。。。。')
        fs = []
        for url in urls_list:
            f = executor.submit(self.Tmp_get_page_url, url)
            fs.append(f)
        futures.wait(fs)
        res = []
        for f2 in fs: res += f2.result()
        return res

    # 获取某一页的所有图片下载链接,过程函数等待线程调用
    def Tmp_get_download_url(self, url):
        soup = BeautifulSoup(self.sesn.get(url).text, 'html.parser').select('div.content img')
        picture_list = [tmp1['src'] for tmp1 in soup]
        return picture_list

    # 调用多线程获取所有图片下载链接
    def get_download_url(self):
        urls_list1 = self.get_page_url()
        print('正在调用多线程获取所有图片下载链接，请稍后。。。。。。')
        fs = []
        for url in urls_list1:
            f = executor.submit(self.Tmp_get_download_url, url)
            fs.append(f)
        futures.wait(fs)
        res = []
        for f in fs: res += f.result()
        return res

    # 根据图片，保存某一图片。过程函数等待线程调用
    def Tmp_download_image(self, url):
        res = self.sesn.get(url)
        with open(self.path1 + '/' + ('_'.join(url.split('/')[-2:])), 'wb') as file:
            # 将数据的二进制形式写入文件中
            file.write(res.content)

    # 调用多线程，保存全部图片
    def download_image(self):
        urls_list = self.get_download_url()
        print('正在调用多线程，下载全部图片')
        fs = []
        for url in urls_list:
            f = executor.submit(self.Tmp_download_image, url)
            fs.append(f)
        futures.wait(fs)


t0 = time()
start_url = 'https://m.lanvshen.com/x/12/'
page_u_want = 1  # 注意这里的页数不要弄得太大，我下载一页就40个图集3500多个图片 1.2个G的内存
image = Image_Download(start_url, page_u_want)
res = image.download_image()
t1 = time()
count = len(os.listdir(image.path1))
print('共下载了%s张图片，耗时%0.2f秒，平均每张耗时%0.2f秒' % (count, t1 - t0, (t1 - t0) / count))
