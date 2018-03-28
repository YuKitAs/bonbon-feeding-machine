import time
import os

import serial


def isNewCommand(command, last_command_timestamp):
    command, timestamp = command.split("_")
    return int(timestamp) > last_command_timestamp


def main():
    with serial.Serial("/dev/ttyACM0", 9600, timeout=5) as ser:
        while "READY" not in ser.readline().decode("utf-8"):
            time.sleep(1)
        print("connected")

        accumulatedLoops = 0
        last_command_timestamp = int(time.time())
        while True:
            accumulatedLoops += 1

            if accumulatedLoops >= 10:
                accumulatedLoops = 0

                ser.write(b"h")

                if "ALIVE" not in ser.readline().decode("utf-8"):
                    print("heatbeat-missing")

            commands = os.listdir("/tmp/bonbon/commands")
            newCommands = list(filter(lambda command: isNewCommand(command, last_command_timestamp), commands))

            if newCommands != []:
                last_command_timestamp = int(time.time())

                for newCommand in newCommands:
                    if newCommand.startswith("feed"):
                        ser.write(b"f")
                    elif newCommand.startswith("reset"):
                        ser.write(b"r")
                    elif newCommand.startswith("forward"):
                        ser.write(b"a")
                    elif newCommand.startswith("backward"):
                        ser.write(b"b")
                ser.readline()
                time.sleep(5)

            time.sleep(1)


if __name__ == '__main__':
    main()
