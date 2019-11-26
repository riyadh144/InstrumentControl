import time
import numpy as np
# This function is meant to take the functions needed to sweep and query a parameter
#Over a range of values with a determined step. and return an array which concatenates the values to the parameter
def sweep(function_to_read_device,
			function_to_read_insturment,
			argument_to_read,
			function_to_set_instrument,
			 argument_to_set,range_min,
			 range_max,step,time_to_soak):
    array_to_return=[[],[]]
    for i in np.arange(range_min, range_max, step):
        function_to_set_instrument(*argument_to_set, i)
        time.sleep(time_to_soak)
        device_reading=function_to_read_device()
        insturment_reading=function_to_read_insturment(*argument_to_read)
        array_to_return[0].append(float(device_reading))
        array_to_return[1].append(float(insturment_reading))

    print(array_to_return)
    return array_to_return
