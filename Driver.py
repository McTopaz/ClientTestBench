import os
import sys
import socket
import serial
import xml.etree.ElementTree as ET

'''
	Syntax: Driver.py <configurationFile> <request>
	
	Parameters in:
		configurationFile:	The configuration file to setup the driver after.
		request: 			The data to send. Specified as one long byte-array with no spaces.
		
	Parameters out:
		response: 	The received data. Specified as one long byte-array with no spaces.
'''

# =============================================================================
# === Classes =================================================================
# =============================================================================

# Holds data for UDP or TCP communication.
class NetworkSettings:
	
	def __init__(self, local, remote, protocol):
		self.local = local			# Tuple containing IP-address and port for the local end point.
		self.remote = remote		# Tuple containing IP-address and port for the remote end point.
		self.protocol = protocol	# Either UDP or TCP protocols.

# Holds data for serial communication.		
class SerialSettings:
	
	def __init__(self, port, baudRate, dataBits, parity, stopBits):
		self.port = port
		self.baudRate = baudRate
		self.dataBits = dataBits
		self.parity = parity
		self.stopBits = stopBits
			

# The base class of all drivers.			
class Driver:
	# Init the driver.
	def __init__(self, configurationFile):
		# Init the configuration file and parse its XML-content.
		self.configurationFile = configurationFile	# Save the configuration file.
		self.xmlFile = ET.parse(sys.argv[1])		# Parse the configuration file to an XML-file.
		self.root = self.xmlFile.getroot()			# Get the root XML-file in the XML-file.
		
		# Read the configuration file.
		self.timeout = int(self.root[2][1].text)		# Get the driver's timeout.

	# Read the driver's settings.
	def ReadSettings(self):
		# Note: Override in a derived class.
		pass
		
	# Open the driver.
	def Open(self):
		# Note: Override in a derived class.
		pass
		
	# Close the driver.
	def Close(self):
		# Note: Override in a derived class.
		pass
		
	# Send a request with the driver.
	def Send(self, request):
		# Note: Override in a derived class.
		pass
		
	# Receive a response with the driver.
	def Receive(self):
		# Note: Override in a derived class.
		pass

# The base class of all network drivers.
class NetworkDriver(Driver):
	# Init the network driver.
	def __init__(self, configurationFile):
		Driver.__init__(self, configurationFile)
		self.settings = self.ReadSettings()

	# Read the network settings from the configuration file.
	def ReadSettings(self):
		# Get IP-address and port for the local endpoint.
		localIP = self.root[2][2][0].attrib["IP"]
		localPort = int(self.root[2][2][0].attrib["Port"])
		local = (localIP, localPort)
		
		# Get IP-address and port for the remote endpoint.
		remoteIP = self.root[2][2][1].attrib["IP"]
		remotePort = int(self.root[2][2][1].attrib["Port"])
		remote = (remoteIP, remotePort)
		
		# Get the protocol
		protocol = self.root[2][2][2].text
		
		return NetworkSettings(local, remote, protocol)

# Represent a UDP-driver.		
class UdpDriver(NetworkDriver):
	# Init the UDP-driver.
	def __init__(self, configurationFile):
		NetworkDriver.__init__(self, configurationFile)
		
		# Setup the UDP-socket.
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp.settimeout(self.timeout / 1000)	# Convert to float.
		
	def Open(self):
		# Bind to local end point.
		if not self.settings.local:
			self.udp.bind(self.settings.local[0], self.settings.local[1])
	
	def Close(self):
		self.udp.close()
	
	def Send(self, request):
		self.udp.sendto(request, (self.settings.remote[0], self.settings.remote[1]))
		
	def Receive(self):
		response, endpoint = self.udp.recvfrom(1024)
		return response
		
# Represent a TCP-driver.		
class TcpDriver(NetworkDriver):
	
	# Init the TCP-driver.
	def __init__(self, configurationFile):
		NetworkDriver.__init__(self, configurationFile)
		
		# Setup the TCP-socket.
		self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcp.settimeout(self.timeout / 1000)	# Convert to float.
		
	def Open(self):
		# Bind to local end point.
		if not self.settings.local:
			self.tcp.bind(self.settings.local[0], self.settings.local[1])
	
		# Connect to the remote endpoint.
		self.tcp.connect(request, (self.settings.remote[0], self.settings.remote[1]))
	
	def Close(self):
		self.tcp.close()
	
	def Send(self, request):
		self.tcp.send(request)
		
	def Receive(self):
		response = self.tcp.recv(1024)
		return response
	
# The base class of all serial drivers.		
class SerialDriver(Driver):
	# Init the serial driver.
	def __init__(self, configurationFile):
		Driver.__init__(self, configurationFile)
		self.settings = self.ReadSettings()

	# Read the serial settings from the configuration file.
	def ReadSettings(self):
		
		# Read the serial settings from the configuration file.
		port = self.root[2][3][0].text
		baudRate = int(self.root[2][3][1].text)
		dataBits = int(self.root[2][3][2].text)
		parity = self.root[2][3][3].text
		stopBits = self.root[2][3][4].text
		
		return SerialSettings(port, baudRate, dataBits, parity, stopBits)

# Represent a serial-driver.			
class SerialPort(SerialDriver):
	# Init the serial port.
	def __init__(self, configurationFile):
		SerialDriver.__init__(self, configurationFile)
		
		# Setup the serial port.
		self.ser = serial.Serial()
		self.ser.port = self.settings.port
		self.ser.baudrate = self.settings.baudRate
		self.ser.bytesize = self.settings.dataBits
		self.ser.parity = self.settings.parity
		self.ser.stopBits = self.settings.stopBits
		self.ser.timeout = (self.timeout / 1000)	# Convert to float.
	
	def Open(self):
		self.ser.open()
		
	def Close(self):
		self.ser.close()
		
	def Send(self, request):
		self.ser.write(request)
		
	def Receive(self):
		response = self.ser.read(1024)
		return response
	
def PrintData(data):
	tstr = ""
	for j in range(len(data)):
		if j%16 == 0 and j != 0:
			tstr = tstr + '\n'
		tstr = tstr + "%02X "%data[j]
	print(tstr)	
	
# =============================================================================
# === Main ====================================================================
# =============================================================================

if len(sys.argv) < 3:
	file = "%s%s"%(os.path.splitext(os.path.basename(sys.argv[0]))[0], os.path.splitext(os.path.basename(sys.argv[0]))[1])
	print("Error: Too few arguments. ", end="")
	print("%s <configuration file path> <request>"%(file))
	sys.exit()

# Make sure the configuration XML-file exist.
if os.path.isfile(sys.argv[1]) == False:
	print("Error: Configuration file don't exist.")
	sys.exit()

if sys.argv[2] == None or sys.argv[2] == "":
	print("Error: No request specified.")
	sys.exit()
	
configurationFile = sys.argv[1]			# Gets the configuration file.
request = sys.argv[2]					# Gets the request and convert to a byte array.
xmlFile = ET.parse(configurationFile)	# Parse the configuration's XML content.
root = xmlFile.getroot()				# Gets root element in XML-file.
type = root[2].attrib["Type"]			# Gets type in XML-file.

driver = None	# Represent the driver to send the request and receive the response.

# Get what driver to use.
if type == "Network":
	protocol = root[2][2][2].text
	
	if protocol == "UDP":
		driver = UdpDriver(configurationFile)	# UDP driver.
	elif protocol == "TCP":
		driver = TcpDriver(configurationFile)	# TCP driver.
	else:
		print("Error: Unknown protocol.")
		sys.exit()
	
elif type == "Serial":
	driver = SerialPort(configurationFile)		# Serial driver.
else:
	print("Error: Unknown type.")
	sys.exit()

request = bytearray.fromhex(request)	# Convert to a byte array.
	
# Run the driver.
driver.Open()					# Open connection.
driver.Send(request)			# Send the request.
response = driver.Receive()		# Receive the response.
driver.Close()					# Close connection.

if len(request) == 0:
	print("Error: No data received.")
else:
	#PrintData(response)
	responseLine = "".join("%02X"%(i) for i in response)
	print(responseLine)