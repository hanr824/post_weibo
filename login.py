import re 
import time 
import base64 
import rsa
import requests
import binascii
import math
import random
from urllib.parse import quote_plus


VERIFY_CODE_PATH = './{}.png'


headers = {
    # "Host":"login.sina.com.cn",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    }

def get_encodename(name):
    '''name must be string'''
    username_quote = quote_plus(str(name))
    username_base64 = base64.b64encode(username_quote.encode('utf-8'))
    return username_base64.decode('utf-8')

def get_password(password, servertime, nonce, pubkey):
    """get a encrypt password"""
    rsa_publickey = int(pubkey, 16)
    key = rsa.PublicKey(rsa_publickey, 65537)
    message =bytes(str(servertime) + '\t' + str(nonce) + '\n' + str(password),encoding=('utf-8'))
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    #print(passwd)
    return passwd

def get_pincode_url(pcid):
    """组装获取验证码的url"""
    url = 'https://login.sina.com.cn/cgi/pin.php'
    pincode_url ='{}?r={}&s=0&p={}'.format(url,math.floor(random.random() * 100000000),pcid)
    #print(pincode_url)
    return pincode_url

def get_img(name,img_url):
    pincode_name = VERIFY_CODE_PATH.format(name)
    res = requests.get(img_url,headers = headers,stream=True)
    with open('pincode_name','wb') as f:
        for i in res.iter_content(1000):
            f.write(i)

def get_redirect(post_url,data,name,session):
    resp = session.post(post_url,data=data,headers=headers)
    login_loop = resp.content.decode("GBK")
    #print(login_loop)
    
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    print (re.findall(pa, login_loop)[0])
    return re.findall(pa, login_loop)[0]



def get_server_data(su):
    pre_url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su='
    pre_url = pre_url+su+'&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_='
    prelogin_url = pre_url + str(int(time.time()*1000))
    pre_data_res = requests.get(prelogin_url,headers = headers)
    server_data = eval(pre_data_res.content.decode('utf-8').replace('sinaSSOController.preloginCallBack',''))
   #print(server_data)
    return server_data

def login_no_pincode(name,passwd,session,server_data):
    post_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    servertime = server_data["servertime"]
    nonce = server_data['nonce']
    rsakv = server_data["rsakv"]
    pubkey = server_data["pubkey"]
    sp = get_password(passwd,servertime,nonce,pubkey)
    data = {
        'encoding': 'UTF-8',
        'entry': 'weibo',
        'from': '',
        'gateway': '1',
        'nonce': nonce,
        'pagerefer': "",
        'prelt': 67,
        'pwencode': 'rsa2',
        "returntype": "META",
        'rsakv': rsakv,
        'savestate': '7',
        'servertime': servertime,
        'service': 'miniblog',
        'sp': sp,
        'sr': '1920*1080',
        'su': get_encodename(name),
        'useticket': '1',
        'vsnf': '1',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
    }
    rs = get_redirect(post_url,data,name,session)
    return rs 

def login_by_pincode(name,passwd,session,server_data):
    post_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    servertime = server_data["servertime"]
    nonce = server_data['nonce']
    rsakv = server_data["rsakv"]
    pubkey = server_data["pubkey"]
    pcid = server_data['pcid']
    sp = get_password(passwd,servertime,nonce,pubkey)
    data = {
        'encoding': 'UTF-8',
        'entry': 'weibo',
        'from': '',
        'gateway': '1',
        'nonce': nonce,
        'pagerefer': "",
        'prelt': 67,
        'pwencode': 'rsa2',
        "returntype": "META",
        'rsakv': rsakv,
        'savestate': '7',
        'servertime': servertime,
        'service': 'miniblog',
        'sp': sp,
        'sr': '1920*1080',
        'su': get_encodename(name),
        'useticket': '1',
        'vsnf': '1',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'pcid': pcid
    }
    img_url = get_pincode_url(pcid)
    get_img(name,img_url)
    data['door'] = input("please input verify_code...")
    rs = get_redirect(post_url,data,name,session)
    return rs 

def do_login(name,passwd):
    session = requests.Session()
    su = get_encodename(name)
    server_data = get_server_data(su)
    if server_data['showpin']:
        url=login_by_pincode(name,passwd,session,server_data)
        re = session.get(url,headers=headers)
        return session.cookies.get_dict()
    else:
        url = login_no_pincode(name,passwd,session,server_data)
        re = session.get(url,headers=headers)
        return session.cookies.get_dict()
