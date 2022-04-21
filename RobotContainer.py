from Drivetrain import Drivetrain
from USBController import USBController
from PWMController import PWMController
from queue import Queue

class RobotContainer:

    def __init__(self):
        self.usb_controller = USBController()
        self.drivetrain = Drivetrain(self.usb_controller, 1, 1)
        self.waist = PWMController(0, self.usb_controller)
        self.head_twist = PWMController(3, self.usb_controller)
        self.head_tilt = PWMController(4, self.usb_controller)
        self.command_queue = Queue()
        #self.speech_recognizer = SpeechRecognition(self.command_queue, self)