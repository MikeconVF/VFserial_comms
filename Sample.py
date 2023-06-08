from pymodbus.client.sync import ModbusSerialClient

# Create a Modbus serial client
client = ModbusSerialClient(
    method='rtu', 
    port='COM8',  # Replace with the appropriate serial port for your adapter
    baudrate= 115200,  # Set the baud rate of your serial communication
    parity='N',  # Set the parity as required
    stopbits=1,  # Set the stop bits as required
    bytesize=8  # Set the data bits as required
)

# Open the Modbus serial connection
if client.connect():
    print("Modbus serial connection opened successfully.")

    # Perform Modbus communication operations here
    # For example, you can read holding registers using client.read_holding_registers() or write coils using client.write_coil()

    # Close the Modbus serial connection
    client.close()
    print("Modbus serial connection closed.")
else:
    print("Failed to open the Modbus serial connection.")
