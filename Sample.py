from modbus_var import modbus_variables

modbus_vars = modbus_variables()

start_register = modbus_vars.MOD_8AO['start_register']
num_registers = modbus_vars.MOD_8AO['num_registers']
current_value = modbus_vars.MOD_8AO['current_value']
voltage_value = modbus_vars.MOD_8AO['voltage_value']

print(start_register)
print(num_registers)
print(current_value)
print(voltage_value)


        if r_value == 6:
