#$language = "Python"
#$interface = "1.0"
import time
import AES
import re


def cmd(scr, pre_wait, cmdstr, post_wait):
    if (pre_wait > 0.0):
        time.sleep(pre_wait)
    scr.Send(cmdstr + '\r')
    if (post_wait > 0.0):
        time.sleep(post_wait)

def xmodem_upload_wait_for_finish(scr,crt, cmd_to_start_upload,string_to_wait_before_upload,delay_before_upload,file_to_upload, string_to_wait_for, time_to_wait_after_string ):
	scr.Synchronous = True
	cmd(scr, 0.5, cmd_to_start_upload, 0.0)
	reswait(scr, string_to_wait_before_upload, delay_before_upload)
	scr.Synchronous = False

	crt.FileTransfer.SendXmodem(file_to_upload)
	scr.Synchronous = True
	reswait(scr, string_to_wait_for, 1)
	scr.Synchronous = False
	time.sleep(time_to_wait_after_string)


def read_from_file_and_send(file,crt):

	crt.Screen.Synchronous = True
	# Note: A IOError exception will be generated if 'input.txt' doesn't exist.
	#
	for line in open(file, "r"):
		# Send the line with an appended CR
		#
		crt.Screen.Send(line + '\r')

		# Wait for my prompt before sending the next line
		#
		crt.Screen.WaitForString(line)

	crt.Screen.Synchronous = False

def reswait(scr, resstr, wait):
    return scr.WaitForString(resstr, wait)


def get_info_with_line_starting_with(scr,cmd_to_query,start_of_parameters_array):
	scr.clear()
	sync_mem = scr.Synchronous
	scr.Synchronous = True
	cmd(scr, 0.5, cmd_to_query, 0.0)
	all_on_screen : str =scr.get()
	results=[]
	for params in start_of_parameters_array :
		results.append(re.findall("(?<="+params+")",scr.get()))
	scr.Synchronous = False

	return results
def append_to_results_to_csv_file(file,parameters):
	f = open(file, "a")
	for params in parameters:
		f.write(params+",")
	f.write("\n")

def aes_login(scr):
	DEFAULT_KEY = [
		0x58, 0x49, 0x52, 0x47, 0x4f, 0x54, 0x45, 0x43,
		0x48, 0x44, 0x45, 0x46, 0x41, 0x55, 0x4c, 0x54
	]

	DEFAULT_IV = [
		0xcb, 0x11, 0x25, 0xe4, 0x38, 0x18, 0xde, 0x1f,
		0x82, 0x49, 0xc7, 0xb2, 0xdc, 0x0d, 0xe7, 0xee
	]

	key = DEFAULT_KEY

	decrypto = AES.AESModeOfOperation()

	''' Screen Object properties '''
	sync_mem = scr.Synchronous
	scr.Synchronous = True

	''' login '''
	scr.Send('login\r')
	scr.ReadString('\r', 2)

	login_list = []
	''' AES.decrypt expects a list of ints.  The device sends us a string of hex
	bytes, so here I split them into a list and convert them to ints. '''
	login_string = scr.ReadString('\r', 1).strip('\r\n').encode('ascii')
	if (login_string == "ERROR"):
		scr.Send('Already LoggedIn\n', True)
	else:

		login_list = [int(login_string[i:i + 2], 16) for i in range(0, len(login_string), 2)]
		dec_string = decrypto.decrypt(login_list,
									  16,
									  decrypto.modeOfOperation["CBC"],
									  key,
									  decrypto.aes.keySize["SIZE_128"],
									  DEFAULT_IV)
		scr.Send(''.join([i.encode('hex') for i in dec_string]) + '\r')

	''' decrypt returns a string in ASCII.  I have to do a conversion back to hex.
		This converts to hex, then slaps them all together into a nice long string
		that the device likes, then sends it.'''

	''' restore Screen Object properties '''
	scr.Synchronous = sync_mem