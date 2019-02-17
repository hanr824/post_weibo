import requests
from lxml import etree

use_imgs=[]
headers = {
    "Host":"tieba.baidu.com",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    }

def get_pic():
    '''获取帖子的id'''
    url = 'http://tieba.baidu.com/limyoona'
    resp = requests.get(url,headers= headers)
    resp = resp.text
    res=resp.replace(r'<!--','"').replace(r'-->','"')
    html = etree.HTML(res)
    try:
        cons = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
        for con in cons:
            res = get_link(con)
            if res:
                return res
    except:
        pass

def get_link(con):
    ''' 获取图片url'''
    pre_url = 'http://tieba.baidu.com'
    url = pre_url + con
    resp = requests.get(url,headers=headers)
    html = etree.HTML(resp.text)
    imgs = html.xpath('//div[@class="d_post_content_main d_post_content_firstfloor"]/div/cc/div/img[@class="BDE_Image"]/@src')
    for img in imgs:
        if img not in use_imgs:
            use_imgs.append(img)
            return img
        
        




    
    
    
        
        
        
        
            
            

