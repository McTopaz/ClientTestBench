import os
import re
import sys
import xml.etree.ElementTree as ET

# Specify a file path.
def InputFilePath(header, default):
	while True:
		print("%s [%s]: "%(header, default), end="")
		inp = input()
		
		# Use default file.
		if inp == "":
			return default
		# Use specified file.
		elif os.path.isfile(inp):
			return os.path.realpath(inp)
		# Invalid file path given. Try again.
		else:
			pass

# Specify some choices.
def SpecifyChoices(header, default):
	while True:
		print("%s [%s]: "%(header, default), end="")
		inp = input()
		
		# Use default args.
		if inp == "":
			return default
		
		if inp == "none":
			return ""
		
		# Check the given args.
		parts = inp.split(' ')
		args = []
		for part in parts:
			# Only use arguments which is a digit.
			if part.isdigit() and not part in args:
				args.append(part)
		
		# Check what arguments to use.
		if len(args) > 0:
			args.sort()
			arguments = "".join("\"%s\","%(arg) for arg in args)	# Put " around every argument: "<arg>".
			arguments = arguments[:-1] # Cut last comma and space.
			return arguments
			
# Specify a choice from a list of choices.
def SelectChoice(header, default, choices):
	line = "".join("%s, "%(choice) for choice in choices)	# Create a line with all choices.
	line = line[:len(line)-2]								# Remove last ', ' from the line.
	line = "%s of [%s], [%s]"%(header, line, default)		# Include the header and the defualt value in the line.
	
	while True:
		print("%s: "%(line), end="")
		inp = input()
	
		# Use default choice.
		if inp == "":
			return default
		# Verify if any of the choices where given.
		elif inp != "":
			for choice in choices:
				if inp == choice:
					return inp	# One if the choices where selected.
		# None of the choices where selected. Try again.
		else:
			pass
			
# Specify a value.			
def InputValue(header, default, min, max):
	while True:
		print("%s [min=%s, max=%s] [%s]: "%(header, min, max, default), end="")
		inp = input()
		
		# Use default value.
		if inp == "":
			return default
			
		# Use the value which was specified.
		elif inp.isdigit() and (int(inp) >= min) and (int(inp) <= max):
			return inp
		# Invalid value specified. Try again.
		else:
			pass
			
# Specify an IP-address.			
def InputIPaddress(header, default):
	while True:
		print("%s [%s]: "%(header, default), end="")
		inp = input()
		
		# Use default IP.
		if inp == "":
			return default
		# Use specified IP.
		elif re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', inp):
			return inp
		# Invalid IP given. Try again.
		else:
			pass

# Specify a name.
def InputName(header, default):
	while True:
		print("%s [%s]: "%(header, default), end="")
		inp = input()
		
		# Use default name.
		if inp == "":
			return default
		# Use specified name.
		else:
			return inp

# Specify a name of the configuration file.
def ConfigurationFileName():
	while True:
		print("Enter name of configuration: ", end="")
		inp = input()
			
		if inp == "":
			continue
		else:
			return inp
	
# Alter a existing XML-file with user specific settings.
def AlterConfiguration(xmlFile, saveFilePath):
	print("")
	print("\t=== Press CTRL + C to exit at any time ===")
	print("")
	
	root = xmlFile.getroot()
	
	temp = ""	# A default variable to store stuff in.
	
	# ======================
	# === Source section ===
	# ======================
	
	temp = InputFilePath("Specify source file", root[0][0].text)
	root[0][0].text = temp
	
	# ==============================
	# === Request parser section ===
	# ==============================
	
	temp = InputFilePath("Specify request file", root[1][0].text)	# Request's file.
	root[1][0].text = temp
	temp = SpecifyChoices("Select request's args", root[1][1].text)			# Request's arguments.
	root[1][1].text = temp
	
	# ======================
	# === Driver section ===
	# ======================
	temp = InputFilePath("Specify driver's file", root[2][0].text)	# Driver's file path.
	root[2][0].text = temp
	
	temp = SpecifyChoices("Select driver's args", root[2][1].text)	# Driver's arguments.
	root[2][1].text = temp
	
	temp = InputValue("Specify driver's timeout", root[2][2].text, 0, 0xFFFFFFFFFFFFFFFF)	# Driver's timeout.
	root[2][2].text = temp
	
	temp = SelectChoice("Select type", root[2].attrib["Type"], ["Network", "Serial"])	# Driver's type selection.
	root[2].attrib["Type"] = temp;
	 
	# ================================= 
	# === Driver's network section ====
	# =================================
	if root[2].attrib["Type"] == "Network":
	
		# Local end point's IP-address.
		temp = InputIPaddress("Specify local end point's IP-address", root[2][3][0].attrib["IP"])
		root[2][3][0].attrib["IP"] = temp
		
		# Local end point's port number.
		temp = InputValue("Specify local end point's IP-port", root[2][3][0].attrib["Port"], 0x00, 0xFFFF)
		root[2][3][0].attrib["Port"] = temp
		
		# Remote end point's IP-address.
		temp = InputIPaddress("Specify remote end point's IP-address", root[2][3][1].attrib["IP"])
		root[2][3][1].attrib["IP"] = temp
		
		# Remote end point's port number.
		temp = InputValue("Specify remote end point's IP-port", root[2][3][1].attrib["Port"], 0x00, 0xFFFF)
		root[2][3][1].attrib["Port"] = temp
		
		# Network protocol.
		temp = SelectChoice("Select protocol", root[2][3][2].text, ["UDP", "TCP"])
		root[2][3][2].text = temp
		
	# ===============================
	# === Driver's serial section ===
	# ===============================
	elif root[2].attrib["Type"] == "Serial":
	
		# Port name
		temp = InputName("Specify port name", root[2][4][0].text)
		root[2][4][0].text = temp
		
		# Baudrate
		temp = InputValue("Enter baud rate", root[2][4][1].text, 0x01, 0xFFFFFFFF)
		root[2][4][1].text = temp
		
		# Data bits
		temp = SelectChoice("Specify data bits", root[2][4][2].text, ["5", "6", "7", "8"])
		root[2][4][2].text = temp
		
		# Parity
		temp = SelectChoice("Specify parity", root[2][4][3].text, ["E", "M", "N", "O", "S"])
		root[2][4][3].text = temp
		
		# Stop bits
		temp = SelectChoice("Specify stop bits", root[2][4][4].text, ["0", "1", "1,5", "2"])
		root[2][4][4].text = temp
		
	# This state should never happen.
	else:
		pass
	
	# ===============================
	# === Response parser section ===
	# ===============================
	temp = InputFilePath("Specify response file:", root[3][0].text)	# Response's file.
	root[3][0].text = temp
	temp = SpecifyChoices("Select response's args", root[3][1].text)			# Response's arguments.
	root[3][1].text = temp
	
	# ======================
	# === Result section ===
	# ======================
	temp = InputFilePath("Specify result file:", root[4][0].text)
	root[4][0].text = temp
	
	print("")
	
	# === Save configuration to file ===
	
	if saveFilePath == "":
		name = ConfigurationFileName()								# Get a name of the configuration file.
		directory = os.path.dirname(sys.argv[0])					# Get the folder of the script.
		saveFilePath = "%s%s%s.xml"%(directory, os.path.sep, name)	# Concat the save file path.
	else:
		# The save file path is already given due to the configuration was only modified.
		pass
	
	xmlFile.write(saveFilePath)

# Create a new XML-file with default settings.
def CreateDefaultConfiguration():
	root = ET.Element("ClientTestBench")
	
	# =============
	# == Source ===
	# =============
	source = ET.SubElement(root, "Source")		# Source's node.
	sourceFile = ET.SubElement(source, "File")	# Source's file.
	
	# ===============
	# === Request ===
	# ===============
	request = ET.SubElement(root, "RequestParser")	# Request parser node.
	requestFile = ET.SubElement(request, "File")	# Request's file.
	args = ET.SubElement(request, "Args")			# Request's arguments from [source-file].
	
	# ==============
	# === Driver ===
	# ==============
	driver = ET.SubElement(root, "Driver", Type="")	# Driver's node.
	driverFile = ET.SubElement(driver, "File")		# Driver's file path.
	args = ET.SubElement(driver, "Args")				# Driver's arguments from [source-file].
	timeout = ET.SubElement(driver, "Timeout")
	
	# Driver's network.
	network = ET.SubElement(driver, "Network")							# Driver's network node.
	local = ET.SubElement(network, "LocalEndPoint", IP="", Port="")
	remote = ET.SubElement(network, "RemoteEndPoint", IP="", Port="")
	protocol = ET.SubElement(network, "Protocol")
	
	# Driver's serial.
	serial = ET.SubElement(driver, "Serial")		# Driver's serial node.
	port = ET.SubElement(serial, "Port")
	baudRate = ET.SubElement(serial, "Baudrate")
	dataBits = ET.SubElement(serial, "DataBits")
	parity = ET.SubElement(serial, "Parity")
	stopBits = ET.SubElement(serial, "StopBits")
	
	# ================
	# === Response ===
	# ================
	response = ET.SubElement(root, "ResponseParser")	# Response's parser node.
	requestFile = ET.SubElement(response, "File")		# Response's file.
	args = ET.SubElement(response, "Args")				# Response's arguments from [source-file].
	
	# ====================
	# === Result node ====
	# ====================
	result = ET.SubElement(root, "Result")
	resultFile = ET.SubElement(result, "File")
	
	# Create the XML-file.
	xmlFile = ET.ElementTree(root)
	return xmlFile

# ============
# === Main ===
# ============
		
# Existing configuration file is specified.
if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
	xmlFile = ET.parse(sys.argv[1])				# Open the XML-file.
	AlterConfiguration(xmlFile, sys.argv[1])	# Alter the content of the XML-file.

# No configuration is specified, create a new.
else:
	xmlFile = CreateDefaultConfiguration()		# Create a default XML-file.
	AlterConfiguration(xmlFile, "")				# Alter the default XML-file.
	
