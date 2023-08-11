import tkinter as tk
from tkinter import *
from threading import Thread
import time
import cv2
from roboflow import Roboflow


def main_task(com_data, ser_data):
    global port
    global arm_serial
    global matrix_gui
    global label_3
    global model
    global cam
    port = com_data
    arm_serial = ser_data
    rf = Roboflow(api_key="GEmyku3lcfnR5MjWDq61")
    project = rf.workspace().project("strawberries-chain-chua-chain")
    model = project.version(1).model
    cam_port = 1
    cam = cv2.VideoCapture(cam_port)

    label_3.configure(text=f"Arduino is connected in port {port}", font=("Arial", 25))
    daemon = Thread(target=back_ground_task, daemon=True, name="Monitor")
    daemon.start()
    matrix_gui.mainloop()


def back_ground_task():
    global model
    global arm_serial
    global cam

    while True:
        cam = cv2.VideoCapture(1)
        result, image = cam.read()
        if result:
            cv2.imwrite("img.png", image)

            # infer on a local image
            pred = model.predict("img.png", confidence=50, overlap=30)
            pred.save()
            json_result = pred.json()
            json_result = json_result["predictions"]
            max = 0
            pred = ""
            for x in json_result:
                if x["confidence"] > max:
                    max = x["confidence"]
                    pred = x["class"]

            if pred == "chin":
                arm_serial.write("1".encode())
            elif pred == "chua_chin":
                arm_serial.write("0".encode())
            time.sleep(4)
            cam.release()
            
            # cv2.imshow("img.png", image)

        # If captured image is corrupted, moving to else part
        else:
            print("No image detected. Please! try again")
            time.sleep(4)


Data_transmit = None
arm_serial = None
port = None
connection = True
matrix_gui = tk.Tk()
matrix_gui.title("Robotic arm")
matrix_gui.geometry("1200x500")
matrix_gui.configure(bg="#055d7b")
label_3 = Label(matrix_gui, text="", bg="#055d7b")
label_3.place(relx=0.5, rely=0.5, anchor="center")
