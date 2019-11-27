# $language = "python"
# $interface = "1.0"

# #######################################
# W7 Login Script, uses AES Decryption.
# Dependences: AES.py
#
# A key can be passed in using a 16-byte 
# hex-as-ASCII string, ie, 
# 0102030405060708090a0b0c0d0e0f
# or an 16-character ASCII string, ie,
# THISISAPASSWORD!  
# Otherwise it will use the default key.
#
# Nate Williams/Xirgo Technologies
# #######################################


import AES

def main():
    '''These probably should not be plaintext floating around but.. they are.'''
    # DEFAULT_KEY = [
	# 0x22,0xC7,0x52,0xF4,0x84,0xA0,0x63,0x41,
	# 0x3E,0x54,0x55,0x83,0x48,0x0F,0x36,0x98
	# ]
    DEFAULT_KEY = [
        #0x22,0xC7,0x52,0xF4,0x84,0xA0,0x63,0x41,0x3E,0x54,0x55,0x83,0x48,0x0F,0x36,0x98
        0x58, 0x49, 0x52, 0x47, 0x4f, 0x54, 0x45, 0x43,0x48, 0x44, 0x45, 0x46, 0x41, 0x55, 0x4c, 0x54
		#0x48, 0xc0,0xb4,0xdc,0x36,0x07,0xc2,0x8f,0x3a,0x12,0x91,0x45,0xd1,0xb0,0xf4,0x90
		#0x01,0xab,0x23,0xcd,0x45,0xef,0x67,0xab,0x89,0xcd,0x01,0xef,0x23,0xab,0x45,0xcd
  ]

    DEFAULT_IV = [

        0xcb, 0x11, 0x25, 0xe4, 0x38, 0x18, 0xde, 0x1f,
        0x82, 0x49, 0xc7, 0xb2, 0xdc, 0x0d, 0xe7, 0xee
    ]

    key = []

    if crt.Arguments.Count < 1:
        key = DEFAULT_KEY
    else:
        if len(crt.Arguments.GetArg(0)) == 16:
            for i in range(0,16):
                key.append(ord(crt.Arguments.GetArg(0)[i]))
        elif len(crt.Arguments.GetArg(0)) == 32:
            for i in range(0,32,2):
                key.append(int(crt.Arguments.GetArg(0)[i:i+2],16))
        else:
            key = DEFAULT_KEY
            
    ''' Set up all the SecureCRT Mumbo-jumbo.  Initialize our decryption object'''
    crt.Screen.Synchronous     = True
    tab                        = crt.GetScriptTab()
    decrypto                   = AES.AESModeOfOperation()
        
    ''' Try a login '''
    tab.Screen.Send('login\r')
    tab.Screen.ReadString('\r',2)
    
    ''' Someone did care about the robustness of this.  So now we try five times
    to login, dumping any strings that don't translate well.  There are some
    cases where this may fail, but this should work for the most part. Five
    is the number because Ensemble prints 4 lines of junk at the beginning of
    the USB print. '''
    login_list=[]
    counter = 0
    while (not login_list):
        if counter > 4:
            return
            
        login_string = tab.Screen.ReadString('\r',1).strip('\r\n').encode('ascii')

        if not login_string:
            return
        
        ''' AES.decrypt expects a list of ints.  The device sends us a string of hex bytes,
        so here I split them into a list and convert them to ints. '''
        try:
            login_list = [int(login_string[i:i+2],16) for i in range(0,len(login_string),2)]
        except:
            counter+=1
        

    ''' Does the actual decryption.  The orin_length is hardcoded because hacky.'''
    dec_string = decrypto.decrypt(login_list,
                                  16,
                                  decrypto.modeOfOperation["CBC"],
                                  key,
                                  decrypto.aes.keySize["SIZE_128"],
                                  DEFAULT_IV)

    ''' decrypt returns a string in ASCII.  I have to do a conversion back to hex.
        This converts to hex, then slaps them all together into a nice long string
        that the device likes, then sends it.'''
    tab.Screen.Send(''.join([i.encode('hex') for i in dec_string]) + '\r')
    
main()