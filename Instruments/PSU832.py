from pyvisa import ResourceManager
class PSU832:
    def __init__(self,visa_call_name,rm:ResourceManager):
        self.psu=rm.open_resource(visa_call_name)
    def set_voltage(self,chan,volt):
        self.psu.write(":SOURce"+str(chan)+":VOLTage "+str(volt))
    def set_current_limit(self,chan, curr):
        self.psu.write(":SOURce"+str(chan)+":CURR "+str(curr))
    def read_voltage(self,chan):
        return self.psu.query("measure? ch"+str(chan))

    def idn(self):
        return self.psu.query("*IDN?")

#Example of Usage
# rm= ResourceManager()
# psu=PSU832("TCPIP0::192.168.1.74::INSTR",rm)
# print(psu.read_voltage(1))
# psu.set_current_limit(1,1.5)
# psu.set_voltage(3,4)
# rm.close()
