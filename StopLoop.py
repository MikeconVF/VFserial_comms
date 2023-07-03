#StopLoop.py
def user_stop_module(modbus_module):
    from modbus_var import modbus_variables, Buttons
    import time

    # Create an instance of the modbus_variables class
    modbus_vars = modbus_variables()

    # Access variables from read in data 
    Mod_16I = modbus_vars.MOD_16I['address']
    #start_register = modbus_vars.MOD_16I['STOP_LOOP_1']
    stop_register = modbus_vars.MOD_16I['stop_loop1']

    #acces variable to write out data
    #main pump, assumption that the main pump have been set to NC
    Mod_6RO = modbus_vars.MOD_6RO['address']
    pump_register = modbus_vars.MOD_6RO['m_pump1']
    #injector pump, assumption that correlating defaults are set NC switch
    Mod_16RO = modbus_vars.MOD_16RO['address']
    injector_register = modbus_vars.MOD_16RO['i_pump1']
    warning_lamp_register = modbus_vars.MOD_16RO['warning_light1']
    #system lamp, assumption that correlating defaults are set NC switch
    system_register = modbus_vars.MOD_16RO['system_indicator']
    

    # Read stop
    stop_list = modbus_module.read_digital_coils(stop_register, 5, Mod_16I)

    if any(stop_list):
        print("There is at least one True value in the stop_list.")
        # Find the indices of all True values
        true_indices = [index for index, value in enumerate(stop_list) if value]
        print("Indices of True values:", true_indices)
        for index in true_indices:
            #main pump
            modbus_module.write_register(pump_register+index, True, Mod_6RO)
            #injector pump
            modbus_module.write_register(injector_register+index, False, Mod_16RO)
            #warning lamp
            modbus_module.write_register(warning_lamp_register +index, True, Mod_16RO)
        
        modbus_module.write_register(system_register, True, Mod_16RO)
    if not all (stop_list):
        stop_state=False
        return stop_state
    
