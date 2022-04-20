# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from RobotContainer import RobotContainer

def main():
    robot_container = RobotContainer()
    commands = []
    while robot.step(TIMESTEP) != -1 and index < len(commands) and index <= max_index:
        if runCommands:
            if not commands[index].initialized:
                commands[index].initialize(robot.getTime())
            if not commands[index].is_finished():
                commands[index].update(robot.getTime())
            else:
                print("Ended Command")
                index += 1
                if index < len(commands):
                    commands[index].initialize(robot.getTime())

            if touchSensor.getValue() > 0:
                mapper.setTrophy(drivetrain.odometry.getPose())
                print("WIN!")
                break
        if mapper.updateGridWalls(drivetrain.odometry.getPose(), drivetrain.get_heading(), sonicSensors.get_grid()):
            mapper.prettyPrintMap()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
