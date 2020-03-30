import threading  # 导入threading模块
from queue import Queue  # 导入queue模块
import time  # 导入time模块
import requests
import os
from lxml import etree as et

# 请求头
headers = {
    # 用户代理
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
# 待抓取网页基地址
base_url = 'https://www.23jj.com/c/qingchun/'
# 保存图片基本路径
base_dir = './img/'


# 保存图片
def savePic(pic_url):
    # 如果目录不存在，则新建
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    arr = pic_url.split('/')
    file_name = base_dir + arr[-2] + arr[-1]
    print(file_name)
    # 获取图片内容
    response = requests.get(pic_url, headers=headers)
    # 写入图片
    with open(file_name, 'wb') as fp:
        for data in response.iter_content(128):
            fp.write(data)


# 爬取文章详情页
def get_detail_html(detail_url_list, id):
    while True:
        url = detail_url_list.get()  # Queue队列的get方法用于从队列中提取元素
        response = requests.get(url=url, headers=headers)
        # 请求状态码
        code = response.status_code
        if code == 200:
            html = et.HTML(response.text)
            # 获取页面所有图片地址
            r = html.xpath('//li/a/img/@src')
            # 获取下一页url
            # t = html.xpath('//div[@class="page"]/a[@class="ch"]/@href')[-1]
            for pic_url in r:
                a = 'http:' + pic_url
                savePic(a)


# 爬取文章列表页
def get_detail_url(queue):
    for i in range(1, 100):
        # time.sleep(1) # 延时1s，模拟比爬取文章详情要快
        # Queue队列的put方法用于向Queue队列中放置元素，由于Queue是先进先出队列，所以先被Put的URL也就会被先get出来。
        page_url = base_url + format(i)
        queue.put(page_url)
        print("put page url {id} end".format(id=page_url))  # 打印出得到了哪些文章的url


# 主函数
if __name__ == "__main__":
    detail_url_queue = Queue(maxsize=1000)  # 用Queue构造一个大小为1000的线程安全的先进先出队列
    # A线程负责抓取列表url
    thread = threading.Thread(target=get_detail_url, args=(detail_url_queue,))
    html_thread = []
    # 另外创建三个线程负责抓取图片
    for i in range(20):
        thread2 = threading.Thread(target=get_detail_html, args=(detail_url_queue, i))
        html_thread.append(thread2)  # B C D 线程抓取文章详情
    start_time = time.time()
    # 启动四个线程
    thread.start()
    for i in range(20):
        html_thread[i].start()
    # 等待所有线程结束，thread.join()函数代表子线程完成之前，其父进程一直处于阻塞状态。
    thread.join()
    for i in range(20):
        html_thread[i].join()
    print("last time: {} s".format(time.time() - start_time))  # 等ABCD四个线程都结束后，在主进程中计算总爬取时间。
