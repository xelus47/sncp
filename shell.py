import socket,os,argparse
from _prototype import SNCP

killhelp='close/stop/quit/terminate/destroy/kill/shutdown'
parser = argparse.ArgumentParser(description='InstaPwn/Bash an instagram user')
parser.add_argument('--status',help='get status on active shell',action='count')
parser.add_argument('--restart',help='restart active shell',action='count')

parser.add_argument('--close',help=killhelp,action='count')
parser.add_argument('--stop',help=killhelp,action='count')
parser.add_argument('--quit',help=killhelp,action='count')
parser.add_argument('--terminate',help=killhelp,action='count')
parser.add_argument('--destroy',help=killhelp,action='count')
parser.add_argument('--kill',help=killhelp,action='count')
parser.add_argument('--shutdown',help=killhelp,action='count')
args = parser.parse_args()

killbool=bool(args.close) or bool(args.stop) or bool(args.quit) or bool(args.terminate) or bool(args.destroy) or bool(args.kill) or bool(args.shutdown) 

if killbool:
	if os.path.isfile('shell'):
		os.remove('shell')
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect(('127.0.0.1',8000))
		print "Sending shutdown"
		#s.send("hi bye")
		s.send('SNCP/1.0 hi bye\nUser-agent:Shell\n')
		data = s.recv(1024)
		print data
		s.close()
	except:
		print "Failed to connect to shell. Is it already closed?"
	exit()
elif bool(args.status): #
						# status
						#
	if os.path.isfile('shell'):
		print "Local shell file present"
	else:
		print "No local shell file, still checking localhost"
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect(('127.0.0.1',8000))
		print "Active shell found in localhost"
		print "Status:"
		s.send('SNCP/1.0 get status\nUser-agent:Shell\n')
		data = s.recv(1024)
		print data
		s.close()
	except:
		print "No active shell found in localhost"
	exit()
elif bool(args.restart):
	print "Feature not supported :P"
	exit()



else:
	mySNCP=SNCP()

	address=('127.0.0.1',8000)
	buffer_size = 1024

	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(address)

	f=open('shell','w')
	f.close()

	print "Is there a ghost in my shell?\n"

	while os.path.isfile('shell'):
		s.listen(1)

		conn, addr = s.accept()

		print 'Connection address:', addr
		while 1:
			data = conn.recv(buffer_size)
			if not data: break
			mySNCP.parse(data)
			if mySNCP.error_code!=400:
				#print "%s:%s" % (mySNCP.command,mySNCP.path)
				if mySNCP.command.lower()=="get":
					if mySNCP.path.lower()=="ping":
						conn.send('SNCP/1.0 200 OK\n\nPong')
					elif mySNCP.path.lower()=="status":
						conn.send("SNCP/1.0 200 OK\n\nShell address: %s:%s\n" % address)
						conn.send("Currently handling %s neural nodes\n" % 0)
				else:
					conn.send("SNCP/1.0 ")
			else:
				print "could not parse data:", data
				conn.send("SNCP/1.0 400 Bad_Request")
			print ""
		conn.close()