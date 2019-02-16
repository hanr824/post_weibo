

import time 
from login import do_login 
from config import NAME,PASSWD

COOKIE_PATH ='./cookies.text'
print('--process to flush cookies--')
content = do_login(NAME,PASSWD)
cookies = COOKIE_PATH
with open ("cookies","w") as f:
	f.write(str(content))
	print('flush successful')

print ('--flush cookies successful--')