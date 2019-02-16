
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
		get_text(link)
		

def get_main():

	'''获取分页链接'''

	url = 'https://www.duanwenxue.com/shige/aiqingshiju/'
	resp = requests.get(url,headers=headers)
	#html = etree.HTML(resp.text)
	#con = html.xpath('//div[@class="list-base-article"]/ul/li/a/@href')
	#CON.extend(con)
	pattern = r'option value="(.*?)"'
	list = re.findall(pattern,resp.text)
	for i in list:
		get_page_url(i)
		
def get_text(link):
		
	url = 'https://www.duanwenxue.com'+link
			#print(url)
	res= requests.get(url,headers=headers)
	html = etree.HTML(res.text)
	try:
		texts = html.xpath('//div[@class="article-content"]/p')[0]
		t=texts.xpath('string(.)')
		#for i in texts:
		# if t not in use_text:
		# 	use_text.append(t)
		# 	#print(t)
		return t
		# else:
		# 	pass
		
	except:
		pass

			

def save_text(t):
	with open('text.txt','a',encoding='utf-8') as f:
		f.write(t+'\n')
