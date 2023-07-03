from pymodbus.client.sync import ModbusSerialClient
from IOModbusModule import IOModbusModule
from modbus_var import modbus_variables
from EC_signal_generator import sim_EC_signal
import time

# Create an instance of the IOModbusModule class
modbus_module = IOModbusModule('/dev/cu.usbserial-1420', 115200)

# Create an instance of the modbus_variables class
modbus_vars = modbus_variables()

# Access variables from read-in data 
Mod_8AI = modbus_vars.MOD_8AI['address']
flow_meter5 = modbus_vars.MOD_8AI['flow_meter5']
EC_meter1 = modbus_vars.MOD_8AI['EC_meter']

# Write out variable registers
# Analog output register
Mod_8AO = modbus_vars.MOD_8AO['address']
spoof_flow_meter1 = modbus_vars.MOD_8AO['spoof_flow_meter1']
Mod_16RO = modbus_vars.MOD_16RO['address']
I_pump1 = modbus_vars.MOD_16RO['i_pump1']
warning_lamp1 = modbus_vars.MOD_16RO['warning_light1']

# Create an instance for simulated sine wave signal for analog output
FM_signal = sim_EC_signal(start_value=0, end_value=19, step=1)

count = 1
# HZ frequency of injection pump
counter_trigger = 4

# EC_meter value set to 5mA
def EC_meter():
    EC_current_uA = modbus_module.read_register(EC_meter1, count, unit=Mod_8AI)
    EC_current = modbus_module.scaling_uA_mA(EC_current_uA)

    if EC_current <= 5:
        raise ValueError("EC current is too low: {}".format(EC_current))
    elif EC_current >= 15:
        raise ValueError("EC current is too high: {}".format(EC_current))

    return EC_current

# Treating flow meter as good when greater than 4mA
# Write out to 8AO
def spoof_FMsignal(value):
    # Flow meter
    if value == 0:
        modbus_module.write_register(spoof_flow_meter1, 0, unit=Mod_8AO)
    elif value > 4:
        FM1_integer = modbus_module.scaling_mV_integer(7)
        # Write analog output registers
        modbus_module.write_register(spoof_flow_meter1, FM1_integer, unit=Mod_8AO)
    elif value == 20:
        raise ValueError("FM current is too high: {}".format(value))

# FM_meter value set to 7mA
def FM_meter():
    FM_current_uA = modbus_module.read_register(flow_meter5, count, unit=Mod_8AI)
    FM_current = modbus_module.scaling_uA_mA(FM_current_uA)
    return FM_current

def counter_loop():
    global counter  # Declare 'counter' as global to modify its value
    counter += 1
    if counter == 3:
        counter = 0  # Reset counter to 0
        return True
    else:
        return False


# Injection pump and warning lamp controller
def Inj_pump_controller(injection_pulse):
    # Injection pump
    modbus_module.write_digital_coil(I_pump1, injection_pulse, Mod_16RO)
    # Warning lamp
    modbus_module.write_digital_coil(warning_lamp1, injection_pulse, Mod_16RO)

    read_pump1 = modbus_module.read_digital_coils(I_pump1, 1, Mod_16RO)
    # Warning lamp
    read_warning_light1 = modbus_module.read_digital_coils(warning_lamp1, 1, Mod_16RO)
    print(f"read data: {read_pump1}, {read_warning_light1}")

counter = 0

try:

    while True:
        # Generate the EC signal
        signal_values = FM_signal.generate_signal()

        for i, value in enumerate(signal_values):
            # EC meter to artificially made by current generator
            EC_current = EC_meter()
            # Spoofing flow meter signal using for loop counter
            spoof_FMsignal(value)
            FM_current = FM_meter()

            if EC_current >= 5 and FM_current >= 7:
                injection_pulse = counter_loop()  # Trigger the counter on the 4th iteration
                print(f"Counter triggered: {injection_pulse}")
                Inj_pump_controller(injection_pulse)
            else:
                Inj_pump_controller(False)
                print(f"Counter triggered: {False}")

            print(f"Iteration {i}")
            # Add a delay before generating the signal again
            # Adjust the delay as needed
            time.sleep(1)

except ValueError as e:
    # Handle the ValueError
    print("Error:", str(e))
