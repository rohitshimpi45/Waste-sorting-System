

import cv2
import requests
import numpy as np
from ultralytics import YOLO
import serial
import time

# ESP32 details
ESP_IP = "192.168.56.107"
CAPTURE_URL = f"http://{ESP_IP}/capture"

# Arduino Serial (check your COM port in Device Manager)
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

# Load YOLO model
model = YOLO(r"D:\deep learning\janatics\runs\detect\train14\weights\best.pt")
print("Model class names:", model.names)


def send_to_arduino(label):
    # Only send signals for plastic or paper
    if label == "plastic":
        ser.write(b'P')  # Plastic → Piston 2
    elif label == "paper":
        ser.write(b'R')  # Paper → Piston 3 (if applicable)


def main():
    while True:
        try:
            # Capture image from ESP32
            img_resp = requests.get(CAPTURE_URL, timeout=2)
            img_resp.raise_for_status()
            img = cv2.imdecode(np.frombuffer(img_resp.content, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                print("Error: Failed to decode image")
                continue
        except Exception as e:
            print(f"Error capturing image: {e}")
            continue

        # Run YOLO inference
        results = model(img)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls]

                # Only check plastic and paper
                if label in ["plastic", "paper"] and conf > 0.2:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Send label to Arduino
                    send_to_arduino(label)

        cv2.imshow("Detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    ser.close()  # Close serial port when done


if __name__ == "__main__":
    main()
