#include <avr/io.h>
#include <util/delay.h>
#include <avr/eeprom.h>

#define F_CPU 16000000UL
#define BAUD 2400
#define MYUBRR F_CPU/16/BAUD-1

// Function to initialize UART
void UART_init(unsigned int ubrr) {
    // Set baud rate
    UBRR0H = (unsigned char)(ubrr >> 8);
    UBRR0L = (unsigned char)ubrr;
    // Enable receiver and transmitter
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);
    // Set frame format: 8 data bits, 1 stop bit
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

// Function to transmit a byte
void UART_transmit(unsigned char data) {
    while (!(UCSR0A & (1 << UDRE0))); // Wait for empty transmit buffer
    UDR0 = data; // Send data
}

// Function to receive a byte
unsigned char UART_receive(void) {
    while (!(UCSR0A & (1 << RXC0))); // Wait for data to be received
    return UDR0; // Get and return received data
}

// Function to send a string
void UART_send_string(const char *str) {
    while (*str) {
        UART_transmit(*str++);
    }
}

// Function to store received data into EEPROM
void store_to_eeprom(uint16_t addr, unsigned char data) {
    eeprom_write_byte((uint8_t *)addr, data);
}

// Function to retrieve data from EEPROM
unsigned char read_from_eeprom(uint16_t addr) {
    return eeprom_read_byte((uint8_t *)addr);
}

int main(void) {
    uint16_t eeprom_addr = 0;
    unsigned char received_data;

    UART_init(MYUBRR); // Initialize UART

    // Receive and store data in EEPROM
    while (1) {
        received_data = UART_receive();
        if (received_data == '\0') break; // End of transmission
        store_to_eeprom(eeprom_addr++, received_data);
    }

    // Send data back from EEPROM
    for (uint16_t i = 0; i < eeprom_addr; i++) {
        unsigned char data = read_from_eeprom(i);
        UART_transmit(data);
    }

    return 0;
}
