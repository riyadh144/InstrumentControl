#$language = "Python"
#$interface = "1.0"

# bhph_fwupdate_noring.py
# 
# with 1170AC1 FW it was found that the RING signal from the cellular module can
# cause a FW update failure if the timing is just right.
# To avoid this possibility, turn off the RING signal before update and
# then turn the RING signal back on.

update_file = '/home/quanta/OneDrive/XirgoTech/CustomerSamples/Fedex/09232019/PBz1.1178AA2.1.5502f3b.bin'
#update_file='NULL'
boot_file ='/home/quanta/OneDrive/XirgoTech/CustomerSamples/Fedex/09232019/PBzB.1178AA2.1.5502f3b.bin'
#boot_file='NULL'
ConfigFile = "/home/quanta/OneDrive/XirgoTech/CustomerSamples/Fedex/09232019/configs.txt"
#ConfigFile="NULL"
#Parameters_File="NULL"
TPS_FILE="NULL"
CSV_FILE="/home/quanta/OneDrive/XirgoTech/CustomerSamples/Fedex/09232019/09232019.csv"
macSerial="/home/quanta/OneDrive/XirgoTech/Firmware/Releases/Sitar/DoorSensorMacSitar.csv"

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

    tab = crt.GetTab(1)
    scr = tab.Screen
    tab2=crt.GetTab(2)
    scr2=tab2.Screen

    ''' login '''
    #aes_login(scr)

    ''' Send firmware update file via Xmodem '''
    if(boot_file!="NULL"):
         cmd(scr, 0.5, '', 0.0)
         cmd(scr, 0.5, '!xi', 0.0)	
         cmd(scr, 0.5, '!uf:2,xmodem', 0.0)

         reswait(scr, 'Waiting for Xmodem Start (Ctrl-D twice to cancel)', 10.0)
         crt.FileTransfer.SendXmodem(boot_file)
         reswait(scr,"Application Initialization", 0.0)

         ''' Wait for reset '''
         time.sleep(10.0)
         #aes_login(scr)

    ''' Send FW update complete message '''
    cmd(scr, 0.5, '!xs', 2.0)
    scr.Send('!!FW UPDATE COMPLETE!!\r\n', True)
    if(update_file!="NULL"):
         cmd(scr, 0.5, '!uf:1,xmodem', 0.0)
         reswait(scr, 'Waiting for Xmodem Start (Ctrl-D twice to cancel)', 30.0)
         crt.FileTransfer.SendXmodem(update_file)
         reswait(scr, 'Application Initialization', 0.0)
         time.sleep(20.0)

         cmd(scr, 0.5, '!xs', 0.5)
         cmd(scr, 0.5, '!xs', 0.5)
         cmd(scr, 0.5, '!xs', 0.5)

         cmd(scr, 0.5, '!npakas', 0.0)
         cmd(scr, 0.5, '!npstms', 0.0)
         cmd(scr,0.5,".....PLUG THE CABLE",0.0)
         time.sleep(100.0)
    #aes_login(scr)
    tab2.Activate()
    
    cmd(scr2,0.5,"adb root",0.0)
    cmd(scr2,0.5,"/home/quanta/OneDrive/XirgoTech/Firmware/Releases/Sitar/1178AA4.1/1178AA2.1_to_1178AA4.3.zip /data/update.zip ",65.0)
    cmd(scr2,0.5,"adb shell",0.2)
    cmd(scr2,0.5,"touch /cache/recovery/command",0.2)
    cmd(scr2,0.5,'echo "--update_package=/data/update.zip" > /cache/recovery/command',10)
    cmd(scr2,0.5,"reboot recovery",50)
    tab.Activate()
    cmd(scr, 15, '!npakas', 0)
    cmd(scr, 0.5, '!npstms', 190)
    tab2.Activate()
    cmd(scr2,0.5,"adb logcat |grep 1178",10)
    cmd(scr2,0.5,"\003",10)
    cmd(scr2,0.5,"adb shell cat /proc/version",10)
    cmd(scr2,0.5,"adb install -r -t /home/quanta/OneDrive/XirgoTech/Firmware/Releases/Sitar/DBz1.1178AA2.4e8b4ae4.apk",10)
    tab.Activate()
    cmd(scr,0.5,".....UNPLUG THE CABLE..........",0.0)
    cmd(scr,0.5,"!nx",2)
    if(ConfigFile!="NULL"):
        cmd(scr, 5, '!npakas', 0.1)
        cmd(scr, 15, '!npakas', 0.1)
        cmd(scr, 0.5, '!npstms', 100)
        for line in open(ConfigFile, "r"):
		# Send the line with an appended CR
		#
            crt.Screen.Send(line + '\r')
	 
		# Wait for my prompt before sending the next line
		#
            #crt.Screen.WaitForString(line)
            time.sleep(.1)

    cmd(scr, 0.5, '!xs', 0.0)
    serial=scr.ReadString("PLATFORM:").split("SERIALSTR: ")[1]
    cmd(scr, 0.5, '!mcs:7,'+serial, 0.5)
    cmd(scr, 0.5, '!mcs:6,4', 1)
    time.sleep(.5)

    for line in open(macSerial,"r"):
        x=line.split(',')
        #cmd(scr,0.5,x[0],0.5)
        #cmd(scr,0.5,line,0.5)
        
        #cmd(scr,0.5,str(serial in line),0.5)

        if(x[0] in serial):
            cmd(scr,0.5,"!mcs:25,"+x[1],0.5)
            break
        
    cmd(scr, 0.5, '!xs', 1.0)
       
    cmd(scr, 1, "!npscmd:!gpd", 0.0)
    qti=scr.ReadString("ICCID1:");
    IMEI=qti.split("IMEI:")[1]
    cmd(scr, 1, '!npscmd:!gpd', 0.0)
    qti=scr.ReadString("ICCID2");
    CCID=qti.split("ICCID1:")[1]
    cmd(scr, 0.5, '!npscmd:!gpd', 0.0)
    qti=scr.ReadString("OK");
    CCID2=qti.split("ICCID2:")[1]
    f = open(CSV_FILE, "a")
    x=serial.replace("\n","").replace("\r","")+","+CCID.replace("\n","").replace("\r","")+","+CCID2.replace("\n","").replace("\r","")+","+IMEI.replace("\n","").replace("\r","")
    x=x.replace(" ","").replace("|","")
    f.write("0,"+x+"\n")
    cmd(scr, 0.5, '!nx', 0.0)
    cmd(scr,0.5,".....DONE..........",0.0)

   
main()
