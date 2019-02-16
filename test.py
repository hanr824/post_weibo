import time 
from config import USERID,USERNAME
import requests
import base64


def get_data(url):
	#pre_url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1550151117959&di=51e635be142b017ffa877907348086c0&imgtype=0&src=http%3A%2F%2Fpic1.win4000.com%2Fwallpaper%2Fc%2F567a6bc736e71.jpg'
	#pre_url ='http://imgsrc.baidu.com/forum/w%3D580/sign=d44efe1c174c510faec4e21250582528/ea9069061d950a7b51026e1007d162d9f3d3c943.jpg'
	#print(url)
	resp = requests.get(url)
	if resp.status_code == 200:
		content = resp.content
	b64_data = base64.b64encode(content)
	#print(b64_data)
	data = {'b64_data':b64_data}

	return data

def get_pic(data,USERID,USERNAME):
	headers = {
    # "Host":"login.sina.com.cn",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    }

	
	#print(cookies)

	url = 'https://picupload.weibo.com/interface/pic_upload.php?cb=https%3A%2F%2Fweibo.com%2Faj%2Fstatic%2Fupimgback.html%3F_wv%3D5%26callback%3DSTK_ijax_{}&mime=image%2Fjpeg&data=base64&url=weibo.com%2Fu%2F{}&markpos=1&logo=1&nick=%40{}&marks=0&app=miniblog&s=rdxt&pri=null&file_source=1'
	url = url.format(str(int(time.time()*1000000)),USERID,USERNAME)
	#print(url)

	res = requests.post(url,data=data,cookies=cookies,headers=headers)
	if res.status_code ==200:
		#print(res.url)
		pid =res.url.split("pid=")[-1]
		print(pid)

with open('cookies','r') as f:
	content = f.read()
cookies = eval(content)

f=  open('img_url','r') 
while True:

	img_url = f.readline().replace('\n','')

	data = get_data(img_url)
	get_pic(data,USERID,USERNAME)

