import requests
import base64
from config import USERID,USERNAME
import time


with open('cookies','r') as f:
	content = f.read()
cookies = eval(content)
F = open('img_url','r')
G = open('text.txt','rb')

def get_data(url):
	#pre_url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1550151117959&di=51e635be142b017ffa877907348086c0&imgtype=0&src=http%3A%2F%2Fpic1.win4000.com%2Fwallpaper%2Fc%2F567a6bc736e71.jpg'
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
    'Referer':'https://weibo.com/u/{}/home?topnav=1&wvr=6'.format(USERID),
    }

	
	#print(cookies)

	url = 'https://picupload.weibo.com/interface/pic_upload.php?cb=https%3A%2F%2Fweibo.com%2Faj%2Fstatic%2Fupimgback.html%3F_wv%3D5%26callback%3DSTK_ijax_{}&mime=image%2Fjpeg&data=base64&url=weibo.com%2Fu%2F{}&markpos=1&logo=1&nick=%40{}&marks=0&app=miniblog&s=rdxt&pri=null&file_source=1'
	url = url.format(str(int(time.time()*1000000)),USERID,USERNAME)
	print(url)

	res = requests.post(url,data=data,cookies=cookies,headers=headers)
	print(res.status_code)
	if res.status_code ==200:
		print(res.url)
		
		pid =res.url.split("pid=")[-1]
		print(pid)
	return pid

def post_weibo():
	print('-----')

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
			pre_url = F.readline().replace('\n','')
			print(pre_url)
			
			datas = get_data(pre_url)
			pid = get_pic(datas,USERID,USERNAME)
		except:
			pid = '006OKj2Gly1g084uj8x5rj31c00u043h'
			
			
		with open('cookies','r') as f:
			content = f.read()
		cookies = eval(content)
			
			
		text = G.readline().decode('utf-8')
		
		print(text)

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
		#print(data)
		


		resp = requests.post(url=url,data= data,headers=headers,cookies=cookies)
		print(resp.status_code)
		if resp.status_code ==200:
			print("successful")
			time.sleep(20)
		else:
			print('not successful')
		


post_weibo()

