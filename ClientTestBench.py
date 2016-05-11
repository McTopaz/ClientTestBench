import os
import sys
import subprocess
import xml.etree.ElementTree as ET

if len(sys.argv) != 2 or os.path.isfile(sys.argv[1]) == False:
	print("Error: No configuration file specified.")
	sys.exit()
	
configurationFile = sys.argv[1]			# Gets the configuration file.
xmlFile = ET.parse(configurationFile)	# Parse the XML-structure in the configurationFile.
root = xmlFile.getroot()				# Get the root folder in the XML-structure.

# Get all files in the configuration file.
sourceFilePath = root[0][0].text
requestFilePath = root[1][0].text
driverFilePath = root[2][0].text
responseFilePath = root[3][0].text
resultFilePath = root[4][0].text

sourceFile = open(sourceFilePath)

for line in sourceFile:
	line = line.replace(',', ' ')
	command = "%s, %s"%(requestFilePath, line)
	print(command)
	output = subprocess.check_output("dir /b")
	print(output)
	
sourceFile.close()
	

