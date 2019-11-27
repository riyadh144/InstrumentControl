from comms import Serial
from datetime import datetime, date, timedelta
from datetime import timedelta
# from pyfirmata import ArduinoMega, util

import time


class Sitar(Serial):
    def __init__(self, _port):
        self.com_port = _port
        self.login_state = 0
        Serial.__init__(self, _port)
        self.serialNum = ''
        self.IMEI = ''
        self.CCID = ''
        self.current = []
        time.sleep(.02)

        self.write_port("\r")
        time.sleep(.02)
        # Telling Sitar Not to Sleep
        self.write_port("!npakas\r")
        self.write_port("\r")
        self.write_port("!npakas\r")

        self.write_port("\r")
        time.sleep(.02)
        time.sleep(.02)

        self.write_port("!npstms\r")
        self.write_port("!npstms\r")

        self.write_port("\r")


    def test_batteryVoltage(self):
        self.write_port("!nas\r")
        self.write_port("!rp:5\r")
        return (str(self.read_foo().split('BATTERYVOLTAGE:')[1].split('\r')[0].replace(" ", "")))

    def test_OUT1Short(self):
        self.write_port("!is:5\r")

    def test_OUT1Open(self):
        self.write_port("!ic:5\r")

    def getSerial(self):
        return self.get_value("!xs", "SERIALSTR: ",4)


    def get_value(self,command,thing_before_it,countFail): # this is a general command that can be used to construct mroe specific functions
        self.write_port("\r")
        time.sleep(.05)
        # this will be used for SITAR as it fails to take the whole word at low temps so it needs to be feed character by charachter
        # for c in command:
        #     self.write_port(c)
        #     time.sleep(.1)
        self.write_port(command)
        self.write_port("\r")
        time.sleep(.07)
        string = self.read_foo()
        if (thing_before_it in string):
            after=string.split(thing_before_it)[1]
            before_the_return=after.split['r'][0]
            return (string.split(thing_before_it)[1].split('\r')[0])
        elif (countFail > 1):
            return self.get_value(command,thing_before_it,countFail - 1)
        else:
            return 0
    def getTemp(self):
        return self.get_value("!rp:9","TEMPVOLTAGE: ",4)
    def get_main_volt_adc(self):
        return self.get_value("!rp:1","MAINVOLTAGE: ",4)

    def get_solar_volt_adc(self):
        return self.get_value("!rp:20", "SOLARVOLTAGE: ",4)

    def get_bat_volt_adc(self):
        return self.get_value("!rp:5", "BATTERYVOLTAGE: ",4)

    def getADCs(self,countFail):
        self.write_port("\r")
        time.sleep(.02)
        self.write_port("!rp:*")
        self.write_port("\r")
        time.sleep(.02)
        string = self.read_foo()

    def checkGPS(self):
        self.write_port("Gpi\r")
        first = datetime.strptime(self.read_foo().split("Time: ")[1].split('\r')[0], '%m/%d/%Y %H:%M:%S').time()
        time.sleep(1)
        self.write_port("Gpi\r")
        second = datetime.strptime(self.read_foo().split("Time: ")[1].split('\r')[0], '%m/%d/%Y %H:%M:%S').time()
        FMT = '%H:%M:%S'
        print(first.second - second.second)

    def testPower(self):
        self.board.digital[self.arduinoPin].write(1)
        time.sleep(3)
        self.write_port("Xpd\r")
        print(self.read_foo().split('Voltage{VoltageMain}:')[1].split('\r')[0])

        self.board.digital[self.arduinoPin].write(0)
        time.sleep(3)
        self.write_port("Xpd\r")
        print(self.read_foo().split('Voltage{VoltageMain}:')[1].split('\r')[0])

