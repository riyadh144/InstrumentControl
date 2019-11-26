from visa import ResourceManager 
import time

class Key34461a:
    def __init__(self,visa_call_name,rm:ResourceManager):
        self.dmm=rm.open_resource(visa_call_name)

    def set_voltage_dc_range(self, range, res):
        self.dmm.write(f"CONF:VOLT:DC  {range},{res}")

    def set_voltage_ac_range(self, range, res):
        self.dmm.write(f"CONF:VOLT:AC {range},{res}")

    def set_current_dc_range(self, range, res):
        self.dmm.write(f"CONF:CURR:DC {range},{res}")

    def set_current_ac_range(self, range: str, res: float):
        self.dmm.write(f"CONF:VOLT:DC {range},{res}")

    def initialize_reading(self): # get ready for trigger
        self.dmm.write("INIT")

    def sample_count(self, count: int): # here you will define how mnay samples you want your fetch to return 
        self.dmm.write(f"SAMP:COUN {count}")
        self.dmm.write("SAMP:SOURCE:TIM")
        
    def set_trig_source(self, trigsource): #you setup your trigger source usually our trigger is over the network so you will use  "BUS"
        self.dmm.write(f"TRIG:SOUR {trigsource}")
    def take_measurment(self):#trigger the measurment start
        self.dmm.write("*TRG")
    def read_triggered_measurment(self):
        return self.dmm.query("FETC?")
    def query_config(self) -> str:
        return self.dmm.query("CONF?")

    def read(self):
        return self.dmm.query("read?")

    def idn(self):
        return self.dmm.query("*IDN?") # this is equivelent to initialize trig and fetch at the same time, but it will return as many readings as you had set in sample_countz

#Example of Usage
# rm = ResourceManager()
# dmm=Key34461a("TCPIP0::192.168.1.56::INSTR",rm)
# dmm.set_voltage_dc_range(10,5)
# dmm.sample_count(10)
# print(dmm.read())
# dmm.initialize_reading()
# dmm.set_trig_source("BUS")
# dmm.take_measurment()
# time.sleep(1)
# print(dmm.read_triggered_measurment())
# print(dmm.read())
# print(dmm.read())
# print(dmm.read())


