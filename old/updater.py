import urllib
import WConio
from shutil import copy2, rmtree
from sys import exit
import os

WConio.settitle('MiniServ :: Update Tool')
WConio.textmode()
WConio.textcolor(7)


def download(url):
	
	webFile = urllib.urlopen(url)
	filename = url.split('/')[-1]
	localFile = open(filename, 'w')
	print '\n  Downloading File:',filename,'...',
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()
	WConio.textcolor(2)
	print 'done'
	WConio.textcolor(7)

def goto_dir(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)
	os.chdir(dir)

ini = open('settings.ini','r')
ini = ini.readlines()
version = ini[0].split('=')
version = version[1]

onver = urllib.urlopen('http://www.frankadler.de/miniserv/files/version.txt').read()
versio = version.split()
versio = versio[0]
WConio.textcolor(7)
print '\n\n  Version online:',onver
print '  Version running:',versio
od = onver.split('.')
vc = versio.split('.')
od[3] = od[3].split('\n')[0]
onver = od[0]+od[1]+od[2]+od[3]
versio = vc[0]+vc[1]+vc[2]+vc[3]

if versio == onver:
	WConio.textcolor(2)
	print '\n  Your Version is up to date'
	WConio.textcolor(7)
	exit()
else:
	if onver > versio:
		WConio.textcolor(4)
		print '\n  You should update!'
		WConio.textcolor(7)
		print '\n  This Updater can do all that for you, ok? [y/n]: ',
		text = WConio.cgets(1)
		if text == 'n':
			exit()
		elif text == 'y':
			print '\n\n  Creating temp directory...',
			goto_dir('temp')
		
			WConio.textcolor(2)
			print 'done'
			WConio.textcolor(7)
			cons = 'http://www.frankadler.de/miniserv/files/latest/cons.exe'
			download(cons)
			serv = 'http://www.frankadler.de/miniserv/files/latest/serv.exe'
			download(serv)
			updater = 'http://www.frankadler.de/miniserv/files/latest/updater.exe'
			download(updater)
			settings = 'http://www.frankadler.de/miniserv/files/latest/settings.ini'
			download(settings)
			
			print '\n  Killing running processes of Server / Console...',
			serv = 0
			cons = 0
			if ''.join(os.popen('query process').readlines()).find('serv.exe') >= 0:
				os.system('taskkill /IM serv.exe > NUL')
				serv = 1
			if ''.join(os.popen('query process').readlines()).find('cons.exe') >= 0:
				os.system('taskkill /IM cons.exe > NUL')
				cons = 1
			WConio.textcolor(2)
			print 'done'
			WConio.textcolor(7)

			print '\n  Overwriting old files...',
			copy2("serv.exe", "../")
			copy2("cons.exe", "../")
			copy2("updater.exe", "../")
			copy2("settings.ini", "../")
			WConio.textcolor(2)
			print 'done'
			WConio.textcolor(7)
			
			os.chdir('..')
			
			print '\n  Removing temp files...',
			rmtree('temp')
			WConio.textcolor(2)
			print 'done'
			
			print '\n  Update done!\n  Closing Update Tool now'
			WConio.textcolor(7)
			exit()
	else:
		WConio.textcolor(9)
		print "\n  There's something strange going on..."
		WConio.textcolor(7)
		exit()