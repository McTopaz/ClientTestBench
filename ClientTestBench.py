import os
import sys
import subprocess
import xml.etree.ElementTree as ET

# Include args from the source-file into a file's arguments.
def IncludeSourceFilesArgsInCommand(fileArgs, sourceFileArgs):
    # If the file's arg don't have any arguments.
    if fileArgs == "" or fileArgs == None:
        return ""
    
    fileArgs = fileArgs.replace('"', "")    # Remove the " from the file's arguments.
    args = fileArgs.split(',')              # Split the args for the file and get them as a list.
    commandArgs = []                        # These are the arguments which will be used in the file.
    
    # Iterate over all arguments for the file.
    for arg in args:
        index = int(arg)                            # Get what index each arguments represents.
        index -= 1                                  # Decrement the index so, for instance, '1' point to the source-file's '0' index.
        commandArgs.append(sourceFileArgs[index])   # Store the arguments for the command.
    
    commandArgLine = "".join("\"%s\","%(arg) for arg in commandArgs)    # A string with the file's arguments form the source-file.
    commandArgLine = commandArgLine[:-1]                                # Cut last comma and space.
    return commandArgLine

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

# Get args elements.
requestFileArgs = root[1][1].text
driverFileArgs = root[2][1].text
responseFileArgs = root[3][1].text

# Open the source file.
sourceFile = open(sourceFilePath)

# Read from source file.
for line in sourceFile:

    # Ignore any commented lines.
    if line.startswith("#"):
        continue

    # ===============================
    # === Get the line to process ===
    # ===============================
    line = line.rstrip()
    data = line

    # Checks if a comment exist in the line.
    hasComment = '#' in data	
    if hasComment:
        data = data[:data.find('#')]	# Removes the comment section.
        data = data.strip()				# Removes spaces at end of data.

    sorceFileArgs = data.split(',')
    data = "".join("\"%s\" "%(arg) for arg in sorceFileArgs)	# Put " around every argument: "<arg>".
    print("Line:\t\t%s"%(line))
    #print("Args:\t\t%s"%(sorceFileArgs))

    # ===========================
    # === Call request parser ===
    # ===========================
    args = IncludeSourceFilesArgsInCommand(requestFileArgs, sorceFileArgs)
    command = "%s %s %s"%(requestFilePath, args, data)
    print("Request command:\t" + command)
    output = subprocess.check_output(command, shell=True)
    request = output.decode("ascii").rstrip()
    #print("Request:\t%s"%(request))

    # ===================
    # === Call driver ===
    # ===================
    args = IncludeSourceFilesArgsInCommand(driverFileArgs, sorceFileArgs)
    command = "%s %s %s %s"%(driverFilePath, configurationFilePath, args, request)
    print("Driver command:\t" + command)
    output = subprocess.check_output(command, shell=True)
    response = output.decode("ascii").rstrip()
    #print("Response:\t%s"%(response))

    # ============================
    # === Call response parser ===
    # ============================
    args = IncludeSourceFilesArgsInCommand(responseFileArgs, sorceFileArgs)
    command = "%s %s %s"%(responseFilePath, args, response)
    print("Response command:\t" + command)
    output = subprocess.check_output(command, shell=True)
    result = output.decode("ascii").rstrip()
    print("Result:\t\t%s"%(result))
    print("")

    # Write to result file.
    with open(resultFilePath, "a") as resultFile:
        resultFile.write("Line:\t%s"%(line.rstrip()))
        resultFile.write("\n")
        resultFile.write("Result:\t%s"%(result.lstrip()))
        resultFile.write("\n")
        resultFile.write("\n")

sourceFile.close()
