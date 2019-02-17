
import base64
import time

import requests

from config import USERID,USERNAME
from get_pic import get_pic
from get_text import get_text



with open('cookies','r') as f:
    content = f.read()
cookies = eval(content)


def get_data(url):
    """获取图片base64转码后的信息"""
    resp = requests.get(url)
    if resp.status_code == 200:
        content = resp.content
    b64_data = base64.b64encode(content)
    data = {'b64_data':b64_data}
    return data

def get_pic_pid(data,USERID,USERNAME):
    """获取pic_id参数，用于post时发送图片信息"""
    headers = {
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    'Referer':'https://weibo.com/u/{}/home?topnav=1&wvr=6'.format(USERID),
    }
    url = 'https://picupload.weibo.com/interface/pic_upload.php?cb=https%3A%2F%2Fweibo.com%2Faj%2Fstatic%2Fupimgback.html%3F_wv%3D5%26callback%3DSTK_ijax_{}&mime=image%2Fjpeg&data=base64&url=weibo.com%2Fu%2F{}&markpos=1&logo=1&nick=%40{}&marks=0&app=miniblog&s=rdxt&pri=null&file_source=1'
    url = url.format(str(int(time.time()*1000000)),USERID,USERNAME)
    print(url)
    res = requests.post(url,data=data,cookies=cookies,headers=headers)
    if res.status_code ==200:
        pid =res.url.split("pid=")[-1]
    return pid

def post_weibo():
    """自动发送图片文字微博函数"""
    url = 'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd={}'.format(int(1000*time.time()))
    headers = {
    "Host":"weibo.com",
    "Connection":"keep-alive",
    "Content-Length":"179",
    "Origin":"https://weibo.com",
    "X-Requested-With":"XMLHttpRequest",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
    "Referer":"https://weibo.com/u/{}/home".format(USERID),
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    }
    while True: 
        try:
            img = get_pic()
            datas = get_data(img)
            pid = get_pic_pid(datas,USERID,USERNAME)
        except:
            pid = '006OKj2Gly1g084uj8x5rj31c00u043h'
        text = get_text()
        data ={
            'location':'v6_content_home',
            'text':text,
            'appkey':"",
            'style_type':'1',
            'pic_id':pid,
            'tid':'',
            'pdetail':'',
            'mid':'',
            'isReEdit':'false',
            'gif_ids':'',
            'rank':'0',
            'rankid':'',
            'module':"stissue",
            'pub_source':'main_',
            'updata_img_num':'1',
            'pub_type':'dialog',
            'isPri':'null',
            '_t':'0',
                }
        resp = requests.post(url=url,data= data,headers=headers,cookies=cookies)
        print(resp.status_code)
        if resp.status_code ==200:
            print("successful")
            time.sleep(100)
        else:
            print('not successful')

if __name__ == '__main__':
    post_weibo()

