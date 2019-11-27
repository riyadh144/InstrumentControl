# $language = "Python"
# $interface = "1.0"
import SecureCRT
from SecureCRT.SecureCRT import *

tab = crt.GetScriptTab()
scr = tab.Screen

parameters = []
cmd(.1, "!mcs:22,1", .1)
cmd(.1, "!nx", 7)
cmd(.1, "!mcs:19,8003", 5)
parameters = parameters + (get_info_with_line_starting_with(scr, "!xs\r", ["DSN:"]))

xmodem_upload_wait_for_finish(scr, crt, #SecureCRT enviroment varibales we want to pass to the function
							  "!uf:30\r", # command to send to device before upload
							  "Waiting for Xmodem Start (Ctrl-D twice to cancel)",#Command to wait for before device starts
							  2,#time before device starts
							  f"/home/quanta/OneDrive/XirgoTech/CustomerSamples/allwest/11252019/truststore/" + "XT2469-{parameters[0]}-TRUSTSTORE.BIN",
							  "Xmodem Done (0)",
							  2)

cmd(.1, "!gcc", .1)
cmd(.1, "!mcs:22,0", .1)
cmd(.1, "!xs", .1)
parameters = parameters + (get_info_with_line_starting_with(scr, "!gpd\r", ["IMEI:",
																			"CCID:"]))  # here we concatenate the parameters which is done with the + operator
append_to_results_to_csv_file("/home/quanta/OneDrive/XirgoTech/CustomerSamples/allwest/11252019/11252019allwest",
							  parameters)
read_from_file_and_send("/home/quanta/OneDrive/XirgoTech/CustomerSamples/allwest/11252019/Configs", crt)


