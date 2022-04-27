from PWMController import PWMController
from USBController import USBController
def main():

    usb = USBController()

    while True:
        x = input("Servo number [q to quit]: ")
        if x == 'q':
            exit()
        x = int(x)
        pwm_controller = PWMController(x, usb)
        y = input("Position: ")
        y = int(y)
        pwm_controller.set(y)

if __name__ == "__main__":
    main()