import serial
import sys

class USBController:

    def __init__(self):
        try:
            self.usb = serial.Serial('/dev/ttyACM0')
        except:
            try:
                self.usb = serial.Serial('/dev/ttyACM1')
            except:
                print("No servo serial ports found")
                sys.exit(0)

    def sendCmd(self, cmd):
        cmdStr = chr(0xaa) + chr(0x0c) + cmd
        self.usb.write(bytes(cmdStr, 'latin-1'))