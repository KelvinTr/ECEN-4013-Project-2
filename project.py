import csv
from datetime import datetime

import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055

from machine import Pin, SPI
import sdcard
import os
    

with open("C:/Users/sydno/OneDrive - Oklahoma A and M System/School/4013/P2/GPSdata.csv","w",newline="") as file:
    writer = csv.writer(file,delimiter=',')

    header = ['Date', 'Time', 'Satellites', 'Latitude', 'Longitude', 'Elevation', 'X Accel', 'Y Accel', 'Z Accel', 'X Mag', 'Y Mag', 'Z Mag', 'X Gyro', 'Y Gyro', 'Z Gyro']
    writer.writerow(header)

    
    i2c = I2C(1)  # Device is /dev/i2c-1
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    last_val = 0xFFFF

    def temperature():
        global last_val  # pylint: disable=global-statement
        result = sensor.temperature
        if abs(result - last_val) == 128:
            result = sensor.temperature
            if abs(result - last_val) == 128:
                return 0b00111111 & result
        last_val = result
        return result


    def GPS_Info():
        global NMEA_buff
        global lat
        global longi
        global sat 
        global alt 

        nmea_time = []
        nmea_latitude = []
        nmea_longitude = []
        nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
        nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
        nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
        nmea_satelites = NMEA_buff[6]
        nmea_alt = NMEA_buff[8]
        
        #print("NMEA Time: ", nmea_time,'\n')
        #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
        
        lat = float(nmea_latitude)                  #convert string into float for calculation
        longi = float(nmea_longitude)               #convertr string into float for calculation    
        sat = float(nmea_satelites)
        alt = float(nmea_alt)

    gpgga_info = "$GPGGA,"
    ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
    GPGGA_buffer = 0
    NMEA_buff = 0
    lat = 0
    longi = 0
    sat = 0
    alt = 0 
    

    while True:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info()                                          #get time, latitude, longitude, sat, and alt 

            print("lat: ", lat," long: ", longi, " sat: ", sat, " alt: ", alt, '\n')

            print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
            print("Magnetometer (microteslas): {}".format(sensor.magnetic))
            print("Gyroscope (rad/sec): {}".format(sensor.gyro))
            print()

            now = datetime.now()
            current_date = now.strftime('%m/%d/%Y')
            current_time = now.strftime('%I:%M:%S')
 
            row = [current_date, current_time, sat, lat, longi, alt] #accelerometer, magnetometer, and gyroscope are not entered bc they are not separeated into x, y, and z yet
            writer.writerow(row)

            time.sleep(0.25)

