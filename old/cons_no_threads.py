import WConio
import socket
import re
import urllib
import os
import sys
import time

HOST = 0
PORT = 0

### Functions ###

def login ():
	global HOST
	global PORT
	global auth
	WConio.textcolor(7)
	print('\n\n  Please enter server data: \n\n    IP: ', end=" ")
	HOST = WConio.cgets(30)
	print('\n    Port: ', end=" ")
	PORT = WConio.cgets(30)
	print('\n\n  Setting up connection...')
	try:
		HOST = HOST.split()
		PORT = PORT.split()
		HOST = HOST[0]
		PORT = int(PORT[0])
		
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		s.send('OPT')
		req = s.recv(1024)
		if req == 'AUTH':
			print('\n  Please enter user data: \n\n    User: ', end=" ")
			user = WConio.cgets(30)
			print('\n    Password: ', end=" ")
			passw = WConio.cgets(30)
			print('\n\n  Sending login data...')
			s.send(user)
			s.send(passw)
			req = s.recv(1024)
			if req == 'DENY':
				WConio.textcolor(4)
				print('\n  Error! Server rejected login. Wrong Password?\n  Please try again later!')
				auth = 0
			else:
				auth = 1
				print('\n  Successfully logged in!')
		else:
				auth = 1
				print('\n  Already logged in')
	except:
		WConio.textcolor(4)
		print('\n  Connection Error!')

ini = open('settings.ini','r')
ini = ini.readlines()
# version = ini[0].split('=')
# version = version[1]
version = ini[0]

WConio.settitle('MiniServ :: Service Console')
WConio.textmode()

WConio.textcolor(9)

print('>>>>> MiniServ :: Service Console %s\n'%version)

WConio.textcolor(15)

print('Enter "help" for a list of commands \n') 

commands = 'help','check update','connect','say hello','get server time','get server info','set logging min','set logging max','close server','close console','close all','disconnect'

auth = 0

while 1:
	WConio.textcolor(2)
	print('\n> ', end=" ")
	text = WConio.cgets(30)
	
	### text now contains a command ###
	
	if not text in commands:
		WConio.textcolor(7)
		print('\n\n  Unknown Command!')
		continue
	
	elif text == 'help':
		WConio.textcolor(7)
		print('\n\n  Possible Commands:')
		print('    help			-- shows this page')
		print('    connect to [IP] [PORT]	-- connects to selected IP to login')
		print('    say hello			-- sends Greetings to the Server')
		print('    get server time		-- fetches current server time')
		print('    get server info		-- fetches short server information')
		print('    set logging min		-- sets logging to minimal')
		print('    set logging max		-- sets logging to maximal')
		print('    check update		-- checks MiniServ Website for updates')
		print('    close server		-- shuts down the server app')
		print('    close console		-- shuts down the service console')
		print('    close all			-- shuts down server and service console')
		continue
	
	elif text == 'check update':
		print('\n\n  Running Update Tool...')
		os.popen('updater.exe')
		print('\n\n  Please restart Server/Console now!')
		time.sleep(5)
		sys.exit()

	elif text == 'connect':
		login()
			
	elif text == 'close console':
		if auth == 1:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((HOST,PORT))
			s.send('OPT')
			req = s.recv(1024)
			if req == 'OK':
				s.send('DISC')
				s.close()
		WConio.textcolor(7)
		print('\n\n  Bye!')
		break	
	
	elif text == 'close all':
		if auth == 1:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((HOST,PORT))
			s.send('OPT')
			req = s.recv(1024)
			if req == 'OK':
				s.send('EXIT')
				s.close()
		WConio.textcolor(7)
		print('\n\n  Bye!')
		break
	
	else:
		if auth == 0:
			login()
			if auth == 0:
				continue
				
		WConio.textcolor(7)
		
		if text == 'close server':
			try:
				print('\n\n  Sending termination singnal...')
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((HOST,PORT))
				s.send('OPT')
				req = s.recv(1024)
				if req == 'OK':
					s.send('EXIT')
					s.close
					auth = 0
					print('\n  Server shutdown completed!')
				s.close
			except:
				WConio.textcolor(4)
				print('\n\n  Can not connect to server. Please use "connect" first!')
				continue
				
		elif text == 'say hello':
			try:
				print('\n\n  Sending hello message!')
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((HOST,PORT))
				s.send('OPT')
				req = s.recv(1024)
				if req == 'OK':
					s.send('HELO')
				s.close
			except:
				WConio.textcolor(4)
				print('\n\n  Can not connect to server. Please use "connect" first!')
				continue			

		elif text == 'set logging min':
			try:
				print('\n\n  Setting loging to minimal')
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((HOST,PORT))
				s.send('OPT')
				req = s.recv(1024)
				if req == 'OK':
					s.send('LMIN')
				s.close
			except:
				WConio.textcolor(4)
				print('\n\n  Can not connect to server. Please use "connect" first!')
				continue			
		
		elif text == 'set logging max':
			try:
				print('\n\n  Setting loging to maximal')
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((HOST,PORT))
				s.send('OPT')
				req = s.recv(1024)
				if req == 'OK':
					s.send('LMAX')
				s.close
			except:
				WConio.textcolor(4)
				print('\n\n  Can not connect to server. Please use "connect" first!')
				continue			
		
		elif text == 'get server time':
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((HOST,PORT))
				s.send('OPT')
				req = s.recv(1024)
				if req == 'OK':
					s.send('TIME')
					ltime = s.recv(1024)
					print('\n\n ',ltime)
				s.close
			except:
				WConio.textcolor(4)
				print('\n\n  Can not connect to server. Please use "connect" first!')
				continue			
				
		elif text == 'get server info':
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((HOST,PORT))
				s.send('OPT')
				req = s.recv(1024)
				if req == 'OK':
					s.send('INFO')
					info = s.recv(1024)
					print('\n\n ',info)
				s.close
			except:
				WConio.textcolor(4)
				print('\n\n  Can not connect to server. Please use "connect" first!')
				continue
				
		elif text == 'disconnect':
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((HOST,PORT))
				s.send('OPT')
				req = s.recv(1024)
				if req == 'OK':
					s.send('DISC')
					print('\n\n  Disconnected successfully')
					auth = 0
				s.close
			except:
				WConio.textcolor(4)
				print('\n\n  Can not connect to server. Please use "connect" first!')
				continue
		