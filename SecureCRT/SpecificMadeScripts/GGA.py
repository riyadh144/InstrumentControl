''' Set up all the SecureCRT Mumbo-jumbo.  Initialize our decryption object'''
import time

def cmd(scr, pre_wait, cmdstr):
    #tab = crt.GetScriptTab()
    scr = tab.Screen
    if (pre_wait > 0.0):
        time.sleep(pre_wait)
    scr.Send(cmdstr + '\r')


tab = crt.GetScriptTab()
scr = tab.Screen
crt.Screen.Synchronous = True
tab = crt.GetScriptTab()
i=0

while(i<10000):
     i=i+1
     cmd(scr, 0.2,'AT+QGPSGNMEA="GGA"')
     time.sleep(5)