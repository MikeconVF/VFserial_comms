#modbus_var.py

from enum import IntEnum

class Buttons(IntEnum):
    START_BUTTON = 0
    BLEED_BUTTON = 1
    RESET_BUTTON = 2
    STOP_LOOP_1 = 3
    STOP_LOOP_2 = 4
    STOP_LOOP_3 = 5
    STOP_LOOP_4 = 6
    STOP_LOOP_5 = 7
    WATER_LEVEL_SENSOR = 8
    M_PUMP1 = 9
    TEST_BUTTON = 15



class modbus_variables:
    MOD_16I = {
        # Specify the Modbus address
        'address': 1,                   # Replace with your Modbus device's address

        # Read digital input register = register address-1
        'start_button':800, 
        'bleed_button':801, 
        'reset_button':802, 
        'stop_loop1': 803,
        'stop_loop2': 804,
        'stop_loop3': 805,
        'stop_loop4': 806,
        'stop_loop5': 807,
        'water_level_sensor': 808,
        'm_pump1':809,
        'm_pump2':809,
        'm_pump3':809,
        'm_pump4':809,
        'm_pump5':809,
        'test_button':815,

        # Read holding register
        'r_baudrate':2,

        'num_registers': 16,

        # Variables for latch functionality
        'start_button_latched': False,
        'PB_reset': False
    }

    MOD_8AI = {
        # Specify the Modbus slave address
        'address': 2,                   # Replace with your Modbus device's slave address

        # Read discrete register. register address 30053
        'flow_meter1': 55,                      #flow meter 4-20mA
        'flow_meter2': 56,                      #flow meter 0-10000mv
        'flow_meter3': 57,                      #flow meter 0-10000mv
        'flow_meter4': 58,                      #flow meter 0-10000mv
        'flow_meter5': 59,                      #flow meter 0-10000mv
        'EC_meter': 52,                         #EC meter 4-20mA
        'injector_pump_read': 58,               #injectector pump 4-20mA

        'num_registers': 8,                     #1 free analogue read

        # Set output value
        'current_valueAI': 14,
        'voltage_valueAI': 5
    }


    #first 4 analogue output is broken.
    MOD_8AO = {
        # Specify the Modbus slave address
        'address': 3,                           # Replace with your Modbus device's slave address

        # write output register for 0-10000mv



        'injector_pump1': 56,                   #injector pump1 4-20mA signal
        'injector_pump2': 57,                   #injector pump2 4-20mA signal
        'spoof_EC_meter': 58,             #will change to injector pump once testing is done
        'spoof_flow_meter1': 52,                #Voltage will change to injector pump once testing is done
        'num_registers': 4,                     

        # Set output value
        'current_value': 14,
        'voltage_value': 5
    }


    MOD_16RO = {
        #watchdog: 40009 modbus register, 8 dec. set default to 0.
        
        'address': 4,

        #number of default register
        'num_def_registers': 6,  

        #set default state to true, for NC switch. otherwise normal default set to false.
        #write coil dec register set up to true for NC switch
        'i_state1': 199,                   #default NC state of injector pump 1
        'i_state2': 200,                   #default NC state of injector pump 2
        'i_state3': 201,                   #default NC state of injector pump 3
        'i_state4': 202,                   #default NC state of injector pump 4
        'i_state5': 203,                   #default NC state of injector pump 5
        'NC_switch1': 197,              #NC Relay for external on/off functionality

        #number of output register
        'num_registers': 12,  
        
        #write coil register, output
        'warning_light1':816,           #warning light1 switch, output 1
        'warning_light2':817,           #warning light2 switch, output 2
        'warning_light3':818,           #warning light3 switch, output 3
        'warning_light4':819,           #warning light4 switch, output 4
        'warning_light5':820,           #warning light5 switch, output 5
        'system_indicator':821,         #NC switch for external on/off, output 6
        'flush_lamp':822,               #NO switch, output 7
        #output 9 not worki dec adress=824
        'i_pump1':827,                   #NCinjector pump1 switch, output 12
        'i_pump2':828,                   #NCinjector pump2 switch, output 13
        'i_pump3':829,                   #NCinjector pump3 switch, output 14
        'i_pump4':830,                   #NCinjector pump4 switch, output 15
        'i_pump5':831                    #NCinjector pump5 switch, output 16

    }

    #from panel lights and switches.pdf
    MOD_6RO = {
        #watchdog: 40009 modbus register, 8 dec. set default to 0.

        'address': 5,

        'num_registers': 5,  

        # write coil dec register
        'm_pump1': 816,                 # set relay to NC for main pump1
        'm_pump2': 817,                 # set relay to NC for main pump1
        'm_pump3': 818,                 # set relay to NC for main pump1
        'm_pump4': 819,                 # set relay to NC for main pump1
        'm_pump5': 820,                 # set relay to NC for main pump1


    }
