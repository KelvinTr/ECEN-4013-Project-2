# ECEN 4013 Project 2
 Create a working GPS tracker with low-level and high-level implementation
 
 Necessary Python Libraries:
 
  A. WiringPi:    \n\n\n\n
          pip3 install wiringpi
  
  B. Adafruit:
          pip3 install adafruit-extended-bus
          pip3 install adafruit-circuitpython-bno055
          
  C. PySerial:
          pip3 install pyserial
 
 

1) Connect All components to Raspberry Pi

![schem](https://user-images.githubusercontent.com/111799321/208063677-26a0e5b8-d65e-42d2-a14e-a31de6ad510d.png)

2) Run "GPSIMU.py" with Python 3 on the RPi

3) Run "USBStream.py" with Python 3 on another Device
NOTE: Change the COM port on the program to match



Acknowledgement, Credit, Reference, More Info:

WiringPi: https://github.com/WiringPi/WiringPi-Python
Adafruit: https://pypi.org/project/adafruit-extended-bus/
          https://github.com/adafruit/Adafruit_CircuitPython_BNO055
PySerial: https://pyserial.readthedocs.io/en/latest/pyserial.html

