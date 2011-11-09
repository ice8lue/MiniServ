#####################################
#		MiniServ - First-Run-Setup				   #
#		by Frank Adler, 2010						   #
#####################################

import WConio
import sys
import win32crypt
import binascii

WConio.settitle('MiniServ :: First-Use-Configuration')
WConio.textmode()
WConio.textcolor(2)

ini = open('settings.ini','r')
inidat = ini.readlines()
ini.close()
version = inidat[0].split()
version = version[0]

print("\n\nPlease enter some letters and numbers and press ENTER: ", end=" ")
text = WConio.cgets(512)

print("\n\nPlease give me some more letters and numbers and press ENTER: ", end=" ")
textb = WConio.cgets(512)

string = text + textb
pwdHash = win32crypt.CryptProtectData(string.encode(),'psw',None,None,None,0)
pwdHashStr = str(binascii.hexlify(pwdHash)).upper()
print('\n\nSecurity Login Hash: ' + pwdHashStr)

print("\n\nWriting settings.ini ...")

g = open('settings.ini', "w")
linez = str(version)+"\n"
linea = pwdHashStr
g.write(linez)
g.write(linea)
g.close()

print("\n\nDone! Press ENTER or close this window...")
done = WConio.cgets(1)



