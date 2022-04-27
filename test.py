from PWMController import PWMController
from USBController import USBController
def main():

    usb = USBController()

    while True:
        x = input("[Servo number] [position] (q to quit): ")
        if x == 'q':
            exit()
        x = x.split()
        port = int(x[0])
        pos = float(x[1])
        pwm_controller = PWMController(port, usb)
        pwm_controller.set(pos)

if __name__ == "__main__":
    main()