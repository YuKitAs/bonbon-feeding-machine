import time

import os
import serial


def is_new_command(command, last_command_timestamp):
    command, timestamp = command.split("_")
    return int(timestamp) > last_command_timestamp


def main():
    with serial.Serial("/dev/ttyACM0", 9600, timeout=5) as ser:
        while "READY" not in ser.readline().decode("utf-8"):
            time.sleep(1)
        print("connected")

        accumulated_loops = 0
        last_command_timestamp = int(time.time())
        while True:
            accumulated_loops += 1

            if accumulated_loops >= 10:
                accumulated_loops = 0

                ser.write(b"h")

                if "ALIVE" not in ser.readline().decode("utf-8"):
                    print("heartbeat missing")

            commands = os.listdir("/tmp/bonbon/commands")
            new_commands = list(filter(lambda command: is_new_command(command, last_command_timestamp), commands))

            if new_commands != []:
                last_command_timestamp = int(time.time())

                for new_command in new_commands:
                    if new_command.startswith("feed"):
                        ser.write(b"f")
                    elif new_command.startswith("reset"):
                        ser.write(b"r")
                    elif new_command.startswith("forward"):
                        ser.write(b"a")
                    elif new_command.startswith("backward"):
                        ser.write(b"b")
                ser.readline()
                time.sleep(5)

            time.sleep(1)


if __name__ == '__main__':
    main()
