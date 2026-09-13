#################################
# 视频相关内容
#################################

import requests
import os
import re
from bs4 import BeautifulSoup
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 视频文件夹
def mkdir():
    if not os.path.exists("videos"):
        os.makedirs("videos",exist_ok=True)

# 总信息
# 标题+网页地址+m3u8地址
def read_url(video_url_path):
    details = {}
    with open(f"{video_url_path}","r") as file:
        urls = [line.strip() for line in file if line.strip()]
        for url in urls:
            respon = requests.get(url=url,headers=headers).content
            # 标题
            soup = BeautifulSoup(respon,'html.parser')
            title = soup.find('title').text.split(' - J')[0]

            # 网页地址
            web_url = url

            # m3u8地址
            tree = html.fromstring(respon)
            xpath = "//section[1]/script[2]"
            script_text = tree.xpath(xpath)[0].text
            m3u8_url = re.findall(r"var\s+hlsUrl\s*=\s*['\"](.*?)['\"]",script_text,re.DOTALL)[0]
            details[title] = {"title":title,"web_url":web_url,"m3u8_url":m3u8_url}

        return details
if __name__ == '__main__':
    read_url()