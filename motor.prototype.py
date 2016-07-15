try:
	from _prototype import Prototype
except:
	print "Error: failed to import _prototype.py. Node will exit."
	exit()


proto = Prototype('motor')
proto.shellBind() # connect to shell

