# 课题：爬取酷6全站视频
# 根目录下需要有img文件夹
# requests
# json

import requests  # pip install requests
import json
import re


def change_title(title):
    """处理文件名非法字符的方法"""
    pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")  # '/ \ : * ? " < > |'
    new_title = re.sub(pattern, "_", title)  # 替换为下划线
    return new_title


for page in range(0, 10):
    print('++++++++++++++++正在抓取第{}页数据+++++++++++++++++++++'.format(page + 1))
    # 爬虫的一般思路
    # 1、分析目标网页，确定爬取的url路径，headers参数
    base_url = 'https://www.ku6.com/video/feed?pageNo={}&pageSize=40&subjectId=76'.format(str(page))
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko'
                      ') Chrome/73.0.3683.86 Safari/537.36'}

    # 2、发送请求 -- requests 模拟浏览器发送请求，获取响应数据
    response = requests.get(base_url, headers=headers)
    data = response.text
    # print(data)

    # 3、解析数据 -- json模块：把json字符串转化成python可交互的数据类型
    # 3、1 转换数据类型
    json_data = json.loads(data)
    # 3、2 数据提取
    data_list = json_data['data']
    # print(data_list)

    # 遍历列表
    for data1 in data_list:
        video_name = data1['title'] + '.mp4'
        video_url = data1['playUrl']
        # print(video_name, video_url)

        new_title = change_title(video_name)

        # 再次发送视频的请求
        print('正在下载：', video_name)
        video_data = requests.get(video_url, headers=headers).content  # 视频的数据

        # 4、保存数据 -- 保存在目标文件夹中
        with open('video\\' + new_title, 'wb') as f:
            f.write(video_data)
            print('下载完成。。。\n')
