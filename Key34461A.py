from pyvisa import ResourceManager
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

    def initialize_reading(self):
        self.dmm.write("INIT")

    def sample_count(self, count: int):
        self.dmm.write(f"SAMP:COUN {count}")

    def query_config(self) -> str:
        return self.dmm.query("CONF?")

    def read(self):
        return self.dmm.query("read?")

    def idn(self):
        return self.dmm.query("*IDN?")

#Example of Usage
# rm= ResourceManager()
# dmm=Key34461a("TCPIP0::192.168.1.56::INSTR",rm)
# (dmm.set_voltage_dc_range(10,5))
# print(dmm.read())
# print(dmm.read())
# print(dmm.read())
# print(dmm.read())

#rm.close()
