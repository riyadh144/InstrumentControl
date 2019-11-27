#$language = "Python"
#$interface = "1.0"

# bhph_fwupdate_noring.py
# 
# with 1170AC1 FW it was found that the RING signal from the cellular module can
# cause a FW update failure if the timing is just right.
# To avoid this possibility, turn off the RING signal before update and
# then turn the RING signal back on.

update_file = 'C:\\Users\\ralalami\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\Customer Samples\\Fleetmatics\\10292018\\AAb1-1133GA1-e8.bin'
Script_File = 'C:\\Users\\ralalami\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\Customer Samples\\Fleetmatics\\10292018\\ATT_script0925ack.bin'
Parameters_File='C:\\Users\\ralalami\\OneDrive - Xirgo Technologies, LLC\XirgoTech\\Customer Samples\\Fleetmatics\\10292018\\ATT_param101718.txt'
CSV_FILE="C:\\Users\\ralalami\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\Customer Samples\\CTS\\05212019\\05212019Amazon.txt"
import AES
import time

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
    scr.ReadString('\r',2)
    
    login_list=[]
    ''' AES.decrypt expects a list of ints.  The device sends us a string of hex
    bytes, so here I split them into a list and convert them to ints. '''
    login_string = scr.ReadString('\r',1).strip('\r\n').encode('ascii')
    if(login_string=="ERROR"):
		scr.Send('Already LoggedIn\n', True)
    else:

        login_list = [int(login_string[i:i+2],16) for i in range(0,len(login_string),2)]
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

def cmd(scr, pre_wait, cmdstr, post_wait):
    if (pre_wait > 0.0):
        time.sleep(pre_wait)
    scr.Send(cmdstr + '\r')
    if (post_wait > 0.0):
        time.sleep(post_wait)

def reswait(scr, resstr, wait):
    return scr.WaitForString(resstr, wait)

def main():
    tab = crt.GetScriptTab()
    scr = tab.Screen

    cmd(scr, 0.5, ':qti', 0.0)
    qti=scr.ReadString("CCID");
    scr.Send("hello"+str(qti),True)
    IMEI=qti.split("SERIAL: ")[1]
    cmd(scr, 0.5, ':qti', 0.0)
    qti=scr.ReadString("[Status]");
    CCID=qti.split("CCID:")[1]
    cmd(scr, 0.5, ':rdval serial', 0.0)
    serial=scr.ReadString(":OK").split("ESN:")[1]
    cmd(scr, 0.5, ':q1i', 0.0)
    f = open(CSV_FILE, "a")
    x=serial.replace("\n","").replace("\r","")+","+IMEI.replace("\n","").replace("\r","")+","+CCID.replace("\n","").replace("\r","")
    x=x.replace(" ","").replace("|","")
    f.write(x+"\n")
main()
