from Drivetrain import Drivetrain
from ServoCommand import ServoCommand
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
        self.speech_listener = SpeechListener()
        #self.speaker = TTSEngine()

    def add_slash_commands(self):
        inner_delay = .05
        between_delay = 1
        self.command_queue.put(ServoCommand(self.shoulder_x, 1, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.bicep_flex, 1, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.shoulder_y, -1, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.wrist_flex, 1, delayed_end=between_delay))

        self.command_queue.put(ServoCommand(self.shoulder_x, 0, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.bicep_flex, 0, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.shoulder_y, 0, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.wrist_flex, 0, delayed_end=between_delay))

        self.command_queue.put(ServoCommand(self.bicep_flex, 0, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.shoulder_y, -.5, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.shoulder_x, 0, delayed_end=inner_delay))

    def add_drink_commands(self):
        inner_delay = .05
        between_delay = 1
        self.command_queue.put(ServoCommand(self.shoulder_x, 0.5, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.shoulder_y, .7, delayed_end=inner_delay))

        self.command_queue.put(ServoCommand(self.bicep_flex, 0, delayed_end=between_delay))
        self.command_queue.put(ServoCommand(self.head_tilt, 1, delayed_end=between_delay))

        self.command_queue.put(ServoCommand(self.shoulder_x, 1, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.head_tilt, -1, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.bicep_flex, 1, delayed_end=between_delay))

        self.command_queue.put(ServoCommand(self.head_tilt, 0, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.bicep_flex, 0, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.shoulder_y, -.5, delayed_end=inner_delay))
        self.command_queue.put(ServoCommand(self.shoulder_x, 0, delayed_end=inner_delay))


