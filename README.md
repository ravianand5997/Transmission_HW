# Transmission_HW


Approach 1: PC and MCU Code
This approach uses two separate pieces of code:

PC Side Code (C/C++/python)
MCU Firmware (Embedded C/C++)
PC to MCU Transmission
PC Code:

The PC program reads the given text and sends it byte-by-byte over a UART serial port to the MCU.
It uses a serial communication library (e.g., serial in Python for simulation) to open the COM port and transfer data.
The data transmission speed is calculated in real-time by dividing the number of bits transmitted by the elapsed time.
MCU Firmware:

The MCU code continuously listens for data on its UART receive pin.
As the MCU receives data, it stores each byte into the EEPROM. This process is done byte-by-byte since the EEPROM is slow and cannot handle high-speed bulk writes.
The MCU code monitors the speed of data reception and prints it to the UART console (to be received on the PC for debugging).
MCU to PC Transmission
After receiving all data from the PC:

The MCU starts sending the stored text from EEPROM back to the PC via UART.
The MCU reads the data byte-by-byte from EEPROM and sends it over UART.
The MCU measures the speed of transmission and prints it for monitoring.
PC Code:

The PC program now reads data coming from the MCU.
The received data is printed to the console.
The program also calculates the real-time data reception speed.
Summary
Advantages:
This mimics real hardware interactions, making it realistic for firmware testing.
It involves both UART transmission and EEPROM handling.
Disadvantages:
Requires physical hardware (MCU).
Debugging hardware-related issues can be tricky without actual tools.




Approach 2: Alternative Python Simulation
This approach eliminates the need for hardware (MCU) by simulating the entire system on a Windows PC using virtual COM ports.

How It Works
Virtual COM Ports:

We use com0com to create a pair of linked virtual COM ports (e.g., COM3 and COM4).
Data sent to COM3 is automatically forwarded to COM4 and vice versa, simulating UART communication.
PC Simulation for Both Sides:

Two threads (or processes) represent the PC and MCU sides:
PC Side: Sends the text to COM3 and listens on COM4 for the response.
MCU Side: Reads data from COM3, stores it in a simulated memory buffer (mimicking EEPROM), and then sends it back via COM4.
Text Transmission:

The first thread (PC) writes the text to COM3.
The second thread (MCU simulation) reads data from COM3 byte-by-byte, stores it in a Python list (as EEPROM), and then sends it back to COM4.
Speed Calculation:

The speed of transmission is calculated by:
Counting the bits transmitted/received.
Measuring the time taken for the operation.
This is done dynamically for both transmission and reception, and the results are displayed live.
Why This Works Without Hardware
The virtual COM ports simulate UART communication, allowing us to test serial communication without an actual MCU.
Instead of real EEPROM, a Python list is used to store the data.
Summary
Advantages:
No physical hardware required.
Fully testable and debuggable on a single PC.
Quicker setup and debugging.
Disadvantages:
Does not replicate MCU-level constraints like limited EEPROM write cycles or real UART timing.
