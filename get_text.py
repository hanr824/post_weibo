import re 
import time

import requests
from lxml import etree

from config import USERID,USERNAME

use_text=[]
headers = {
        # "Host":"login.sina.com.cn",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        }

def get_page_url(i):
    '''获取每页的帖子链接'''
    url = 'https://www.duanwenxue.com/shige/aiqingshiju/'+i
    res = requests.get(url,headers=headers)
    html = etree.HTML(res.text)
    links = html.xpath('//div[@class="list-base-article"]/ul/li/a/@href')
    for link in links:
        res = get_msg(link)
        if res :
            return res

def get_text():
    '''获取分页链接'''
    url = 'https://www.duanwenxue.com/shige/aiqingshiju/'
    resp = requests.get(url,headers=headers)
    pattern = r'option value="(.*?)"'
    id_list = re.findall(pattern,resp.text)
    for i in id_list:
        res = get_page_url(i)
        if res:
            return res

def get_msg(link):
    '''解析返回文字信息'''
    url = 'https://www.duanwenxue.com'+link
    res= requests.get(url,headers=headers)
    html = etree.HTML(res.text)
    try:
        text = html.xpath('//div[@class="article-content"]/p')[0]
        t=text.xpath('string(.)')
        if t not in use_text:
            use_text.append(t)
            return t
    except:
        pass

            

