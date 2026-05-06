"""A weather app which displays home information from an arduino"""

import tkinter as tk
import re
import sys
import serial # library used to communicate with serial port

class iHome():
    """The main weather app"""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, **kwargs):
        self.gui = GUI(self)
        self.kwargs = kwargs
        self.ser = open_serial_port(self).ser
        self.temp = ''
        self.humd = ''
        self.motion = ''


        while True:
            self.get_home()
            break
    def extract_humd(self, message):
        """Exracts humidity from a message"""
        data_string = message.decode("utf-8")
        humd = re.findall('humd=([\d]+[.,\d]+),', data_string)
        return humd

    def extract_motion(self, message):
        """Exracts motion from a message"""
        data_string = message.decode("utf-8")
        motion = re.findall('motion=([\d]+[.,\d]+)>', data_string)
        return motion

    def extract_temp(self, message):
        """Exracts temperature from a message"""
        data_string = message.decode("utf-8")
        temp = re.findall('<temp=([\d]+[.,\d]+),', data_string)
        return temp

    def extract_data(self, message):
        """Extracts all of the data from a message checking if there is an error"""
        if message.decode("utf-8")[0] == "<":
            self.temp = self.extract_temp(message)[0]
            self.humd = self.extract_humd(message)[0]
            self.motion = self.extract_motion(message)[0]
        return [self.temp, self.humd, self.motion]

    def get_home(self):
        """Get home"""
        print("working...")
        message = self.ser.readline()
        # read one line (until EOL) from the serial port
        #message = b'<temp=4.2,humd=42,motion=1>'
        data = self.extract_data(message)
        #global data_file
        if len(data[0]) > 0:
            data_values = [float(s[0]) for s in data]
            for i in range(len(data_values)):
                if data_values[i].is_integer():
                    data_values[i] += 10
            for i in range(len(data_values)):
                data_values[i] = str(data_values[i])
            temp = data_values[0]
            motion = data_values[1]
            humd = data_values[2]
            print(self.temp)
            print(self.humd)
            print(self.motion)
            self.gui.lbl_temp["text"] = f'{float(self.temp):.2f} Cº'
            self.gui.lbl_humd["text"] = f'{float(self.humd):.2f} %'
            motion = "No movement"
            if float(self.motion):
                motion = "Movement detected"
            self.gui.lbl_motion["text"] = motion
        self.gui.after(1000, self.get_home)

    def run(self):
        """Main loop"""
        self.gui.mainloop()

class GUI(tk.Tk):
    """Graphical Interface for weather app"""

    def __init__(self, weatherstation):
        super().__init__()
        self.geometry("500x200")
        self.title('iHome')
        self.resizable(False, False)
        self.btn_quit = tk.Button(master=self, text="Quit", font=50, bg="red", fg="white", command=self.close_application)
        self.btn_quit.place(x=230, y=100)
        self.lbl_temp = tk.Label(master=self, text = "Inital te C", font = 50)
        self.lbl_temp.place(x=130, y=20)
        self.lbl_humd = tk.Label(master=self, text = "Initial te %", font = 50)
        self.lbl_humd.place(x=230, y=20)
        self.lbl_motion = tk.Label(master=self, text = "Initial text motion", font = 50)
        self.lbl_motion.place(x=330, y=20)

    def close_application(self):
        """Destroys window"""
        self.destroy()

class open_serial_port():
    """An open serial port which gets used in the weather app"""

    def __init__(self, app):
        self.SERIAL_PORT_DEFAULT ='COM4'
        self.SERIAL_BAUDRATE_DEFAULT = 9600
        if 'serial_port' in app.kwargs:
            self.serial_port = app.kwargs['serial_port']
        else:
            self.serial_port = self.SERIAL_PORT_DEFAULT
        if 'serial_baudrate' in app.kwargs:
            self.serial_baudrate = app.kwargs['serial_baudrate']
        else:
            self.serial_baudrate = self.SERIAL_BAUDRATE_DEFAULT
        self.ser = serial.Serial()
        self.ser.port = self.serial_port
        try:
            self.ser.open() # open the serial port
            if self.ser.isOpen(): # check if the serial port is opened successfully
                print("Port " + self.ser.port + " opened successfully")
        except Exception as e:
            print(e)
            sys.exit()


App = iHome(serial_port = 'COM4')
App.run()
App.f.close()
App.ser.close()