#main.py

from pymodbus.client.sync import ModbusSerialClient
from modbus_var import modbus_variables
import time 

# Create a Modbus serial client
client = ModbusSerialClient(
    method='rtu',
    port='/dev/cu.usbserial-1420',  # Replace with your serial port
    baudrate=115200,  # Set the baud rate of your serial communication
    parity='N',  # Set the parity as required
    stopbits=1,  # Set the stop bits as required
    bytesize=8  # Set the data bits as required
)

# slow down script excution
time_n=0.5

# scalling 4-20mA to 1000
def scaling_mA_integer(current):
    current_min = 4  # Minimum current value in mA
    current_max = 20  # Maximum current value in mA
    integer_min = 0  # Minimum integer value
    integer_max = 1000  # Maximum integer value
    
    # Calculate the scaling factor
    scaling_factor = (integer_max - integer_min) / (current_max - current_min)
    
    # Calculate the mapped integer value
    mapped_integer = integer_min + (current - current_min) * scaling_factor
    
    # Round the mapped integer value and convert it to an integer
    mapped_integer = int(round(mapped_integer))
    
    return mapped_integer

# scalling 0-10V to 10240
def scaling_mV_integer(voltage):
    voltage_min = 0  # Minimum current value in mA
    voltage_max = 10  # Maximum current value in mA
    integer_min = 0  # Minimum integer value
    integer_max = 10240  # Maximum integer value
    
    # Calculate the scaling factor
    scaling_factor = (integer_max - integer_min) / (voltage_max - voltage_min)
    
    # Calculate the mapped integer value
    mapped_integer = integer_min + (voltage - voltage_min) * scaling_factor
    
    # Round the mapped integer value and convert it to an integer
    mapped_integer = int(round(mapped_integer))
    
    return mapped_integer

#reset register count
def update_register_number(register_number):
    if register_number < num_registers:
        return register_number + 1
    elif register_number == num_registers:
        return 0

#write register
def write_register(register_address, value, unit_id):
    # Write a single value to a holding register
    response = client.write_register(register_address, value, unit=unit_id)
    if response.isError():
        print(f"Write error occurred for register {register_address}: {response}")
    else:
        print(f"Value {value} written successfully to register {register_address}.")

# Create an instance of the modbus_variables class
modbus_vars = modbus_variables()
# Access variables from MOD_16I
MOD_16I= modbus_vars.MOD_16I['address']
start_register = modbus_vars.MOD_16I['start_button']
num_registers = modbus_vars.MOD_16I['num_registers']
start_button_latched = modbus_vars.MOD_16I['start_button_latched']
PB_reset = modbus_vars.MOD_16I['PB_reset']
register_value = []  



if client.connect():
    for register_number in range(num_registers):
        # Read the discrete input
        print( 'register number=' ,register_number)
        response = client.read_discrete_inputs(start_register + register_number, 1, unit=MOD_16I)
        # Access the retrieved data
        register_value = response.bits[0]
        if response.isError():
            print("Modbus error:", response)
            break

        # Assign the value of input register 1 to the variable "start" and latch it
        if register_number == 0:
            start_button = register_value
            if start_button and not start_button_latched:
                start_button_latched = True
                reset_button_latched = False
                Loop1_button_latched = False

        #stop button
        if register_number == 1:
            Stop_button = register_value
            if Stop_button:
                start_button_latched = False
                break
        
        # Assign the value of input register 3 to the variable "PB_reset" and reset start_button_latched
        if register_number == 2:
            PB_reset= register_value
            if PB_reset:
                reset_button_latched = True

        #bleed button must be pressed and hold to function
        if register_number == 3:
            Bleed_button = register_value
            while Bleed_button:
                print ("bleeding system")
                response = client.read_discrete_inputs(start_register + register_number, 1, unit=MOD_16I)
                print("10",start_register + register_number, " bleed value=", response.bits[0])

                if response.bits[0] == False:
                    Bleed_button = False
        
        #stop loop 1 button 
        if register_number == 4:
            Loop1_button = register_value
            if Loop1_button and not Loop1_button_latched:
                Loop1_button_latched = True
                start_button_latched = False

        # Append the register value to the list
        register_value.append(register_value)

        register_number = update_register_number(register_number)

        time.sleep(time_n)

        if start_button_latched == True:
            print ("system active")
            
        # Add a delay between reads (adjust as needed)
    client.close()
    print("Modbus serial connection closed.")

else:
    print("Unable to connect to the Modbus device")
