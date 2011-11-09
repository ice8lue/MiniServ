#####################################
#		MiniServ Terminal							   #
#		by Frank Adler, 2010						   #
#####################################

import WConio
import socket
import re
import os
import sys
import time

# Load Settings.ini

ini = open('settings.ini','r')
inidat = ini.readlines()
ini.close()
version = inidat[0]
pwdHashStr = inidat[1]

WConio.settitle('MiniServ :: Service Terminal')
WConio.textmode()
WConio.textcolor(9)
print('MiniServ :: Service Terminal %s\n'%version)
WConio.textcolor(15)
print('Enter "help" for a list of commands \n') 

# Setup Server Connection

WConio.textcolor(2)
print('\nPlease enter Server IP: ', end=" ")
IP = WConio.cgets(20)
 
try:
	SPORT = 10104
	ssock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ssock.connect((IP,SPORT))
	print('\n\nService Socket connected to '+str(IP)+' on Port '+str(SPORT)+'\n')
except:
	WConio.textcolor(4)
	print('\n\nERROR! Can not connect to '+IP)
	exit()

def auth():
	global pwdHashStr
	ssock.send(bytes(pwdHashStr, 'iso-8859-1'))
	answ = ssock.recv(1024)
	if answ == bytes('OK', 'iso-8859-1'):
		return 'true'
	elif answ == bytes('NOK', 'iso-8859-1'):
		return 'false'
		
commands = 'help','check update','get server time','get server info','set logging min','set logging max','close server','close console','close all','disconnect'

while 1:
	WConio.textcolor(2)
	print('\n> ', end=" ")
	text = WConio.cgets(30)
	
	if not text in commands:
		WConio.textcolor(4)
		print('\n\n  Unknown Command!')
		WConio.textcolor(2)
		continue
		
	elif text == 'help':
		WConio.textcolor(7)
		print('\n\n  Possible Commands:')
		print('    help			-- shows this page')
		print('    connect to [IP] [PORT]	-- connects to selected IP to login')
		print('    get server time		-- fetches current server time')
		print('    get server info		-- fetches short server information')
		print('    set logging min		-- sets logging to minimal')
		print('    set logging max		-- sets logging to maximal')
		print('    check update		-- checks MiniServ Website for updates')
		print('    close server		-- shuts down the server app')
		print('    close console		-- shuts down the service console')
		print('    close all			-- shuts down server and service console')
		continue
		
	elif text == 'close console':
		WConio.textcolor(7)
		print('\n\n  Bye!')
		exit()
		
	elif text == 'close server':
		if auth():
			WConio.textcolor(7)
			ssock.send(bytes('EXIT', 'iso-8859-1'))
			answ = ssock.recv(1024)
			if answ == bytes('OK', 'iso-8859-1'):
				print('  Server shutting down!')
				continue
			print('  Server shutdown not possible!')
		else:
			WConio.textcolor(4)
			print('  Authentification Error!')
			WConio.textcolor(2)
			
	elif text == 'close all':
		if auth():
			WConio.textcolor(7)
			ssock.send(bytes('EXIT', 'iso-8859-1'))
			answ = ssock.recv(1024)
			if answ == bytes('OK', 'iso-8859-1'):
				print('  Server shutting down!')
				print('\n\n  Bye!')
				exit()
			print('  Server shutdown not possible!')
			print('\n\n  Bye!')
			exit()
		else:
			WConio.textcolor(4)
			print('  Authentification Error!')
			WConio.textcolor(2)
	
	
	
	