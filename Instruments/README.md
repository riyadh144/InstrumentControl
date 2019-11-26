# Description
This Folder has the classes to control some of the instruments in the lab

# Dependencies

## miminalmodbus
```
pip install minimalmodbus
```
##pySerial
```
pip install pyserial
```
##pyvisa
```
pip install pyserial
```

# Example of Use

```
#Example of Usage
voltages=[]
rm= ResourceManager()# you define the resource manager that is one resource manager per whole script, one resource manager is responsible for many different instruments
dmm=Key34461a("TCPIP0::192.168.1.56::INSTR",rm) # here you create an  Keysight dmm object which has a TCPIP identifier and is manager by the resource manager already defined
dmm.set_voltage_dc_range(10,5) #here you configure your device to the range you want to be reading at, the description of this function is int the prototype
print(dmm.read()) # you issue a read command to the instrumet and the value is returned to you via a the function then you can process it, read it, append it to a matrix....
voltage=dmm.read()
voltages.append (dmm.read())
``` 

