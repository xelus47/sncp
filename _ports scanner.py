import socket

import colorama
from colorama import Fore, Back, Style
colorama.init()

MINY, MAXY = 1, 24
MINX, MAXX = 1, 80

pos = lambda y, x: '\x1b[%d;%dH' % (y, x)



ip=raw_input('IP: ')
if ip == '': ip='127.0.0.1'


for port in xrange(8070,8090):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((ip,port))
		s.send('Hi')
		data = s.recv(1024)
		s.close()
		print("Connected "+ip+":%s" % port)
	except socket.error:
		print "%s\x1b[1A" % port
