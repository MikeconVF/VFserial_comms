def start_loop_module(modbus_module):
    from modbus_var import modbus_variables, Buttons
    import time

    # Create an instance of the modbus_variables class
    modbus_vars = modbus_variables()

    # Access variables from MOD_16I
    Mod_16I = modbus_vars.MOD_16I['address']
    start_register = modbus_vars.MOD_16I['start_button']
    stop_register = modbus_vars.MOD_16I['stop_loop1']

    # Read start
    PB_list = modbus_module.read_digital_coils(start_register,1, Mod_16I)
    start_B = PB_list[Buttons.START_BUTTON]

    #main pump switch address
    Mod_6RO = modbus_vars.MOD_6RO['address']
    main_pump = modbus_vars.MOD_6RO['m_pump1']
    num_pump = modbus_vars.MOD_6RO['num_registers']

    #AI board register
    #mainly for testing
    Mod_8AI = modbus_vars.MOD_8AI['address']
    spoof_value = modbus_vars.MOD_8AI['spoof_EC_meter']
    num_signal = 2 #modbus_vars.MOD_8AI['num_registers']

    start_button_latched=False

    # Read stop
    stop_list = modbus_module.read_digital_coils(stop_register, 5, Mod_16I)

    #latch start button signal
    if start_B and not start_button_latched:
        start_button_latched = True
        reset_button_latched = False

    if start_button_latched and not all (stop_list):
        #turn on the all main pump
        for i in range(num_pump):
            modbus_module.write_register(main_pump+i, True, Mod_6RO)

        m_pump_list = modbus_module.read_digital_coils(main_pump, 5, Mod_16I)
        false_indices = [index +1 for index, value in enumerate(m_pump_list) if not value]
        #error finding for main pump
        if not any(m_pump_list):
            raise ValueError(f"Main pump: {false_indices} not working")

        #Poll AI Board Voltage register
        signal_list = modbus_module.read_register(spoof_value, num_signal, Mod_8AI)

    return signal_list





#need to preset default of MOD_16RO NC switches
