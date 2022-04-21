from Drivetrain import Drivetrain
from USBController import USBController
from PWMController import PWMController

class RobotContainer:

    def __init__(self):
        self.usb_controller = USBController()
        self.drivetrain = Drivetrain(self.usb_controller, 1, 1)
        self.waist = PWMController(0, self.usb_controller)
        self.head_twist = PWMController(3, self.usb_controller)
        self.head_tilt = PWMController(4, self.usb_controller)