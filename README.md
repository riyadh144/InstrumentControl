
# InstrumentControl

## Note
I am separating the different classes into folders for ease of documentation but you need to have all the classes that you plan to use in the same directory
create a main file to run the script from
import the different modules

## Functions
Sweep function is a small script that makes sweeping a parameter and formatting its output a bit easier
It takes the following inputs
```
            function_to_read_device
			function_to_read_insturment
			argument_to_read
			function_to_set_instrument
			argument_to_set
			range_min
			range_max,step
			time_to_soak
```
And returns an array of the following format
```
[[array_of_swept_parameter],[array_of_measured_parameter]]
```

## Logging
To log the output of the console (your print statments) from pycharm follow this guide
https://www.jetbrains.com/help/pycharm/setting-log-options.html
## Dependencies
Depending on how you want to install the dependencies, you can either use pip from the command line or use the method in your favorite IDE
for example in pycharm use the following guide
https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html
### Visa
```
pip install pyvisa

```
Also install ni visa drivers, depending on your OS
https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#329456
### pyserial
```
#Install from command line
pip install pyserial
#import in a python program
import serial
```

### twisted

```
pip install Twisted
#import in a python program
import twisted
```

### minimalmodbus
```
#Install from command line
pip install minimalmodbus
#import in a python program
import minimalmodbus
```

### numpy
```
#Install from command line]
pip install numpy
#import in a python program
import numpy as np
```