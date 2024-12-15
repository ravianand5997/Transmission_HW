import serial
import time

# Constants
COM_PORT = "COM3"  # Update this based on your com0com setup
BAUD_RATE = 2400
TEXT = (
    "Finance Minister Arun Jaitley Tuesday hit out at former RBI governor "
    "Raghuram Rajan for predicting that the next banking crisis would be "
    "triggered by MSME lending, saying postmortem is easier than taking action "
    "when it was required..."
)

def calculate_speed(start_time, end_time, data_size):
    elapsed_time = end_time - start_time
    return (data_size * 8) / elapsed_time if elapsed_time > 0 else 0

def main():
    with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
        print("Sending data to MCU...")
        start_time = time.time()

        # Send text to MCU
        for char in TEXT:
            ser.write(char.encode())
            time.sleep(0.001)  # Simulate slower send for better visualization
        ser.write(b'\0')  # End transmission signal

        end_time = time.time()
        transmission_speed = calculate_speed(start_time, end_time, len(TEXT))
        print(f"Data sent at {transmission_speed:.2f} bits/second")

        print("\nReceiving data from MCU...")
        received_data = ""
        start_time = time.time()

        while True:
            byte = ser.read(1)
            if not byte:
                break
            received_data += byte.decode()

        end_time = time.time()
        reception_speed = calculate_speed(start_time, end_time, len(received_data))
        print(f"Data received at {reception_speed:.2f} bits/second")
        print("Received data:\n", received_data)

if __name__ == "__main__":
    main()
