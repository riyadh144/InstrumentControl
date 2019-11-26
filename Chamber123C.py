# This will import the entire minimalmodbus library
# import minimalmodbus

# This is to import the Instrumnet class under the minimalmodbus library
from minimalmodbus import Instrument as Ins
import time
#import minimalmodbus.Instrument

class ChamberOld(Ins):
    def set_baud_rate(self, baud):
        self.serial.baudrate=baud
    def read_temp(self):
        return self.read_register(100, 0, 3, True)/10 #Read the Actual Temperature
    def read_set_temp(self):
        return self.read_register(300, 0, 3, True)/10 #Read the set Temperatuer
    def set_temp(self,temp):
        self.write_register(300,temp,1,6,True) #write the set Temperatuer

    def temp_soak(self,temp,seconds):#Will set the temperature wait for it to be within one degree and then soak for the given time
        time.sleep(1)

        self.write_register(300,temp,1,6,True) #write the set Temperatuer
        time.sleep(seconds)
        current_temp=self.read_temp()
        print(current_temp)
        if(abs(current_temp-temp)>1):
             time.sleep(60)
             
#Example of Usage
# temp=ChamberOld("com53", 1)
# temp.set_baud_rate("9600")
# temp.set_temp(-40)
# print(temp.read_temp())
# print(temp.read_set_temp())
