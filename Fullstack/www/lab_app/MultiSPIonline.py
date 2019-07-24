#have either read or select return something indicating reading failed inorder to display alternate html page
import spidev
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def read():
    raw_adc=[0,0,0,0]
    voltages=[0,0,0,0]
    spi2=spidev.SpiDev()
    spi2.open(0,0)
    spi2.max_speed_hz=1350000
    buf=[[ 0x01, 0x00, 0x00],[ 0x01, 0x20, 0x00],[ 0x01, 0x40, 0x00],[ 0x01, 0x60, 0x00]]
    spi2.xfer2(buf[0])
    spi2.xfer2(buf[1])
    spi2.xfer2(buf[2])
    spi2.xfer2(buf[3])
    for i in range(4):
        raw_adc[i]=((buf[i][1] &3)<<8) +buf[i][2] #converts last 10 bits of data into an ADC reading
        voltages[i]=(raw_adc[i]*5)/1023 #converts ADC reading into a voltage
        #print("Ch {} - Ch{}:".format(i,i+1))
        #print('{0:.3f} volts'.format( voltages[i]))#prints voltages to 3 decimal place
    return voltages

def select(device):
    """Select the SPI device to communicate with; Device index begins at 0 in hexedecimal and goes up to F; 0-9 should be entered as ints,
while A-F should be strings"""
    buf=[[0x00],[0x01],[0x02],[0x03],[0x04],[0x05],[0x06],[0x07],[0x08],[0x09],[0x0A],[0x0B],[0x0C],[0x0D],[0x0E],[0x0F]]
    spi1=spidev.SpiDev()
    spi1.open(0,1) #select channel 1, bus 0
    spi1.max_speed_hz=1350000 #clock speed that facilitates transactions (recomended clock speed for MCP3008)
    if device==0:
        spi1.xfer(buf[0])
        #print("Device 0 selected")
    elif device==1:
        spi1.xfer2(buf[1])
        print("Device 1 selected")
    elif device==2:
        spi1.xfer(buf[2])
        print("Device 2 selected")
    elif device==3:
        spi1.xfer2(buf[3])
        print("Device 3 selected")
    elif device==4:
        spi1.xfer(buf[4])
        print("Device 4 selected")
    elif device==5:
        spi1.xfer2(buf[5])
        print("Device 5 selected")
    elif device==6:
        spi1.xfer(buf[6])
        print("Device 6 selected")
    elif device==7:
        spi1.xfer2(buf[7])
        print("Device 7 selected")
    elif device==8:
        spi1.xfer(buf[8])
        print("Device 8 selected")
    elif device==9:
        spi1.xfer2(buf[9])
        print("Device 9 selected")
    elif device=="A" or "a":
        spi1.xfer(buf[10])
        print("Device A selected")
    elif device=="B" or "b":
        spi1.xfer2(buf[11])
        print("Device B selected")
    elif device=="C" or "c":
        spi1.xfer(buf[12])
        print("Device C selected")
    elif device=="D" or "d":
        spi1.xfer2(buf[13])
        print("Device D selected")
    elif device=="E" or "e":
        spi1.xfer(buf[14])
        print("Device E selected")
    elif device=="F" or "f":
        spi1.xfer2(buf[15])
        print("Device F selected")
