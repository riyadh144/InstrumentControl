#$language = "Python"
#$interface = "1.0"
import time
import re

tab = crt.GetScriptTab()
scr = tab.Screen


def cmd(scr, pre_wait, cmdstr, post_wait):
    if (pre_wait > 0.0):
        time.sleep(pre_wait)
    scr.Send(cmdstr + '\r')
    if (post_wait > 0.0):
        time.sleep(post_wait)

def xmodem_upload_wait_for_finish(scr,crt, cmd_to_start_upload,string_to_wait_before_upload,delay_before_upload,file_to_upload, string_to_wait_for, time_to_wait_after_string ):

	cmd(scr, 0.5, cmd_to_start_upload, 2)
	reswait(scr, string_to_wait_before_upload, delay_before_upload)


	crt.FileTransfer.SendXmodem(file_to_upload)

	reswait(scr, string_to_wait_for, 1)

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
		time.sleep(1)

	crt.Screen.Synchronous = False

def reswait(scr, resstr, wait):
    return scr.WaitForString(resstr, wait)


def get_info_with_line_starting_with(scr,cmd_to_query,start_of_parameters_array):
	scr.Clear()
	sync_mem = scr.Synchronous

	cmd(scr, 0.5, cmd_to_query, 0.0)
	all_on_screen =scr.ReadString("OK")

	results=[]
	#cmd(scr,0.1,all_on_screen,0.1)

	for params in start_of_parameters_array :
		results.append(re.search("(?<="+params+").*",all_on_screen).group().strip("\r").strip(" ").encode("ascii"))
		#cmd(scr,0.1,re.findall("(?<="+params+")",all_on_screen)[0],.1)
	


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

parameters=[]
cmd(scr,.1,"!mcs:3,22,1\r",.1)
cmd(scr,.1,"!nx\r",7)
cmd(scr,.1,"!mcs:19,8003\r",5)
x=(get_info_with_line_starting_with(scr,"!xs\r",["DSN:"]))
parameters.append(x[0])
xmodem_upload_wait_for_finish(scr,crt,"!uf:30\r","Waiting for Xmodem Start (Ctrl-D twice to cancel)",2,"/home/quanta/OneDrive/XirgoTech/CustomerSamples/allwest/11252019/truststore/"+"XT2469-"+str(parameters[0])+"-TRUSTSTORE.BIN","Xmodem Done (0)",2)

cmd(scr,5,"!gcc\r",15)
cmd(scr,.1,"!mcs:3,22,0\r",.1)
cmd(scr,.1,"!xs\r",.1)
x=get_info_with_line_starting_with(scr,"!gpd\r",["IMEI:","CCID:"])
parameters.append(x[0])
parameters.append(x[1])

read_from_file_and_send("/home/quanta/OneDrive/XirgoTech/CustomerSamples/allwest/11252019/Configs",crt)
append_to_results_to_csv_file("/home/quanta/OneDrive/XirgoTech/CustomerSamples/allwest/11252019/11252019allwest",parameters)
cmd(scr,.5,"!nx\r",.1)
