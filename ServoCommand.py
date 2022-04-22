from Command import Command
from PWMController import PWMController

class ServoCommand(Command):
    CENTER = 0
    MAX = 1
    MIN = -1
    LOW_MID = -.5
    HIGH_MID = .5

    def __init__(self, servo: PWMController, target, delayed_end=0.1):
        self.servo = servo
        self.servo.set(0)
        self.target = target
        self.start_time = None
        self.delayed_end = delayed_end
        self.time_elapsed = 0

    def initialize(self, time):
        self.start_time = time
        self.initialized = True
        self.servo.set(self.target)

    def update(self, time):
        self.time_elapsed = time-self.start_time

    def is_finished(self):
        return self.time_elapsed >= self.delayed_end