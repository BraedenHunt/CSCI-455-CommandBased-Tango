from Drivetrain import Drivetrain
from Command import Command

class DriveForwardCommand(Command):

    def __init__(self, drivetrain: Drivetrain, time_to_drive, left_speed, right_speed):
        self.drivetrain = drivetrain
        self.time_to_drive = time_to_drive
        self.left_speed = left_speed
        self.right_speed = right_speed


    def update(self, time):
        self.time = time - self.initial_time
        self.drivetrain.drive(self.left_speed, self.right_speed)
        self.drivetrain.update()

    def initialize(self, time):
        self.initial_time = time
        self.initialized = True

    def end(self, interrupted):
        self.drivetrain(0, 0)

    def is_finished(self):
        return self.time >= self.time_to_drive