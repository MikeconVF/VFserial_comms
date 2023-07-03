from pymodbus.client.sync import ModbusSerialClient
from IOModbusModule import IOModbusModule
from modbus_var import modbus_variables, Buttons
from EC_signal_generator import sim_EC_signal
import time

# Create an instance of the IOModbusModule class
modbus_module = IOModbusModule('/dev/cu.usbserial-1420', 115200)

# Create an instance of the modbus_variables class
modbus_vars = modbus_variables()

# Access variables from read in data 
Mod_8AI = modbus_vars.MOD_8AI['address']
flow_meter1 = modbus_vars.MOD_8AI['flow_meter1']
EC_meter1 = modbus_vars.MOD_8AI['EC_meter']

# Write out variable registers
# Analog output register
Mod_8AO = modbus_vars.MOD_8AO['address']
spoof_flow_meter1 = modbus_vars.MOD_8AO['spoof_flow_meter1']

# Create an instance for simulated sine wave signal for analog output
ec_signal = sim_EC_signal(start_value=0, end_value=19, step=1)

count = 1

while True:
    # Generate the EC signal
    signal_values = ec_signal.generate_signal()
    
    for value in signal_values:
        if value == 0:
                modbus_module.write_register(spoof_flow_meter1, 0, unit=Mod_8AO)
        if value >= 4:
            FM1_current = modbus_module.scaling_mA_integer(value)
            # Write analogue output registers
            modbus_module.write_register(spoof_flow_meter1, FM1_current, unit=Mod_8AO)
        
        modbus_module.read_register(spoof_flow_meter1, count, unit=Mod_8AI)

        # Add a delay before generating the signal again
        # Adjust the delay as needed
        time.sleep(1)

