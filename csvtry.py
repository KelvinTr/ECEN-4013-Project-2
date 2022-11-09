

'''
SD CARD  
'''
import csv
from datetime import datetime

# Create / Open a file in write mode.
# Write mode creates a new file.
# If  already file exists. Then, it overwrites the file.
    
with open("C:/Users/sydno/OneDrive - Oklahoma A and M System/School/4013/P2/GPSdata.csv","w",newline="") as file:
    writer = csv.writer(file,delimiter=',')

    header = ['Date', 'Time', 'Satellites', 'Latitude', 'Longitude', 'Elevation', 'X Accel', 'Y Accel', 'Z Accel', 'X Mag', 'Y Mag', 'Z Mag', 'X Gyro', 'Y Gyro', 'Z Gyro']
    writer.writerow(header)


    i=0
    while i<5:
            now = datetime.now()
            current_date = now.strftime('%m/%d/%Y')
            current_time = now.strftime('%I:%M:%S')
            row = [current_date, current_time, 'Satellites', 5, 3]
            writer.writerow(row)
            i=i+1
                            
    

# Open the file in "read mode". 
# Read the file and print the text on debug port.
file = open("C:/Users/sydno/OneDrive - Oklahoma A and M System/School/4013/P2/GPSdata.csv", "r")
if file != 0:
    print("Reading from SD card")
    read_data = file.read()
    print (read_data)
file.close()

