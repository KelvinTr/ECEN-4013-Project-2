import serial 
import sys
import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import csv
from datetime import datetime
import wiringpi

wiringpi.wiringPiSetup() 
wiringpi.pinMode(2, 1)
wiringpi.digitalWrite(2, 0)

i2c = I2C(1)  # Device is /dev/i2c-1
sensor = adafruit_bno055.BNO055_I2C(i2c)
ser0 = serial.Serial("/dev/ttySC0", 9600)

gpgga_info = "$GPGGA,"
ser1 = serial.Serial ("/dev/ttyACM0", 9600)              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
numSatellites = 0
elevation = 0.0

ser2 = serial.Serial("/dev/ttySC1", baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    global numSatellites
    global elevation
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    numSatellites = NMEA_buff[6]
    elevation = NMEA_buff[8]
    
    
    if nmea_latitude == "":
        if  nmea_longitude == "":
            return
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.8f" %(position)
    return position
    


now = "/media/pi/GPS_SD/" + str(datetime.now()) + ".csv"
fileSD = now.replace(":", ",")
print(fileSD)
with open(fileSD, 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Latitude', 'Longitude', 'Elevation', 'Number of Satellites Locked','Angular Velocity', 'Acceleration', 'Magnetic Field']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    while True:
        accel = sensor.acceleration
        mag = sensor.magnetic
        gyro = sensor.gyro
        current_time = datetime.now()
        ctime = current_time.strftime("%H:%M:%S")
        
        received_data = (str)(ser1.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string      
        time.sleep(1)           
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info()                                          #get time, latitude, longitude
            

        if(int(numSatellites) > 0):
            wiringpi.digitalWrite(2, 1)
        else:
            wiringpi.digitalWrite(2, 0)
            print("No Locked Satellites.")

        print("Time: {}".format(ctime))
        print("Latitude: {}".format(lat_in_degrees))
        print("Longitude: {}".format(long_in_degrees))
        print("Elevation: {}".format(elevation))
        print("Number of Satellites: {}".format(numSatellites))
        print("Gyroscope (rad/sec): {}".format(gyro))
        print("Accelerometer (m/s^2): {}".format(accel))
        print("Magnetometer (uT): {}".format(mag))
        print()


        latStr = ("Latitude: {}".format(lat_in_degrees))
        ser0.write(bytes(latStr, 'utf-8'))
        ser2.write(bytes(latStr, 'utf-8'))
        ser0.write(b"\n")
        ser2.write(b"\n")

        longStr = ("Longitude: {}".format(long_in_degrees))
        ser0.write(bytes(longStr, 'utf-8'))
        ser2.write(bytes(longStr, 'utf-8'))
        ser0.write(b"\n")
        ser2.write(b"\n")

        eleStr = ("Elevation: {}".format(elevation))
        ser0.write(bytes(eleStr, 'utf-8'))
        ser2.write(bytes(eleStr, 'utf-8'))
        ser0.write(b"\n")
        ser2.write(b"\n")

        satStr = ("Number of Satellites: {}".format(numSatellites))
        ser0.write(bytes(satStr, 'utf-8'))
        ser2.write(bytes(satStr, 'utf-8'))
        ser0.write(b"\n")
        ser2.write(b"\n")


        gyroStr = ("Gyroscope (rad/sec): {}".format(gyro))
        ser0.write(bytes(gyroStr, 'utf-8'))
        ser2.write(bytes(gyroStr, 'utf-8'))
        ser0.write(b"\n")
        ser2.write(b"\n")
        
        accelStr = ("Accelerometer (m/s^2): {}".format(accel))
        ser0.write(bytes(accelStr, 'utf-8'))
        ser2.write(bytes(accelStr, 'utf-8'))
        ser0.write(b"\n")
        ser2.write(b"\n")

        magStr = ("Magnetometer (uT): {}".format(mag))
        ser0.write(bytes(magStr, 'utf-8'))
        ser2.write(bytes(magStr, 'utf-8'))
        ser0.write(b"\n\n")
        ser2.write(b"\n\n\n")

        writer.writerow({'Time': ctime,'Latitude': lat_in_degrees,'Longitude': long_in_degrees,'Elevation': elevation,'Number of Satellites Locked': numSatellites,'Angular Velocity': gyro, 'Acceleration': accel, 'Magnetic Field': mag})
        time.sleep(2)