import serial
import time

serTester = serial.Serial('COM6')

serTester.baudrate = 9600
serTester.bytesize = 8
serTester.parity = 'N'
serTester.stopbits = 1

time.sleep(1)

while 1:
    rx_data = serTester.readline()
    print(rx_data.decode())

serTester.close()