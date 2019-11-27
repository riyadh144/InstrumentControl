import time
import numpy as np
from pyvisa import ResourceManager
# import Chamber123C
# import PSU832
# import Key34461A
# import Sitar

#To run the script from another folder then you need to import the module with the commands below, uncomment those and comment the ones above.
import Instruments.Chamber123C as Chamber123C
import Instruments.Key34461A as Key34461A
import Instruments.PSU832 as PSU832
import XirgoDevices.Sitar as Sitar


def sweep(function_to_read_device,
		  function_to_read_insturment,
		  argument_to_read,
		  function_to_set_instrument,
		  argument_to_set, range_min,
		  range_max, step, time_to_soak):
	array_to_return = [[0], [0]]
	for i in np.arange(range_min, range_max, step):
		function_to_set_instrument(*argument_to_set, i)
		time.sleep(time_to_soak)
		device_reading = function_to_read_device()
		insturment_reading = function_to_read_insturment(*argument_to_read)
		array_to_return[0].append(float(device_reading))
		array_to_return[1].append(float(insturment_reading))

	print(array_to_return)
	return array_to_return


rm = ResourceManager()
# Initialize Communication With the Instruments, and creating their objects
chamber = Chamber123C.ChamberOld("/dev/ttyUSB2", 1)#COM1-100 IN WINDOWS
chamber.set_baud_rate(9600)  # Setting the baudrate of the Chamber
psu = PSU832.PSU832("TCPIP0::192.168.1.74::INSTR", rm)  # Connection over ethernet
dmm = Key34461A.Key34461a("TCPIP0::192.168.1.56::INSTR", rm)  # Connection over ethernet

# Initializing our devices under test in this case two sitars
sitar1 = Sitar.Sitar("/dev/ttyUSB0")
sitar2 = Sitar.Sitar("/dev/ttyUSB1")

# Initializing storage variables
bat_adc_1 = [[0, [[0], [0]]]]
solar_volt_adc_1 = [[0, [[0], [0]]]]
main_volt_adc_1 = [[0, [[0], [0]]]]
temp_adc_1 = [[0], [0]]
bat_adc_2 = [[0, [[0], [0]]]]
solar_volt_adc_2 = [[0, [[0], [0]]]]
main_volt_adc_2 = [[0, [[0], [0]]]]
temp_adc_2 = [[0], [0]]

# Check Communication With the Instruments
print(chamber.read_temp())
print(psu.idn())
print(dmm.idn())

# Check communication with our devices

s1 = sitar1.getSerial()
s2 = sitar2.getSerial()
time.sleep(1)
print(s1)
print(s2)
sitar1.getADCs(1)
# Sweeping Temperature -40C to 70C in 5 degree steps It will soak at -40 for 2hours and 30 mins at each temperature after that
# print(sweep(sitar1.get_bat_volt_adc, dmm.read, psu.set_voltage, [3], 3.5, 4.2, .05, 1))

# chamber.temp_soak(-40,2*60*60)

for temp in range(-20, 70, 5):
	if temp == -20:
		chamber.temp_soak(temp, 2 * 60 * 60)
	else:
		chamber.temp_soak(temp, .5 * 60 * 60)

	# sweep bat voltage
	bat_adc_1.append([temp, sweep(sitar1.get_bat_volt_adc, #passing the function we wantto use to read from the device function_to_read_device,
								dmm.read,  # passomg the function we want to use to read from the instrument
								[],  # passing the parameters of the read function
								psu.set_voltage,  # passing the function we want to use to set the instrument
								[3],  # passing the parameters of that function
								3.5,  # range min
								4.2,  # range max to sweep
								.05,  # sweep step
								1)])  # time to soak before taking the measurment
	# The rest of the sweeps follow the example of the first one
	bat_adc_2.append([temp, sweep(sitar2.get_bat_volt_adc, dmm.read, [], psu.set_voltage, [3], 3.5, 4.2, .05, 1)])
	# sweep main voltage
	main_volt_adc_1.append(
		[temp, sweep(sitar1.get_main_volt_adc, psu.read_voltage, [1], psu.set_voltage, [1], 3, 20.5, .1, 1)])
	main_volt_adc_2.append(
		[temp, sweep(sitar2.get_main_volt_adc, psu.read_voltage, [1], psu.set_voltage, [1], 3, 20.5, .1, 1)])
	# sweep  solar voltage
	solar_volt_adc_1.append(
		[temp, sweep(sitar1.get_solar_volt_adc, psu.read_voltage, [2], psu.set_voltage, [2], 0, 10.5, .1, 1)])
	solar_volt_adc_2.append(
		[temp, sweep(sitar2.get_solar_volt_adc, psu.read_voltage, [2], psu.set_voltage, [2], 0, 10.5, .1, .1)])
	# temp logging
	temp_adc_1.append([chamber.read_temp(), float(sitar1.getTemp(4))])
	temp_adc_2.append([chamber.read_temp(), float(sitar2.getTemp(4))])
	#Printing out our arrays on every loop so that if there was some trouble you still have the data from before
	print(temp_adc_1)
	print(temp_adc_2)
	print(solar_volt_adc_1)
	print(solar_volt_adc_2)
	print(main_volt_adc_1)
	print(main_volt_adc_2)
	print(bat_adc_1)
	print(bat_adc_2)
