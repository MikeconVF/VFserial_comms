#default_Preset.py

def Default_Preset_Value(modbus_module):
    from modbus_var import modbus_variables, Buttons

    # Create an instance of the modbus_variables class
    modbus_vars = modbus_variables()

    #injector pump,set defaults are set NC switch
    Mod_16RO = modbus_vars.MOD_16RO['address']
    injector_state = modbus_vars.MOD_16RO['i_state1']
    system_register = modbus_vars.MOD_16RO['NC_switch1']

    #main pump switch address
    Mod_6RO = modbus_vars.MOD_6RO['address']
    main_pump = modbus_vars.MOD_6RO['m_pump1']
    num_pump = modbus_vars.MOD_6RO['num_registers']


    modbus_module.write_register(system_register, True, Mod_16RO)

    # Read stop default state
    stop_list = modbus_module.read_digital_coils(injector_state, 5, Mod_16RO)

    if not any(stop_list):
        false_indices = [index for index, value in enumerate(stop_list) if value]
        for index in false_indices:
            #injectorpump
            modbus_module.write_register(injector_state+index, True, Mod_16RO)
    #turn off Main pump
    for i in range(num_pump):
        modbus_module.write_register(main_pump+i, False, Mod_6RO)

    

    
