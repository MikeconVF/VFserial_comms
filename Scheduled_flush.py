#Scheduled flush
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

Address_16I= modbus_variables.MOD_16I['address']
test_button = modbus_variables.MOD_16I['test_button']
num_registers = modbus_variables.MOD_16I['num_registers']
start_button_latched = modbus_variables.MOD_16I['start_button_latched']
PB_reset = modbus_variables.MOD_16I['PB_reset']
register_value = []  

# Read holding registers
def read_holding_registers(address, count, unit):
    response = client.read_holding_registers(address, count, unit=unit)
    if response.isError():
        print(f"Read error occurred for holding registers starting at {address}: {response}")
    else:
        print(f"Holding registers starting at {address}: {response.registers[0]}")
    register_value = response.registers[0]
    return  register_value
# Read discrete inputs
def read_discrete_inputs(address, count, unit):
    response = client.read_discrete_inputs(address, count, unit=unit)
    if response.isError():
        print(f"Read error occurred for discrete inputs starting at {address}: {response}")
    else:
        print(f"Discrete inputs starting at {address} - {address + count - 1}: {response.bits}")
    register_value = response.registers[0]
    return  register_value

def read_coils(address, count, unit):
    response = client.read_coils(address, count, unit=unit)
    if response.isError():
        print(f"Read error occurred for coils starting at {address}: {response}")
    else:
        print(f"Coils starting at {address} - {address + count - 1}: {response.bits[0]}")
    register_value = response.bits[0]
    return  register_value

Diana_value = False

if client.connect():

    #Diana_value to be replace
    Diana_value = read_coils(test_button,1, Address_16I)
    print('push button',Diana_value)

    #initialise flush sequence
    while Diana_value:
        #stop nutriend injector -> open NC relay for on/of funtionality 
        

    client.close()
    print("Modbus serial connection closed.")

else:
    print("Unable to connect to the Modbus device")
