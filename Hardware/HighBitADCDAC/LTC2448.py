#Written by Daniel Fingerson, 04/23/2020


import spidev
spi=spidev.SpiDev()
spi.open(0,0)
#may need to update speed if it fails to read 
spi.max_speed_hz=1350000

def read(channel,singleOrDif):
    '''Select which channel to read (0-7 for differential, 0-15 for single ended)),
     and whether that should correspond be a single ended or differential reading (0=single, 1=differential)'''
    if singleOrDif==0:
        buf=[singleEnded[channel],0x00,0x00,0x00]
    elif singleOrDif==1:
        buf=[differential[channel],0x00,0x00,0x00]
    else:
        return("Invalid mode identifier: choose either 0 for singleEnded or 1 for differential")
    spi.xfer2(buf0)
    #this conversion was tested by me and is defintely correct 
    rawADC=(((buf[0]&31)<<19) + (buf[1]<<11) + (buf[2]<<3) + ((buf[3]&224)>>5))
    #voltage conversion may be innacurate, but is probably correct 
    #need to determine what Vref is; may be 2.5
    voltage= (rawADC*5)/16777216
    if singleOrDif==0:
        print("Ch {}".format(channel))
        print('{0:.3f} volts'.format( voltages[i]))#prints voltages to 3 decimal place
    else:
        print("Ch {} - Ch{}:".format(channel,channel+1))
        print('{0:.3f} volts'.format( voltage))#prints voltages to 3 decimal place


#wheter single ended or differential, first byte will always start with 101
#differential has the 4th byte be 0,
#thus the first nibble (half byte) input for differential will be A in hex
#and single ended will be B

#although it CAN be coded so that you can choose whether the first pin in each pair of diffenrtial channels
#be either positive or negative, this will almost never be done in practice
#thus, I will only include code so that the first pin is IN+, and the second IN-

differential=[0xA0,0xA1,0xA2,0xA3,0xA4,0xA5,0xA6,0xA7]

#2nd hex values addressing index increases by 1 every other value 
#even index values (beginning) start at 0
#odd index values start at 8
singleEnded=[0xB0,0xB8,0xB1,0xB9,0xB2,0xBA,0xB3,0xBB,
             0xB4,0xBC,0xB5,0xBD,0xB6,0xBE,0xB7,0xBF]




'''TO ADD: THE ability to specify a range of channels to read if the need arrises easily with the proper if/range statement
     better way may be to have a seperate function which does this, and simply envokes this one over a range'''

'''
Comment on input command: 

    for SPI transactions through Python, in order to recieve bytes back,
    additional bytes neeed to be supplied for the xfer2 command 

    
    the logic of this is the following: 


    if the data recieved back is 32 bits long
    and the data to send is a single byte long

    the program should send 4 bytes: the first byte containting the input command
    the rest should be 0
    when the xfer2 transaction is completed, it will replace the 4 bytes with the output
    from here, the program can use bitwise operands to isolate the needed data 



Datasheet information:

Bit 31 is the leading bit (since the last bit is the 0'th bit)


Data output:

    Bits 28 to 5 are the 24-bit conversion result MSB first.
    Bit 5 is the least significant bit (LSB).


Data input:

    In order to change the speed/resolution or input channel, 
    the first 3 bits shifted into the device are 101.

    If the first 3 bits shifted into the device are 101, then the
    following 5 bits select the input channel for the following conversion 

    When an update operation is initiated (the first 3 bits are
    101) the first 5 bits are the channel address. 

    The first bit, SGL, determines if the input selection is differential
    (SGL = 0) or single-ended (SGL = 1). 

    For SGL = 0, two
    adjacent channels can be selected to form a differential
    input. For SGL = 1, one of 8 channels (LTC2444/LTC2445)
    or one of 16 channels (LTC2448/LTC2449) is selected as
    the positive input. The negative input is COM for all single
    ended operations. The remaining 4 bits (ODD, A2, A1,
    A0) determine which channel is selected.





'''