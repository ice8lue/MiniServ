import socket
import time
import WConio
import os
import stat
import re

def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fTB' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fGB' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fMB' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fKB' % kilobytes
    else:
        size = '%.2fB' % bytes
    return size

auth = 0

ini = open('settings.ini','r')
ini = ini.readlines()
version = ini[0].split('=')
version = version[1]

logging = ini[2].split('=')
logging = logging[1].split()
logging = logging[0]

uname = ini[3].split()
uname = uname[2]

pw = ini[4].split()
pw = pw[2]


WConio.settitle('MiniServ :: Server Window')
WConio.textmode()

HOST = ''
IP = socket.gethostbyname(socket.gethostname())
PORT = ini[1].split('=')
PORT = int(PORT[1])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((HOST,PORT))

exit = 0

WConio.textcolor(9)

print '>>>>> MiniServ',version


stime = time.strftime("%a, %d %b %Y %H:%M:%S")
print 'Server started at',stime,'\nrunning on',IP,'at Port',PORT,'\n' 

os.chdir('..')
os.chdir('htdocs')
root = os.getcwd()

connections = 0
denied = 0
services = 0
transfered = 0

WConio.textcolor(2)
while 1:
	try:
		s.listen(1)
	
		conns, addr = s.accept()
		data = conns.recv(1024)
		
		flag = 0
		kb = 0
		
		if data == 'OPT':
			
			flag = 1
			if auth == 1 and auth_session == addr[0]:
				conns.send('OK')
				
				cmd = conns.recv(1024)
				
				if cmd == 'EXIT':
					atime = time.strftime("%H:%M")
					print '[',atime,']  Received termination signal! Shutting down server NOW!\n'
					break
					
				if cmd == 'HELO':
					atime = time.strftime("%H:%M")
					print '[',atime,'] Hello',addr[0],'\n'
					continue
					
				if cmd == 'LMIN':
					atime = time.strftime("%H:%M")
					logging = 'minimal'
					print '[',atime,'] Logging set to minimal \n'
					continue
				
				if cmd == 'LMAX':
					atime = time.strftime("%H:%M")
					logging = 'maximal'
					print '[',atime,'] Logging set to maximal \n'
					continue
					
				if cmd == 'TIME':
					atime = time.strftime("%H:%M")
					ltime = time.strftime("%a, %d %b %Y %H:%M:%S %Z")
					conns.send(ltime)
					print '[',atime,'] Timestamp sent to',addr[0],' \n'
					continue	

				if cmd == 'INFO':
					atime = time.strftime("%H:%M")
					infostr = 'Server running since %s \n  %s total connection(s) \n  %s denied connection(s) \n  %s service connection(s)\n  %s transfered \n  Logging: %s' % (stime,connections,denied,services,convert_bytes(transfered),logging)
					conns.send(infostr)
					print '[',atime,'] Infostring sent to',addr[0],' \n'
					continue	

				if cmd == 'DISC':
					atime = time.strftime("%H:%M")
					print '[',atime,']',addr[0],' disconnected\n'
					auth = 0
					auth_session = 0
					continue
				
			else:
				atime = time.strftime("%H:%M")
				print '[',atime,']',addr[0],'requests service access\n'
				conns.send('AUTH')
				user = conns.recv(1024)
				passw = conns.recv(1024)
				if user == uname and passw == pw:
					conns.send('OK')
					auth = 1
					auth_session = addr[0]
					atime = time.strftime("%H:%M")
					print '[',atime,'] Access authorized!\n'
				else:
					atime = time.strftime("%H:%M")
					print '[',atime,'] Access denied!\n'
					conns.send('DENY')

		
		if flag == 0:
			connections = connections + 1
			atime = time.strftime("%H:%M")
			print '[',atime,'] Connected by ',addr[0],'\n'
			WConio.textcolor(15)
			if logging == 'maximal':
				print '%s'%data,
			WConio.textcolor(2)
			req = data.split()
			url = req[1].split('/')
			url[0] = 'self'
			for part in url:
				if part == 'self':
					part = '.'
				else:
					if part == '':
						file_name = 'index.html'
						ta = 'text'
						tb = 'html'
						read_mode = 'r'
					else:
						if re.search('.html', part):
							file_name = part
							ta = 'text'
							tb = 'html'
							read_mode = 'r'
							break
						elif re.search('.xml', part):
							file_name = part
							ta = 'application'
							tb = 'xhtml+xml'
							read_mode = 'r'
							break
						elif re.search('.js', part):
							file_name = part
							ta = 'application'
							tb = 'x-javascript'
							read_mode = 'r'
							break
						elif re.search('.css', part):
							file_name = part
							ta = 'text'
							tb = 'css'
							read_mode = 'r'
							break
						elif re.search('.jpg', part):
							file_name = part
							ta = 'image'
							tb = 'jpg'
							read_mode = 'rb'
							break
						elif re.search('.png', part):
							file_name = part
							ta = 'image'
							tb = 'png'
							read_mode = 'rb'
							break
						elif re.search('.gif', part):
							file_name = part
							ta = 'image'
							tb = 'gif'
							read_mode = 'rb'
							break
						elif re.search('.bmp', part):
							file_name = part
							ta = 'image'
							tb = 'bmp'
							read_mode = 'rb'
							break
						elif re.search('.ico', part):
							file_name = part
							ta = 'image'
							tb = 'x-icon'
							read_mode = 'rb'
							break
						else: 
							if os.path.exists(part):
								os.chdir(part)		
								print '[',atime,'] Entering Directory ',part
							else:
								os.chdir(root)
								WConio.textcolor(4)
								print '[',atime,'] File or Directory does not exist, 404\n'
								file_name = '404.html'
								WConio.textcolor(2)
								break
			if not os.path.exists(file_name):
				if kb == 0:
					os.chdir(root)
					WConio.textcolor(4)
					print '[',atime,'] File or Directory does not exist, 404\n'
					file_name = '404.html'
					ta = 'text'
					tb = 'html'
					WConio.textcolor(2)
				else:
					os.chdir(root)
					WConio.textcolor(4)
					print '[',atime,'] File or Directory does not exist, 404\n'
					WConio.textcolor(2)			

			if kb == 0:
				file_stats = os.stat(file_name)
				fsize = file_stats [stat.ST_SIZE]
				last_modified = time.ctime(os.path.getmtime(file_name))
			else:
				fsize = 0		
			sendtime = time.strftime("%a %b %d %H:%M:%S %Y")	

			print '[',atime,'] Sending HTTP Response \n'
					
			accept = 'HTTP/1.1 200 OK\nDate: '+str(sendtime)+'\nServer: MiniServ/'+str(version)+'Last-Modified: '+str(last_modified)+'\nAccept-Ranges: bytes\nContent-length: '+str(fsize)+'\nConnection: keep-alive\nContent-type: '+str(ta)+'/'+str(tb)+'\n\n'
						
			WConio.textcolor(15)
			if logging == 'maximal':
				print accept,
			WConio.textcolor(2)

			conns.send(accept)

			if kb == 0:
				print '[',atime,'] Sending',file_name,' \n'

				datei = open(file_name,read_mode)
				#for zeile in datei.readlines():
				#	conns.send(zeile)
				conns.sendall(datei.read())
				datei.close
			conns.close()	
			WConio.textcolor(2)	
			atime = time.strftime("%H:%M")
			transfered = transfered + fsize
			print '[',atime,']',convert_bytes(fsize),'sent to',addr[0],'\n\n'
			os.chdir(root)
	except:
		WConio.textcolor(4)
		atime = time.strftime("%H:%M")
		print '[',atime,'] Connection lost!\n'	
		continue