import threading
import serial
import codecs
#from Timer import Timer
from enum import Enum

#from Crypto.Cipher import AES
from serial.tools import list_ports
from twisted.internet import reactor, defer
from threading import Lock
import time

class LoginState(Enum):
    XirgoAES = 0
    FedexAES = 1
    TestLogin = 2
    Ascii = 3
    Success = 4
    Timeout = 5
    Fail = 6


class Serial(object):
    DEFAULT_IV = b'\xcb\x11\x25\xe4\x38\x18\xde\x1f\x82\x49\xc7\xb2\xdc\x0d\xe7\xee'
    DEFAULT_KEY = b'\x58\x49\x52\x47\x4f\x54\x45\x43\x48\x44\x45\x46\x41\x55\x4c\x54'
    FEDEX_KEY = b'\x22\xC7\x52\xF4\x84\xA0\x63\x41\x3E\x54\x55\x83\x48\x0F\x36\x98'
    def __init__(self, _port):
        self.serial_port = _port
        self.lock = Lock()
        self.listen_lock = Lock()
        self.listen_set = False
        self.listening = False
        self.com_port = ''
        self.sPort=''
        self.foo=''
        self.fooOn=0;
        self.open_port(_port)
        threading.Thread(target=self.read_port).start()
        # def list_ports_(*args, **kwargs):
    #     _ports = [port.description.split('(')[1].split(')')[0] for port in list_ports.comports()]
    #
    #     print('Available ports')
    #     print(_ports)
    #     return (_ports)

    def open_port(self, _port):

        try:
           self.sPort = serial.Serial(_port, 115200, timeout=0.2, xonxoff=0, rtscts=0, dsrdtr=0,
                                   parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS,
                                   stopbits=serial.STOPBITS_ONE)
        except serial.serialutil.SerialException:
            return 1


        self.com_port = _port
        return 0
    def write_port(self, message):
        try:
            self.sPort.write(message.encode('utf-8'))
            time.sleep(.06)

        except (serial.serialutil.SerialException):
             pass
        return 0
    def read_port(self):
        while(True):


            bytesToRead = self.sPort.inWaiting()
            s = self.sPort.read(bytesToRead)
            s
            if s:
                try:

                    self.foo=(s.decode('utf-8'))
                    print(s.decode('utf-8'))

                except UnicodeDecodeError:
                    pass
            time.sleep(.1)

        return s

    def read_foo(self):
        return self.foo



    def _aes_login(self):
        '''These probably should not be plaintext floating around but.. they are.'''

        self.aes = AES.new(self.key, AES.MODE_CBC, self.DEFAULT_IV)

        # clear tx buffer just in case something is in there
        #self.clear_tx_buffer()

        # Login
        self.write_port('login\r')
        time.sleep(.6)
        hello = self.read_foo().split('\r')[1].strip()
        print(hello)
        try:
            self.cipher = codecs.decode(hello, 'hex_codec')
            self.plaintext = codecs.encode(self.aes.decrypt(self.cipher), 'hex_codec')
            self.write_port(self.plaintext.decode('utf-8') + '\r')
        except (TypeError, ValueError) as e:
            #self.message = self.message.decode('utf-8')
            if "Invalid '+XT' header" in hello:
                pass
            elif 'ERROR' in hello:
                pass

        return 0
##    def login(self):
##
##        login_timer = Timer()
##        login_timer.set_timer(15)
##
##        login_state = LoginState.TestLogin
##        login_options = [LoginState.XirgoAES, LoginState.FedexAES, LoginState.Ascii]
##        attempt = 0
##
##        with self.listen_lock:
##            while True:
##
##                # Check timeout
##                if login_timer.is_expired():
##                    login_state = LoginState.Timeout
##
##                # State Machine
##                if login_state == LoginState.TestLogin:
##                    if self._test_login():
##                        login_state = login_options[attempt % len(login_options)]
##                    else:
##                        login_state = LoginState.Success
##
##                elif login_state == LoginState.XirgoAES:
##                    self.key = self.DEFAULT_KEY
##                    attempt += 1
##                    if self._aes_login():
##                        login_state = LoginState.Fail
##                    else:
##                        login_state = LoginState.TestLogin
##
##                elif login_state == LoginState.FedexAES:
##                    self.key = self.FEDEX_KEY
##                    attempt += 1
##                    if self._aes_login():
##                        login_state = LoginState.Fail
##                    else:
##                        login_state = LoginState.TestLogin
##
##                elif login_state == LoginState.Ascii:
##                    attempt += 1
##                    self.write_port('XIRGOTECH116\r')
##                    login_state = LoginState.TestLogin
##
##                elif login_state == LoginState.Fail:
##                    return 1
##
##                elif login_state == LoginState.Success:
##                    print ('Device Login Successfully')
##                    return 0
##
##                elif login_state == LoginState.Timeout:
##                    return 1
##
##                login_timer.update_timer()
##                time.sleep(0.5)
##
##        return 1
    def _test_login(self):
        self.write_port('mV\r')
        time.sleep(.5)
        try:
            fw_version = self.read_foo().strip('\n').strip('\r')
        except UnicodeDecodeError:
            return 1
        if 'ERROR' in fw_version or not len(fw_version):
            return 1
        else:
            return 0
