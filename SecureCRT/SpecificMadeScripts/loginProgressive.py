
		
import AES
import time
import os
import subprocess		
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
        scr.Send(login_string)
        dec_string=subprocess.call('C:\Users\riyad\OneDrive - Xirgo Technologies, LLC\XirgoTech\aes_Psswd\aes_passwd.exe '+login_string)
        
        scr.Send(''.join([i.encode('hex') for i in dec_string]) + '\r')


    ''' decrypt returns a string in ASCII.  I have to do a conversion back to hex.
        This converts to hex, then slaps them all together into a nice long string
        that the device likes, then sends it.'''

    ''' restore Screen Object properties '''
    scr.Synchronous = sync_mem
def main():
    tab = crt.GetScriptTab()
    scr = tab.Screen

    ''' login '''
    aes_login(scr)
main()
