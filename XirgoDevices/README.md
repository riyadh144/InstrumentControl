# Description
This Folder has the classes to control Xirgo Devices over serial protocol

# Dependencies

## Twisted
```
pip install Twisted
```
# Example of Use

```
#depending on how many devices you have in your setup you will creat a new variable that initializes an object identified by its com port.
sitar1= Sitar("COM1") #Depending on your OS this could be dev/ttyUSB0
sitar2= Sitar("COM2")

# using a function in that class
temperatures=[]#Initialize a temperature array that we are going to log to
temperatures.append(sitar1.getTemp())
#Now this array has that temperature in it and you can loop multi:ple times over the temperature.
#You can mainpulate that data, or print it.
print(temperatures)

``` 

