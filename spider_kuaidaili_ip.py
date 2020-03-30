"""测试过代码完全可行"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

"""抓取免费ip"""
my_headers = {
    "Cookie": 'channelid=0; sid=1584497388180350; _ga=GA1.2.2002581637.1584497921; _gid=GA1.2.616050302.1584497921;'
              ' Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1584497921; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1584497921',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

df1 = pd.DataFrame()
for page in range(1, 999):
    print(page)
    url = 'https://www.kuaidaili.com/free/intr/' + str(page)
    data = requests.get(url, headers=my_headers)
    soup = BeautifulSoup(data.text, 'lxml')
    ips = soup.find_all('tr')
    for i in range(1, len(ips)):
        print(i)
        ip = ips[i].find_all('td')[0].text
        port = ips[i].find_all('td')[1].text
        type = ips[i].find_all('td')[3].text

        """测试ip是否成功"""
        proxies = {
            'https': str(ip) + ":" + str(port)
        }
        print(proxies)
        urll = "https://blog.sodsec.com/ip.php"
        try:
            data = requests.get(urll, proxies=proxies, headers=my_headers, timeout=60)
            print("代理ip为" + str(proxies) + "访问ip为" + data.text)
            df = pd.DataFrame({"IP": ip, "port": port, "type": type}, index=[0])
            df1 = pd.concat([df, df1], axis=0)
            df1.to_csv('./ip .csv', mode='a+',  encoding='utf_8_sig', index=None)  # 可以保存到数据库
        except:
            print("connect failed")
        else:
            print('success')
