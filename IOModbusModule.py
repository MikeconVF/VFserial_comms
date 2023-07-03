#IOModbusModule.py

from pymodbus.client.sync import ModbusSerialClient

class IOModbusModule(object):
    def __init__(self, master_port: str, baudrate: int):
        self.client = ModbusSerialClient(
            method='rtu',
            port=master_port,
            baudrate=baudrate,
            parity='N',
            stopbits=1,
            bytesize=8
        )
        self.client.connect()
    print("Connected to Modbus device")

    def close(self):
        self.client.close()

    def read_digital_coils(self, address, count, unit):
        response = self.client.read_coils(address, count, unit=unit)
        if response.isError():
            print(f"Read error occurred for coils starting at {address}: {response}")
        #else:
            #print(f"Coils starting at {address} - {address + count - 1}: {response.bits}")
        #register_values = response.bits

        return response.bits[0]

    def write_digital_coil(self, address, value, unit):
        response = self.client.write_coil(address, value, unit=unit)
        if response.isError():
            print(f"Write error occurred for coil at address {address}: {response}")
        #else:
            #print(f"Coil at address {address} set to {value}")

    def write_register(self, address, value, unit):
        response = self.client.write_register(address, value, unit=unit)
        if response.isError():
            print(f"Write error occurred for register at address {address}: {response}")
        #else:
            #print(f"Register at address {address} set to {value}")

    def read_register(self, address, count, unit):
        response = self.client.read_input_registers(address, count, unit=unit)
        if response.isError():
            print(f"Read error occurred for registers starting at {address}: {response}")
        #else:
            #print(f"Registers starting at {address} - {address + count - 1}: {response.registers[0]}")
        register_values = response.registers[0]
        return register_values

    # Scaling 4-20mA to 1000
    def scaling_mA_integer(self, current):
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

    # Scaling 0-10V to 10240
    def scaling_mV_integer(self, voltage):
        voltage_min = 0  # Minimum voltage value in V
        voltage_max = 10  # Maximum voltage value in mV
        integer_min = 0  # Minimum integer value
        integer_max = 10240  # Maximum integer value

        # Calculate the scaling factor
        scaling_factor = (integer_max - integer_min) / (voltage_max - voltage_min)

        # Calculate the mapped integer value
        mapped_integer = integer_min + (voltage - voltage_min) * scaling_factor

        # Round the mapped integer value and convert it to an integer
        mapped_integer = int(round(mapped_integer))

        return mapped_integer

    def scaling_integer_mA(self, integer_value):
        current_min = 4  # Minimum current value in mA
        current_max = 20  # Maximum current value in mA
        integer_min = 0  # Minimum integer value
        integer_max = 1000  # Maximum integer value

        # Calculate the scaling factor
        scaling_factor = (current_max - current_min) / (integer_max - integer_min)

        # Calculate the mapped current value
        mapped_current = current_min + (integer_value - integer_min) * scaling_factor

        return mapped_current

    def scaling_uA_mA(self, current_uA):
        current_min_uA = 0  # Minimum current value in uA
        current_max_uA = 20000  # Maximum current value in uA
        current_min_mA = 0  # Minimum current value in mA
        current_max_mA = 20  # Maximum current value in mA

        # Calculate the scaling factor
        scaling_factor = (current_max_mA - current_min_mA) / (current_max_uA - current_min_uA)

        # Calculate the mapped current value in mA
        current_mA = current_min_mA + (current_uA - current_min_uA) * scaling_factor

        return current_mA






# Example usage:
'''
modbus_vars = modbus_variables()

modbus_module = IOModbusModule("COM1", 9600)  # Replace with your port and baud rate
modbus_module.read_digital_coils(modbus_vars.MOD_16I['start_button'], modbus_vars.MOD_16I['num_registers'], unit=1)
modbus_module.write_digital_coil(modbus_vars.MOD_16I['start_button'], True, unit=1)
modbus_module.write_register(modbus_vars.MOD_16RO['address'], 1234, unit=1)
modbus_module.read_register(modbus_vars.MOD_16RO['address'], modbus_vars.MOD_16RO['num_registers'], unit=1)

modbus_module.close()
'''
