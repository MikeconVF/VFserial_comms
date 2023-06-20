class modbus_variables:
    MOD_16I = {
        # Specify the Modbus address
        'address': 0,  # Replace with your Modbus device's address

        # Read digital input register = register address-1
        'start_button':800, 
        'stop_button':801, 
        'bleed_button':802, 
        'reset_button':803, 
        'reset_button':803, 

        # Read holding register
        'r_baudrate':2,

        'num_registers': 16,

        # Variables for latch functionality
        'start_button_latched': False,
        'PB_reset': False
    }

    MOD_8AO = {
        # Specify the Modbus slave address
        'address': 3,  # Replace with your Modbus device's slave address

        # Read holding register 40003S
        'start_register': 52,
        'num_registers': 8,

        # Set output value
        'current_value': 14,
        'voltage_value': 5
    }
