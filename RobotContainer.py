from Drivetrain import Drivetrain
from TTSEngine import TTSEngine
from USBController import USBController
from PWMController import PWMController
from queue import Queue
from SpeechRecognition import SpeechListener

class RobotContainer:

    def __init__(self):
        self.usb_controller = USBController()
        self.drivetrain = Drivetrain(self.usb_controller, 1, 1)
        self.waist = PWMController(0, self.usb_controller)
        self.head_twist = PWMController(3, self.usb_controller)
        self.head_tilt = PWMController(4, self.usb_controller)
        self.bicep_flex = PWMController(6, self.usb_controller)
        self.shoulder_x = PWMController(7, self.usb_controller)
        self.shoulder_y = PWMController(11, self.usb_controller)
        self.gripper = PWMController(8, self.usb_controller)
        self.wrist_flex = PWMController(9, self.usb_controller)
        self.wrist_rotate = PWMController(10, self.usb_controller)
        self.command_queue = Queue()
        #self.speech_listener = SpeechListener()
        #self.speaker = TTSEngine()