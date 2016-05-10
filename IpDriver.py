import os
import sys
import socket

'''
	Syntax: IpDriver.py localIP, localPort, remoteIP, remotePort, protocol, timeout, request
	
	Parameters in:
		localIP: 	The IP-address to send from.
		localPort: 	The port to send from.
		remoteIP: 	The IP-address to send to.
		remotePort: The port to send to.
		protocol: 	UDP och TCP protocol.
		timeout: 	Read timeout.
		request: 	The data to send. Specified as one long byte-array with no spaces.
		
	Parameters out:
		response: 	The received data. Specified as one long byte-array with no spaces.
'''

# Send and receive data with UDP.
def UDP(local, remote, timout, request):
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	# Only bind to IP-address and port if specified.
	if local != None:
		udp.bind(local)
	
	udp.settimeout(timeout)
	udp.sendto(request, remot)
	response, endpoint = udp.recvfrom(1024)
	udp.close()
	return respone
	
# Send and receive data with TCP.
def TCP(local, remote, timeout, request):
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Only bind to IP-address and port if specified.
	if local != None:
		tcp.bind(local)
		
	tcp.settimeout(timeout)
	tcp.connect(remote)
	tcp.send(request, remot)
	response = tcp.recv(1024)
	tcp.close()
	return respone
	
	
def CheckIP(ip):
	pass
	
local = ()		# Local IP and port as tuple.
remote = ()		# Remote IP and port as tuple.
protocol = ""
timeout = 0
request = []

# ============
# === Main ===
# ============

# Use UDP to send and receive data.
if protocol == "UDP":
	response = UDP(local, remote, timeout, request)
	print(response)

# Use TCP to send and receive data.
elif protocol = "TCP":
	response = TCP(local, remote, timeout, request)
	print(response)
	
# Unknown protocol.
else:
	pass