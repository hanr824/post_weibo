import requests
from lxml import etree
import re 
import time


from config import USERID,USERNAME

headers = {
	    # "Host":"login.sina.com.cn",
	    "Connection":"keep-alive",
	    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	    "Accept":"*/*",
	    "Accept-Encoding":"gzip, deflate, br",
	    "Accept-Language":"zh-CN,zh;q=0.9",
	    }

def get_page_url(url):
	res = requests.get(url,headers=headers)
	html = etree.HTML(res.text)
	links = html.xpath('//div[@class="list-base-article"]/ul/li/a/@href')
	for link in links:
		url = 'https://www.duanwenxue.com'+link
		#print(url)
		get_text(url)
		

def get_main_url():
	CON = []

	url = 'https://www.duanwenxue.com/shige/aiqingshiju/'
	

	resp = requests.get(url,headers=headers)
	#html = etree.HTML(resp.text)
	#con = html.xpath('//div[@class="list-base-article"]/ul/li/a/@href')
	#CON.extend(con)
	pattern = r'option value="(.*?)"'
	list = re.findall(pattern,resp.text)
	for i in list:
		url = 'https://www.duanwenxue.com/shige/aiqingshiju/'+i
		get_page_url(url)
		
	
	#print(CON)

def get_text(url):

	res= requests.get(url,headers=headers)

	html = etree.HTML(res.text)
	try:
		texts = html.xpath('//div[@class="article-content"]/p')[0]
	
		t=texts.xpath('string(.)')
		#for i in texts:

		post_text(t)
	except:
		pass

def save_text(t):
	with open('text.txt','a',encoding='utf-8') as f:
		f.write(t+'\n')

	




get_main_url()