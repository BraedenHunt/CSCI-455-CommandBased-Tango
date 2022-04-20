from PWMController import PWMController
from USBController import USBController


class Drivetrain:

    def __init__(self, usb_controller: USBController, max_speed, max_accel):
        self.leftPower = 0
        self.rightPower = 0
        self.usb_controller = usb_controller
        self.MAX_SPEED = max_speed
        self.MAX_ACCELERATION = max_accel
        self.right_motor: PWMController = PWMController(1, self.usb_controller)
        self.left_motor: PWMController = PWMController(2, self.usb_controller)

    def drive(self, left: float, right: float):
        self.leftPower = left
        self.rightPower = right

    def update(self):
        self.left_motor.set(self.bound(self.leftPower, -1, 1))
        self.right_motor.set(self.bound(self.rightPower, -1, 1))

    @classmethod
    def bound(cls, value: float, min_value: float, max_value: float):
        return max(min(max_value, value), min_value)
