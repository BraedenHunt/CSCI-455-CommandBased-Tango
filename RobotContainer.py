from Drivetrain import Drivetrain
from USBController import USBController


class RobotContainer:

    def __init__(self):
        self.usb_controller = USBController()
        self.drivetrain = Drivetrain(self.usb_controller, 1, 1)