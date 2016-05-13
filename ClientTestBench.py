import os
import sys
import subprocess
import xml.etree.ElementTree as ET

if len(sys.argv) != 2 or os.path.isfile(sys.argv[1]) == False:
	print("Error: No configuration file specified.")
	sys.exit()
	
configurationFilePath = sys.argv[1]			# Gets the configuration file.
xmlFile = ET.parse(configurationFilePath)	# Parse the XML-structure in the configuration file.
root = xmlFile.getroot()					# Get the root folder in the XML-structure.

# Get all files in the configuration file.
sourceFilePath = root[0][0].text
requestFilePath = root[1][0].text
driverFilePath = root[2][0].text
responseFilePath = root[3][0].text
resultFilePath = root[4][0].text

sourceFile = open(sourceFilePath)

# Read from source file.
for line in sourceFile:

	# Ignore any commented lines.
	if line.startswith("#"):
		continue
		
	# Get the line to process.
	line = line.rstrip()
	data = line.rstrip()
	parts = data.split(',')
	data = "".join("\"%s\" "%(part) for part in parts)	# Put " around every argument: "<arg>".
	print("Line:\t\t%s"%(line))
	
	# Call request parser.
	command = "%s %s"%(requestFilePath, data)
	output = subprocess.check_output(command, shell=True)
	request = output.decode("ascii").rstrip()
	print("Request:\t%s"%(request))

	# Call driver.
	command = "%s %s %s"%(driverFilePath, configurationFilePath, request)
	output = subprocess.check_output(command, shell=True)
	response = output.decode("ascii").rstrip()
	print("Response:\t%s"%(response))

	# Call response parser.
	command = "%s %s"%(responseFilePath, response)
	output = subprocess.check_output(command, shell=True)
	result = output.decode("ascii").rstrip()
	print("Result:\t\t%s"%(result))
	print("")
	
	# Write to result file.
	with open(resultFilePath, "a") as resultFile:
		resultFile.write(line.rstrip())
		resultFile.write(os.linesep)
		resultFile.write(result.lstrip())
		resultFile.write(os.linesep)
	
sourceFile.close()
