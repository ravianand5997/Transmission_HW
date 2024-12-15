import serial
import time
import threading

# Configuration for COM ports
PC_TO_MCU_PORT = "COM3"
MCU_TO_PC_PORT = "COM4"
BAUD_RATE = 2400
DATA_TEXT = (
    "Finance Minister Arun Jaitley Tuesday hit out at former RBI governor "
    "Raghuram Rajan for predicting that the next banking crisis would be "
    "triggered by MSME lending, saying postmortem is easier than taking action "
    "when it was required..."
)

# Simulate MCU behavior
def mcu_simulation():
    with serial.Serial(PC_TO_MCU_PORT, BAUD_RATE, timeout=1) as mcu_receive, \
         serial.Serial(MCU_TO_PC_PORT, BAUD_RATE, timeout=1) as mcu_send:
        print("MCU: Ready to receive data...")
        eeprom_simulation = []

        # Receive data from PC and store in simulated EEPROM
        while True:
            byte = mcu_receive.read(1)
            if byte == b'\0':  # End of transmission
                break
            if byte:
                eeprom_simulation.append(byte)

        print("MCU: Data received and stored in EEPROM simulation.")
        
        # Send data back from EEPROM simulation
        for data_byte in eeprom_simulation:
            mcu_send.write(data_byte)
            time.sleep(0.001)  # Simulate delay

        print("MCU: Data sent back to PC.")

# PC-side logic
def pc_side():
    with serial.Serial(PC_TO_MCU_PORT, BAUD_RATE, timeout=1) as pc_send, \
         serial.Serial(MCU_TO_PC_PORT, BAUD_RATE, timeout=1) as pc_receive:
        # Send data to MCU
        print("PC: Sending data to MCU...")
        start_send_time = time.time()
        for char in DATA_TEXT:
            pc_send.write(char.encode())
            time.sleep(0.001)  # Simulate realistic send speed
        pc_send.write(b'\0')  # Signal end of transmission
        end_send_time = time.time()

        # Calculate transmission speed
        send_speed = (len(DATA_TEXT) * 8) / (end_send_time - start_send_time)
        print(f"PC: Data sent at {send_speed:.2f} bits/second.")

        # Receive data back from MCU
        print("PC: Receiving data from MCU...")
        received_data = []
        start_receive_time = time.time()
        while True:
            byte = pc_receive.read(1)
            if not byte:
                break
            received_data.append(byte.decode())
        end_receive_time = time.time()

        # Calculate reception speed
        receive_speed = (len(received_data) * 8) / (end_receive_time - start_receive_time)
        print(f"PC: Data received at {receive_speed:.2f} bits/second.")
        print("PC: Received data:\n", "".join(received_data))

if __name__ == "__main__":
    # Use threading to simulate MCU and PC running simultaneously
    mcu_thread = threading.Thread(target=mcu_simulation)
    mcu_thread.start()

    time.sleep(1)  # Allow MCU simulation to initialize
    pc_side()

    mcu_thread.join()
