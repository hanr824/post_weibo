
import requests
from lxml import etree
 
headers = {
    "Host":"tieba.baidu.com",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    }

def get_link():
	url = 'http://tieba.baidu.com/limyoona'
	resp = requests.get(url,headers= headers)
	resp = resp.text
	res=resp.replace(r'<!--','"').replace(r'-->','"')
	html = etree.HTML(res)
	#print(resp.text)
	try:
		con = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
		return con
	except:
		pass

def get_pic_link(url):
	resp = requests.get(url,headers=headers)
	html = etree.HTML(resp.text)
	
	imgs = html.xpath('//div[@class="d_post_content_main d_post_content_firstfloor"]/div/cc/div/img[@class="BDE_Image"]/@src')
		
			
	#print(imgs)
	
	return imgs

def write_imgs(imgs):
	img_url = './img.txt'
	for img in imgs:
		with open('img_url','a') as f:
			f.write(img+'\n')

def get_pic():
	pre_url = 'http://tieba.baidu.com'
	links = get_link()
	for link in links:
		url = pre_url + link
		imgs = get_pic_link(url)
		write_imgs(imgs)

get_pic()