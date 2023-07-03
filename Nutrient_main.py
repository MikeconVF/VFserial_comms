from StartLoop import start_loop_module
from Default_Preset import Default_Preset_Value
from IOModbusModule import IOModbusModule
import time
import math

# Create an instance of the IOModbusModule class
modbus_module = IOModbusModule('/dev/cu.usbserial-1420', 115200)

counter=0
time_n=0.5

# Define the time step and frequency for the sine wave
time_step = 0.1
frequency = 0.1
# Initialize the time variable
time = 0

#set default register values
Default_Preset_Value(modbus_module)

while True:
    #check stop loops
    stop_state = start_loop_module(modbus_module)

    # spoofing ec meter and flow meter
    value1 = 12 + 8 * math.sin(2 * math.pi * frequency * time)
    value2 = 12 + 8 * math.sin(2 * math.pi * frequency * (time + 1))

    if not stop_state:
        #error catch on 
        try:
            signal_list = start_loop_module(modbus_module)

        except ValueError as e:
            # Handle the raised ValueError from start_loop_module
            error_message, stop_list = e.args
            print(error_message,stop_list)
            #print("Stop List:", stop_list)


    time.sleep(time_n)



# Close the Modbus connection
#modbus_module.close()
