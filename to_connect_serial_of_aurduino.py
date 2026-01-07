import serial
import time

ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

def send_to_arduino(label):
    if label == "metal":
        ser.write(b'M')
    elif label == "plastic":
        ser.write(b'P')
    elif label == "paper":
        ser.write(b'R')

send_to_arduino("metal")
