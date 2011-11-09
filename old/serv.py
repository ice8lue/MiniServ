#####################################
#		MiniServ - Multithreading Version	   #
#		by Frank Adler, 2010						   #
#####################################

import time
import WConio
import os
import socket
import stat
import re
import threading
import queue
import sys

WConio.settitle('MiniServ :: Server Window')
WConio.textmode()

# Loading settings

auth = 0
ready = 0
wready = 1

connections = 0
services = 0
transfered = 0

inidat = open('settings.ini','r')
ini = inidat.readlines()
inidat.close()
version = ini[0].split('=')
version = version[1].strip()


pwdHashStr = ini[1]

exit = 0

os.chdir('..')
os.chdir('htdocs')
root = os.getcwd()

WConio.textcolor(9)

print('MiniServ '+version+' is starting, please wait...\n')

WConio.textcolor(2)

print('Settings loaded successfully! \n')

# Setting up Socket

HOST = ''
IP = socket.gethostbyname(socket.gethostname())
PORT = 8080
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
print('Socket started on '+str(IP)+' on Port '+str(PORT)+'\n')

SHOST = ''
SPORT = 10104
ssock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssock.bind((SHOST,SPORT))
print('Service Socket started on '+str(IP)+' on Port '+str(SPORT)+'\n')



# Initialize Job-Queue

class JobQueue (queue.Queue):
	def __init__(self):
		queue.Queue.__init__(self)
		self.length = 0
	
	def enqueue(self, data):
		self.length = self.length + 1
		self.data = data
		self.put(self.data)
	
	def dequeue(self):
		self.length = self.length - 1
		data = self.get()
		return data
	
	def getLength(self):
		return self.length


jobs = JobQueue() 

print('Job Queue initialized!\n')

# Defining Threads

threadLock = threading.Lock()
threads = []

###### Main Thread - Listener ##################################
# The Main Thread is 'listening' to the socket. 									  #
# On request, it will enqeue the request to give it to the worker thread  #
###########################################################

class T_Main (threading.Thread):
	def __init__(self, threadID, name):
		super(T_Main,self).__init__()
		self._stop = threading.Event()
		self.threadID = threadID
		self.name = name
		global ready
		global jobs
		
	def stop (self):
		self._stop.set()

	def stopped (self):
		return self._stop.isSet()
				
	def run(self):
		global connections
		global services
		
		if ready == 0:
			time.sleep(0.5)
		elif ready == 1:
			time.sleep(1)
			print("\nTMain ["+time.strftime("%H:%M:%S")+"] == ready, waiting for connections...\n")
			while 1:
				try:
					s.listen(1)
					conns, addr = s.accept()
					data = conns.recv(1024)
					
					print("TMain ["+time.strftime("%H:%M:%S")+"] << Connected by "+addr[0]+"\n")
					
					connections = connections + 1
					job = conns, data,addr[0]
					jobs.enqueue(job)
					print("TMain ["+time.strftime("%H:%M:%S")+"] == Job pushed to Queue\n")
				except:
					WConio.textcolor(4)
					print("TMain ["+time.strftime("%H:%M:%S")+"] !! Error while running. Will restart now!\n")
					WConio.textcolor(2)
					
					
###### Worker Thread ########################################
# The Worker Thread dequeses jobs and fullfills them						  #
###########################################################
		
class T_Work (threading.Thread):
	def __init__(self, threadID, name):
		super(T_Work,self).__init__()
		self._stop = threading.Event()
		self.threadID = threadID
		self.name = name
		global jobs
		
	def stop (self):
		self._stop.set()

	def stopped (self):
		return self._stop.isSet()
		
	def run(self):
		global transfered
		global root
		global wready
		if wready == 1:
			while 1:
				try:
					wready = 0
					os.chdir(root)
					jobcount = jobs.getLength()
					if jobcount >= 1:
						condata = jobs.dequeue()
						conns = condata[0]
						request = condata[1]
						addr = condata[2]
						request = str(request)
						request = request.split()
						filepath = request[1]
						url = request[1].split('/')
						urlparts = len(url)
						
						for i in range(1,urlparts):
							part = url[i]
							if part == '':
								file_name = 'index.html'
								filepath = filepath+"index.html"
								ta = 'text'
								tb = 'html'
								gottype = '1'
								break
							
							if os.path.exists(part):
								if os.path.isdir(part):
									os.chdir(part)
								else:
									if re.search('.html', part):
										file_name = part
										ta = 'text'
										tb = 'html'
										gottype = '1'
										break
									elif re.search('.xml', part):
										file_name = part
										ta = 'application'
										tb = 'xhtml+xml'
										gottype = '1'
										break
									elif re.search('.xhtml', part):
										file_name = part
										ta = 'application'
										tb = 'xhtml+xml'
										gottype = '1'
										break
									elif re.search('.dtd', part):
										file_name = part
										ta = 'application'
										tb = 'xml-dtd'
										gottype = '1'
										break
									elif re.search('.js', part):
										file_name = part
										ta = 'application'
										tb = 'x-javascript'
										gottype = '1'
										break
									elif re.search('.css', part):
										file_name = part
										ta = 'text'
										tb = 'css'
										gottype = '1'
										break
									elif re.search('.jpg', part):
										file_name = part
										ta = 'image'
										tb = 'jpg'
										gottype = '1'
										break
									elif re.search('.png', part):
										file_name = part
										ta = 'image'
										tb = 'png'
										gottype = '1'
										break
									elif re.search('.gif', part):
										file_name = part
										ta = 'image'
										tb = 'gif'
										gottype = '1'
										break
									elif re.search('.bmp', part):
										file_name = part
										ta = 'image'
										tb = 'bmp'
										gottype = '1'
										break
									elif re.search('.ico', part):
										file_name = part
										ta = 'image'
										tb = 'x-icon'
										gottype = '1'
										break
									elif re.search('.zip', part):
										file_name = part
										ta = 'application'
										tb = 'zip'
										gottype = '1'
										break	
									elif re.search('.rar', part):
										file_name = part
										ta = 'application'
										tb = 'rar'
										gottype = '1'
										break	
									elif re.search('.pdf', part):
										file_name = part
										ta = 'application'
										tb = 'pdf'
										gottype = '1'
										break
									elif re.search('.mp4', part):
										file_name = part
										ta = 'video'
										tb = 'mp4'
										gottype = '1'
										break	
									elif re.search('.mp3', part):
										file_name = part
										ta = 'audio'
										tb = 'mp3'
										gottype = '1'
										break
									elif re.search('.wav', part):
										file_name = part
										ta = 'audio'
										tb = 'vnd.wave'
										gottype = '1'
										break
									elif re.search('.wma', part):
										file_name = part
										ta = 'audio'
										tb = 'x-ms-wma'
										gottype = '1'
										break
									elif re.search('.mpg', part):
										file_name = part
										ta = 'video'
										tb = 'mpg'
										gottype = '1'
										break		
									elif re.search('.mpeg', part):
										file_name = part
										ta = 'video'
										tb = 'mpeg'
										gottype = '1'
										break
									elif re.search('.wmv', part):
										file_name = part
										ta = 'video'
										tb = 'x-ms-wm'
										gottype = '1'
										break
									else: 
										file_name = part
										ta = 'application'
										tb = 'octet-stream'
										gottype = '1'
										break
							else:																	
								os.chdir(root)
								WConio.textcolor(4)
								print("TWork ["+time.strftime("%H:%M:%S")+"] >> File or directory not found: "+filepath+"!\n")
								WConio.textcolor(2)
								gottype = '0'							
								if re.search('.', part):
									if re.search('.html', part) or re.search('.htm', part):
										file_name = "404.html"
										ta = "text"
										tb = "html"
										gottype = '1'
									elif re.search('.ico', part):
										file_name = '404.ico'
										ta = 'image'
										tb = 'x-icon'
										gottype = '1'
						
								
						if gottype == '1':
							print("TWork ["+time.strftime("%H:%M:%S")+"] >> Sending "+file_name+" to "+addr+"\n")
							file_stats = os.stat(file_name)
							fsize = file_stats [stat.ST_SIZE]
							last_modified = time.ctime(os.path.getmtime(file_name))
							sendtime = time.strftime("%a %b %d %H:%M:%S %Y")	
							accept = bytes('HTTP/1.1 200 OK\nDate: '+str(sendtime)+'\nServer: MiniServ/'+str(version)+'Last-Modified: '+str(last_modified)+'\nAccept-Ranges: bytes\nContent-length: '+str(fsize)+'\nConnection: keep-alive\nContent-type: '+str(ta)+'/'+str(tb)+'\n\n', 'iso-8859-1')
							conns.send(accept)
							datei = open(file_name,'rb')
							conns.sendall(datei.read())
							datei.close
						else:
							print("TWork ["+time.strftime("%H:%M:%S")+"] >> Sending ZeroBit to "+addr+"\n")
							fsize = 0
							last_modified = time.strftime("%a %b %d %H:%M:%S %Y")
							sendtime = time.strftime("%a %b %d %H:%M:%S %Y")	
							accept = bytes('HTTP/1.1 404 Not Found\n\n', 'iso-8859-1')
							conns.send(accept)
						conns.close()			
						WConio.textcolor(2)
						time.sleep(0.5)
						wready = 1
				except:
					WConio.textcolor(4)
					print("TWork ["+time.strftime("%H:%M:%S")+"] !! Error while running. Will restart now!\n")
					WConio.textcolor(2)								
		else:
			time.sleep(0.5)
		
				

###### Service Thread ########################################
# The Service Thread is responsible for OPT-Requests by the Terminal #
###########################################################

class T_Serv (threading.Thread):
	def __init__(self, threadID, name):
		super(T_Serv,self).__init__()
		self._stop = threading.Event()
		self.threadID = threadID
		self.name = name
		
	def stop (self):
		self._stop.set()

	def stopped (self):
		return self._stop.isSet()
		
	def run(self):
		# Setting Server ready for connections
		global ready
		ready = 1
		while 1:	
			ssock.listen(1)
			sconns, saddr = ssock.accept()
			sdata = sconns.recv(1024)
			if sdata == bytes(pwdHashStr, 'iso-8859-1'):
				sconns.send(bytes('OK', 'iso-8859-1'))
				cmd = sconns.recv(1024)
				
				if cmd == bytes('EXIT', 'iso-8859-1'):
					sconns.send(bytes('OK', 'iso-8859-1'))
					WConio.textcolor(4)
					print('Received TERMINATION Signal. Shutting down now!')
					TMain.stop()
					TWork.stop()
					TServ.stop()
				
				#elif cmd = bytes('OK', 'iso-8859-1')
				
			else:
				sconns.send(bytes('NOK', 'iso-8859-1'))
				sconns.close()
				
		
	
	def do(self, cmd):
		self.cmd = cmd
		print(cmd)
		
		
		
# Starting Threads

TMain = T_Main(1,"TMain")
TWork = T_Work(2,"TWork")
TServ = T_Serv(3,"TServ")

TWork.start()
print("TWork ["+time.strftime("%H:%M:%S")+"] Started!\n")
TServ.start()
print("TServ ["+time.strftime("%H:%M:%S")+"] Started!\n")
TMain.start()
print("TMain ["+time.strftime("%H:%M:%S")+"] Started!")

# Add threads to thread list
threads.append(TMain)
threads.append(TWork)
threads.append(TServ)

# Wait for all threads to complete
for t in threads:
    t.join()