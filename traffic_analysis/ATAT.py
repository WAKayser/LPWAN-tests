import serial
from time import sleep, localtime
import datetime
from random import choices
import string
from math import floor
# Commands are sometimes send directly instead of with sendCommand
# to have better control of the output of the command
# Precise AT command are not documented. But that is tradition in AT commands.


# Current status of device
device = {'RAT': 7, 'port': 'COM5', 'dBm': 'NaN'}

# Determination of RAT type
RATs = {7: 'LTE-M', 8: "NB-IoT"}


# Reopens the port for every command. This means that other programs can also
# use it.
# IT also protects from short disconnects.
def sendCommand(command):
    with serial.Serial(device['port'], 115200, timeout=1) as ser:
        if command != 'read':
            ser.write(command.encode() + b'\r')
        while(True):
            buff = ser.readline()
            if buff == b'':
                break
            else:
                print(buff.decode(), end='')


# Opens a socket from a randomly chosen port.
def setupSocket():
    sendCommand('AT+USOCL=0')
    sendCommand('AT+USOCR=17,1463')


# Decodes the Signal Quality value into RSSI
def findRSSI(quiet=True):
    global device
    with serial.Serial(device['port'], 115200, timeout=1) as ser:
        ser.write('AT+CSQ'.encode() + b'\r')
        ser.readline()
        RSSI = int(ser.readline().split()[1].split(b',')[0])
        if RSSI == 99:
            dBm = 'NaN'
        else:
            dBm = -113 + (2*RSSI)
        if not quiet:
            print(f'Current RSSI is {dBm} dBm')
        device['dBm'] = dBm
        ser.reset_input_buffer()


# Finds the RAT that the device is currently using
def findRAT(quiet=True):
    global device
    with serial.Serial(device['port'], 115200, timeout=1) as ser:
        ser.write('AT+URAT?'.encode() + b'\r')
        ser.readline()
        rat = int(ser.readline().split()[1])
        if not quiet:
            print(f'Current RAT is {RATs[rat]}')
        device['RAT'] = rat
        ser.reset_input_buffer()


# Turns out it is relatively easy to switch RAT.
# Most devices support this and all Sims from Vodafone support it.
def switchRAT(rat):
    global device
    sendCommand('AT+USOCL=0')
    sendCommand(f'AT+URAT={rat}')
    sendCommand('AT+CFUN=15')
    print('waiting to reset')
    sleep(4)
    if int(rat) == 8:
        sendCommand('AT+CEREG=2')
        print('Extra wait for NB-IoT')
        sleep(9)
    elif int(rat) == 7:
        sendCommand('AT+CEREG=3')
    sleep(1)
    sendCommand('AT+USOCR=17,1463')
    device['RAT'] = int(rat)


# Send some random data. This will then still be encapsulated in an UDP packet
# Which adds an extra 8 bytes
def sendData(dataSize):
    data = ''.join(choices(string.ascii_uppercase + string.digits, k=dataSize))
    sendCommand(f'AT+USOST=0,\"80.112.163.254\",1463,{dataSize},\"{data}\"')
    month = localtime().tm_mon
    day = localtime().tm_mday
    hour = localtime().tm_hour
    quarter = floor(localtime().tm_min / 15)
    with open("autotest.log", 'a') as log:
        log.write(f'{month}\t{day}\t{hour}\t{quarter}'
                  f'\t{dataSize}\t{device["RAT"]}\n')


# Test based on the time of day
def autoTest(count):
    while(count):
        hour = localtime().tm_hour
        dt = datetime.datetime.today()
        day = dt.day
        if day == 7:
            size = 64 * (hour - 11)
        elif day == 8:
            size = 768 + (64 * hour)
        sendData(size)
        quarter = floor(localtime().tm_min / 15)
        if quarter == 0:
            print('First quarter is empty')
            sleep((15-localtime().tm_min) * 60)
        else:
            wait = 15 * 60 / (2**quarter)
            sleep(wait)

        count -= 1


# Increases volume per 15 minutes.
def rampTest():
    for size in [128, 256, 512, 768, 1024]:
        for repetition in [1, 2, 4, 8, 16]:
            if repetition == 1:
                sendData(size)
                sleep((15-(localtime().tm_min % 15)) * 60)
            else:
                for x in range(repetition):
                    sendData(size)
                    sleep((15 * 60 / repetition) - 5)


# Smaller easier repeat test.
def repeatTest(command):
    wait, size, count = [int(x) for x in command]
    while(count):
        sendData(size)
        sleep(wait)
        count -= 1


#  Prints a prompt so that one of the functions can be called
# Or so that an AT Command can be sent.
def main():
    print("Welcome to AT-AT: Automated Tester for AT devices.")
    global device
    port = input("Port (COM5): ")
    if port:
        device['port'] = port
    findRAT()
    while(True):
        findRSSI()
        command = input(f"RSSI: {device['dBm']} ||"
                        f" RAT: {RATs[device['RAT']]} || CMD: ")
        if command == '':
            continue
        splat = command.split()
        if splat[0] == 'stop':
            break
        elif splat[0] == 'send':
            sendData(int(splat[1]))
        elif splat[0] == 'setup':
            setupSocket()
        elif splat[0] == 'auto':
            autoTest(int(splat[1]))
        elif splat[0] == 'at':
            sendCommand(splat[1])
        elif splat[0] == 'repeat':
            repeatTest(splat[1:])
        elif splat[0] == 'rat':
            if len(splat) == 1:
                findRAT(quiet=False)
            else:
                switchRAT(splat[1])
        elif splat[0] == 'rssi':
            findRSSI(quiet=False)
        elif splat[0] == 'ramp':
            rampTest()
        else:
            print("did not understand command")


if __name__ == '__main__':
    main()
