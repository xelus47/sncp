class SNCP():
	def __init__(self):
		self.body=''
		self.request_version=''
		self.command=''
		self.parameter=''
		self.path=''
		self.error_code=100
		self.headers={}

	def parse(self,raw):
		error_code=100
		if len(raw.split('\n\n'))>1:
			head = raw.split('\n\n')[0]
			body = raw.split('\n\n')[1]
		else:
			head=raw
			body=''
		headlines=head.split('\n')
		status = headlines[0]
		headersRaw=[a for a in headlines[1:]]

		if not len(status.split(' '))==3: # :3
			error_code=400
		request_version=status.split(' ')[0]
		command=status.split(' ')[1]
		para = status.split(' ')[2]

		headers={}
		for rawHeader in headersRaw:
			if ":" in rawHeader:
				name=rawHeader.split(':')[0]
				info=rawHeader.split(':')[1]
				headers[name]=info

		self.body=body
		self.request_version=request_version
		self.command=command
		self.parameter=para
		self.path=para
		self.headers=headers
		self.error_code=error_code

		return (command,para)

	def test(self):
		print "Yes"



class Prototype():
	def __init__(self,nType):
		self.__socket__ = __import__('socket')
		self._json = __import__('json')
		self._sncp = SNCP()
		self.nType=nType
		import socket
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		#
		# Define a user agent for the lulz
		#
		import sys
		v=sys.version.split(' ')[0]
		if sys.platform=='win32':
			osinfo='win32 v%s.%s' % (sys.getwindowsversion().major,sys.getwindowsversion().minor)
		else:
			osinfo=sys.platform
		self.user_agent="Prototype/1.0 (Python "+v+") ("+osinfo+")"

	def shellBind(self,ip='127.0.0.1'):
		try:
			header={
				'user-agent':self.user_agent,
				'neuron-type':self.nType
			}

			self.sock.connect((ip,8000))
			self.sock.send('SNCP/1.0 do bind\n') # request a port to occupy
			for i in header:
				self.sock.send(i.capitalize()+':'+header[i].capitalize()+'\n')
			
			data = self.sock.recv(1024)
			print data
			self.sock.close()
		except:
			print "Could not connect to shell on port 127.0.0.1:8000"
			exit()