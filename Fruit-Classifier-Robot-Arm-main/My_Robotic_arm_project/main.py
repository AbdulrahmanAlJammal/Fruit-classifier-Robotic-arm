import tkinter as tk
from tkinter import *
import PIL.Image
import PIL.ImageTk
import sys
import glob
import serial
import time
from threading import Thread


def animation(count_inner):
    global showAnimation
    if showAnimation != 1:
        new_image = imageObject[count_inner]
        gif_label.configure(image=new_image)
        count_inner += 1
        if count_inner == frames:
            count_inner = 0
        showAnimation = root.after(25, lambda: animation(count_inner))
    else:
        global Com_port
        global final_ser
        gif_label.destroy()
        from MatrixGui import main_task

        root.destroy()
        main_task(Com_port, final_ser)


def test_connection():
    while True:
        global testConnection
        if testConnection != 1:
            send_data_to_all_ports()
        else:
            break


def serial_ports():
    """Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def send_data_to_all_ports():
    results = serial_ports()
    for x in results:
        print(x)
        ser_com = serial.Serial(x, 9600)
        time.sleep(3)
        data = "S"
        print(ser_com)
        ser_com.write(data.encode())
        print("here")
        time.sleep(3)
        print("here2")
        data = receive_ack_from_arduino(ser_com)
        print(data)
        if data is True:
            global Com_port
            global testConnection
            global showAnimation
            global final_ser
            Com_port = x
            testConnection = 1
            showAnimation = 1
            final_ser = ser_com


def receive_ack_from_arduino(ser_com):
    if isinstance(ser_com, serial.Serial):
        print("here3")
        print(ser_com)
        while not ser_com.inWaiting():
            continue
        data = ser_com.readline()
        print(data.decode())
        if data.decode() == "Arduino Ack\r\n":
            return True
        else:
            return False
    else:
        return False


root = tk.Tk()
root.title("Robotic arm")
root.geometry("750x750")
root.configure(bg="#055d7b")
label = Label(
    root, text="Waiting for a connection to a robotic arm", bg="#055d7b", font=12
)
label.place(relx=0.5, rely=0.5, anchor="center")
gifImage = "blue_spinner.gif"
openImage = PIL.Image.open(gifImage)
frames = openImage.n_frames
imageObject = [
    PhotoImage(file=gifImage, format=f"gif -index {i}") for i in range(frames)
]
count = 0
showAnimation = None
testConnection = None
Com_port = None
final_ser = None
gif_label = Label(root, image="", bg="#055d7b")
gif_label.place(relx=0.5, rely=0.65, width=150, height=150, anchor="center")
animation(count)
daemon = Thread(target=test_connection, daemon=True, name="Monitor")
daemon.start()
root.mainloop()
