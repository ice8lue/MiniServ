import binascii

string = 'TEST'
print(string)
stringb = binascii.a2b_base64(bytes(string, 'iso-8859-1'))
print(stringb)
stringc = binascii.b2a_base64(stringb)
print(stringc)