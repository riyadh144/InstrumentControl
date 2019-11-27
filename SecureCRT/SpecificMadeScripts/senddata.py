# $language = "python"
# $interface = "1.0"

# This script demonstrates how to open a text file and read it line by
# line to a server.
import sys

def main():
	crt.Screen.Synchronous = True
	# Note: A IOError exception will be generated if 'input.txt' doesn't exist.
	#
	for line in open(crt.Arguments[0], "r"):
		# Send the line with an appended CR
		#
		crt.Screen.Send(line + '\r')
	 
		# Wait for my prompt before sending the next line
		#
		crt.Screen.WaitForString(line)

	crt.Screen.Synchronous = False

	
main()
