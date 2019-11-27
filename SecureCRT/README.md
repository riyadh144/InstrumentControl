# DESCRIPTION
Those are already made scripts for customer sampling, preparing devices and getting info from the devices.

# GUIDE
## FileNames
Remember to change the file names
### Windows
In windows a file must be with the following format 
Note the double slash // 
"C://Folder//File.txt"
### Linux 
In linux the file is the same as if you are writing in a terminal, 
Follow these steps to get the path
    1.open a terminal in the file location usually right click then open in terminal
    2.Enter "PWD" in the opened terminal
    3.Copy and paste that folder location
    4.append the file name "/file.ext" to the end of that path

## Tips
In some of the scripts they will start with something like the code below
if you want to not update the firmware then you comment the update_file='C:\\....'
And uncomment the update_file='NULL'
This will make it skip the update firmware step
```
update_file = 'C:\\Users\\riyad\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\CustomerSamples\\Naia\\AAa4-1133HB1.4.ebf'
#update_file='NULL'
boot_file ='C:\\Users\\riyad\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\CustomerSamples\\Naia\\AAzB-1133BD1.bin'
boot_file='NULL'
Script_File = "C:\\Users\\riyad\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\CustomerSamples\\Naia\\checkin_only_script.bin"
#Script_File="NULL"
Parameters_File="C:\\Users\\riyad\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\CustomerSamples\\Naia\\checkin_only_param.txt"
#Parameters_File="NULL"
#TPS_FILE="C:\\Users\\riyad\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\Customer Samples\\Navistar\\03152019\\tpsBlocks_JBus.tps"
TPS_FILE="NULL"
CSV_FILE="C:\\Users\\riyad\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\CustomerSamples\\Naia\\Naia10142019.txt"
#Cert_File="C:\\Users\\riyad\\OneDrive - Xirgo Technologies, LLC\\XirgoTech\\Customer Samples\\CTS\\\05212019\\"
```


