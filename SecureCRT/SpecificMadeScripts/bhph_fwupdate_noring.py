#$language = "Python"
#$interface = "1.0"

# bhph_fwupdate_noring.py
# 
# with 1170AC1 FW it was found that the RING signal from the cellular module can
# cause a FW update failure if the timing is just right.
# To avoid this possibility, turn off the RING signal before update and
# then turn the RING signal back on.

update_file = 'C:\\AES\\B111-1170AC2.evf'

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
		scr.Send('Already LoggedIn', True)
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

    ''' login '''
    aes_login(scr)

    ''' Disable RING signal '''
    cmd(scr, 0.5, '!cfe', 0.0)
    reswait(scr, 'Pass-thru mode', 60.0)
    cmd(scr, 10.0, 'at^scfg="URC/Ringline","off"', 0.0)
    cmd(scr, 3.0, '!cfd', 0.0)

    ''' Send firmware update file via Xmodem '''
    cmd(scr, 1.0, '!ude 0xff', 0.0)
    cmd(scr, 0.5, '!urb 1 1', 0.0)
    reswait(scr, 'waiting for xmodem', 60.0)
    crt.FileTransfer.SendXmodem(update_file)
    reswait(scr, 'starting fw install in 5 seconds', 60.0)

    ''' Wait for reset '''
    reswait(scr, 'nvm_id: ', 60.0)
    time.sleep(3.0)
    
    ''' login '''
    aes_login(scr)

    ''' Re-enable the RING signal '''
    cmd(scr, 0.5, '!cfe', 0.0)
    reswait(scr, 'Pass-thru mode', 60.0)
    cmd(scr, 10.0, 'at^scfg="URC/Ringline","local"', 0.0)
    cmd(scr, 3.0, 'at+cfun=1,1', 0.0)
    cmd(scr, 3.0, '!cfd', 0.0)

    ''' Send FW update complete message '''
    cmd(scr, 0.5, 'mV', 2.0)
    scr.Send('!!FW UPDATE COMPLETE!!\r\n', True)
    time.sleep(2.0)
    scr.Send('==PROCEEDING TO EVENT ACK VERIFICATION [OPTIONAL]==\r\n', True)

    ''' Enable cellular debug and wait for a message acknowledgment '''
    cmd(scr, 1.0, '!cde 0xffef', 0.0)
    ''' Wait up to 10 minutes to receive an ACK from the server '''
    success = reswait(scr, 'Data>+XT:UDP_ACK,', 600.0)
    if (success == True):
        success = reswait(scr, 'PowerMode: Normal, State: Sleep', 600.0)

    cmd(scr, 2.0, '!cdd', 0.0)
    cmd(scr, 0.5, 'mV', 2.0)

    ''' Send success message (to screen only) '''
    if (success == True):
        scr.Send('!!ACK VERIFY: SUCCESS!!\r\n', True)
    else:
        scr.Send('!!ACK VERIFY: FAILED!!\r\n', True)
    
main()
