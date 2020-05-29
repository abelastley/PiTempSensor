import glob
import time
import os.path
from os import path
from datetime import datetime

# TODO: configure the following parameters
temperature_data_file = "./TemperatureData.csv"
intervalTime = 5 # seconds



# find out how many sensors we have

base_dir = '/sys/bus/w1/devices/'
numSensors = len(glob.glob(base_dir + '28*'))
print("found %s sensors" %numSensors)


# if the data file does not exist, initialize it
if(path.exists(temperature_data_file) != True):
    print("Output file does not exist. Creating new one...\r\n")
    try:
        outputFile = open(temperature_data_file, "w")
        outputFile.write("Date and Time,")
        for n in range(0, numSensors):
            outputFile.write("Sensor %s Reading (degrees F)," %n)
        outputFile.write("\r\n")
        outputFile.close()
    except:
        print "Error occurred while creating or writing to file: " + temperature_data_file, sys.exc_info[0]
else:
    print("Output file exists. Appending new data to it...\r\n")



def read_temp_raw(sensorIndex):
    f = open(glob.glob(base_dir + '28*')[sensorIndex] + '/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensorIndex):
    lines = read_temp_raw(sensorIndex)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(sensorIndex)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def read_temps_and_write_file():
    try:
        outputFile = open(temperature_data_file, "a")
        now = datetime.now()
        dateTimeString = datetime.strftime(now, "%m/%d/%Y %H:%M:%S")
        outputFile.write(dateTimeString + ",")
        
        for n in range(0, numSensors):
            deg_c, deg_f = read_temp(n)
            print("Sensor %s" %n)
            print("temperature %s" %deg_f)
            outputFile.write("%s," %deg_f)
        
        outputFile.write("\r\n")
        outputFile.close()
    except:
        print "Error occurred while appending to file: " + temperature_data_file, sys.exc_info[0]



# TODO: uncomment ONLY 1 of the option blocks below, A or B



####################### Option A ##########################################
#
# uncomment these lines if you want to call the python script only once,
# for example, upon power on or upon login.  The script will run forever
# until it is killed.


#while True:
#    read_temps_and_write_file()    
#    time.sleep(intervalTime)

#########################################################################



    
###################### Option B #############################################
#
# uncomment these lines if you want to schedule the python script to be
# called periodically, for example, with cron.  The script will take 1
# temperature reading per sensor, and then exit

read_temps_and_write_file()


#########################################################################










