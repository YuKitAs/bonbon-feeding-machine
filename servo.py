import serial
def send_servo_signal():
    with serial.Serial('/dev/ttyACM0', 9600) as ser:
        print(ser.name)
        ser.write(b'f')

if __name__ == '__main__':
    send_servo_signal()
