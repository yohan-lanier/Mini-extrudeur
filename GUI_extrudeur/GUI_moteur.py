# coding: utf8
'''
@author = yohan lanier 
@team = Julien Hamelin, Lise Dousset , Alaric Blanque, Yohna Lanier
Projet GMM : extrusion 3D de matériaux locaux @Ecole des Ponts ParisTech 
@note This code is based on the great data logger made by 'DRS Electronic' : https://www.youtube.com/watch?v=3RQPNSiDhYM. Code at : https://github.com/DRSEE/GUI_PyDataLogger
'''

#*******************************************************************************************************************************
#Packages
#*******************************************************************************************************************************
import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as st
import _thread
import sys
import rx_threading
import pathlib
from re import search

#*******************************************************************************************************************************
#INIT
#*******************************************************************************************************************************
serialPort = rx_threading.SerialPort()
arduino_port = ""  #Default COM
baud = 0           #Default baud
tab = [1]
tab.remove(1)
liste = [1]
liste.remove(1)
tab_baud = (1200,1800,2400,4800,7200,9600,19200,38400,57600,115200,128000) #list of baudrate available
tab_file_format = ('.txt','.csv')

isopen = False
        
    
class Application(tk.Frame):
#*******************************************************************************************************************************
#Initialisation
#*******************************************************************************************************************************
    def __init__(self, master=None):
        super().__init__(master)

        self.show_ports()

        self.main_color = '#2D2C36'
        self.intern_paddingx = 15
        self.extern_paddingx = 10
        self.command = ""

        #*******************************************************************************************************************************
        #Master parameters
        #*******************************************************************************************************************************
        self.master = master
        self.master.title("GUI for stepper control")
        self.master.geometry("600x300")
        self.master.resizable(False, False)
        self.master.config(background = self.main_color)
        self.master.iconbitmap('logo_GMM.ico')        

        #*******************************************************************************************************************************
        #Frame decleration
        #*******************************************************************************************************************************
        self.direction_frame = tk.Frame(self.master, width = '199', height = '199', relief = 'ridge', borderwidth = 1, bg = self.main_color)
        self.speed_frame = tk.Frame(self.master, width = '199', height = '299', relief = 'ridge', borderwidth = 1, bg = self.main_color)
        self.com_config_frame = tk.Frame(self.master, width = '199', height = '199', relief = 'ridge', borderwidth = 1, bg = self.main_color)        

        #*******************************************************************************************************************************
        #Packing widgets
        #*******************************************************************************************************************************
        self.create_menu()
        self.create_title()
        self.create_widgets_labels()
        self.create_widgets()

        #*******************************************************************************************************************************
        #packing & placing frames
        #*******************************************************************************************************************************
        self.direction_frame.pack(padx = "2", pady = "2")
        self.direction_frame.place(x=1, y=1)
        self.speed_frame.pack(padx = "2", pady = "2")
        self.speed_frame.place(x=201, y=1)
        self.com_config_frame.pack(padx = "2", pady = "2")
        self.com_config_frame.place(x= 401, y = 1)

    #*******************************************************************************************************************************
    #Menu bars
    #*******************************************************************************************************************************
    def create_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.sub_menu_bar = tk.Menu(self.menu_bar, tearoff = 0)
        self.menu_bar.add_cascade(label = "Menu bar", menu = self.sub_menu_bar)
        self.sub_menu_bar.add_command(label = "Quit", command = quit)
        self.master.config(menu = self.menu_bar)

    #*******************************************************************************************************************************
    #Creating titles
    #*******************************************************************************************************************************
    def create_title(self):

        label_title_directions = tk.Label(self.direction_frame, text="Direction control", font=("Calibri", 15), bg=self.main_color,
                            fg='white')
        label_title_directions.pack()
        label_title_directions.place(x=20, y=0)

        label_title_speeds = tk.Label(self.speed_frame, text="Speed control", font=("Calibri", 15), bg=self.main_color,
                            fg='white')
        label_title_speeds.pack()
        label_title_speeds.place(x=30, y=0)

        label_title_com_config = tk.Label(self.com_config_frame, text="Config panel", font=("Calibri", 15), bg=self.main_color, fg='white')
        label_title_com_config.pack()
        label_title_com_config.place(x = 40, y = 0)

    #*******************************************************************************************************************************
    #Creating widgets labels if necessary
    #*******************************************************************************************************************************
    def create_widgets_labels(self):
        #Com choice label
        self.title_com = tk.Label(self.com_config_frame, text="COM port :", bg = self.main_color, fg='white')
        self.title_com.pack()
        self.title_com.place(x = 10, y = 40)

        #baudrate choice label
        self.title_baudrate = tk.Label(self.com_config_frame, text="Baudrate :", bg = self.main_color, fg='white')
        self.title_baudrate.pack()
        self.title_baudrate.place(x = 10, y = 90)

    #*******************************************************************************************************************************
    #Creating widgets
    #*******************************************************************************************************************************
    def create_widgets(self) : 
        #*******************************************************************************************************************************
        #Direction control
        #*******************************************************************************************************************************
        self.display_direction = tk.Label(self.direction_frame, width = '20', text = "GOING UPWARD", font=("Courrier", 12), bg='#FCB958', fg=self.main_color)
        self.display_direction.pack(fill = tk.X, pady = 25, padx = self.extern_paddingx)
        self.display_direction.place(x = 7, y=50)

        self.upward_button = tk.Button(self.direction_frame, width = '25', text="GO Upward", command = self.set_upward_direction ,bg = "green", fg = self.main_color)
        self.upward_button.pack(fill = tk.X, pady = 5,padx = self.extern_paddingx)
        self.upward_button.place(x = 7, y=100)

        self.downward_button = tk.Button(self.direction_frame, width = '25', text="GO Downward", command = self.set_downward_direction ,bg = "white", fg = self.main_color)
        self.downward_button.pack(fill = tk.X, pady = 5, padx = self.extern_paddingx)
        self.downward_button.place(x = 7, y = 150)

        #*******************************************************************************************************************************
        #Speed control
        #*******************************************************************************************************************************
        self.display_speed = tk.Label(self.speed_frame, width = '20', text = "Current speed = 0.5 rps", font=("Courrier", 12), bg='#FCB958', fg=self.main_color)
        self.display_speed.pack(fill = tk.X, pady = 25, padx = self.extern_paddingx)
        self.display_speed.place(x=7, y=40)

        self.stop_extrusion_button = tk.Button(self.speed_frame, width = '25', text="STOP EXTRUSION", command = self.stop_extrusion_command, bg = "white", fg = "red")
        self.stop_extrusion_button.pack(fill = tk.X, pady = 5, padx = self.extern_paddingx)
        self.stop_extrusion_button.place(x = 7, y = 90)

        self.hspeed_button = tk.Button(self.speed_frame, width = '25', text="HIGH SPEED", command = self.set_high_speed ,bg = "white", fg = self.main_color)
        self.hspeed_button.pack(fill = tk.X, pady = 5, padx = self.extern_paddingx)
        self.hspeed_button.place(x = 7, y=140)
        
        self.aspeed_button = tk.Button(self.speed_frame, width = '25', text="AVERAGE SPEED", command = self.set_average_speed ,bg = "white", fg = self.main_color)
        self.aspeed_button.pack(fill = tk.X, pady = 5, padx = self.extern_paddingx)
        self.aspeed_button.place(x = 7, y = 190)

        self.lspeed_button = tk.Button(self.speed_frame, width = '25', text="LOW SPEED", command = self.set_low_speed ,bg = "green", fg = self.main_color)
        self.lspeed_button.pack(fill = tk.X, pady = 5, padx = self.extern_paddingx)
        self.lspeed_button.place(x = 7, y=240)


        #*******************************************************************************************************************************
        #Com config menu
        #*******************************************************************************************************************************
        #Com port choice
        self.box_com = ttk.Combobox(self.com_config_frame, width = 15)
        self.box_com["values"] = (tab)
        if numConnection >1:
             self.box_com.set(tab[1])
        else:
             self.box_com.set(tab[0])
        self.box_com.pack()
        self.box_com.place(x = 10, y=60)

        #Baudrate choice
        self.box_baudrate = ttk.Combobox(self.com_config_frame, width = 15)
        self.box_baudrate["values"] = (tab_baud)
        self.box_baudrate.set(tab_baud[5]) #set default baudrate -> element 5 -> 9600
        self.box_baudrate.pack()
        self.box_baudrate.place(x = 10, y = 110)

        #launch COM
        self.activate_com_button = tk.Button(self.com_config_frame, text="Launch com",command=self.open_com)
        self.activate_com_button.pack()
        self.activate_com_button.place(x = 15,y= 150)

        #COM update
        self.com_update_button = tk.Button(self.com_config_frame, text="Update", command = self.reset_ports)
        self.com_update_button.pack()
        self.com_update_button.place(x = 140, y = 58)      
    #*******************************************************************************************************************************       
    #Command functions
    #******************************************************************************************************************************* 
    # quit GUI      
    def quit(self):
        self.master.destroy()
    #******************************************************************************************************************************* 
    #direction control
    def set_upward_direction(self): 
        self.display_direction["text"] = "GOING UPWARD"
        self.upward_button["bg"] = "green"
        self.downward_button["bg"] = "white"
        self.stop_extrusion_button["bg"] = 'white'
        self.command = "u"
        serialPort.serialport.write(self.command.encode())


    def set_downward_direction(self): 
        self.display_direction["text"] = "GOING DOWNWARD"
        self.downward_button["bg"] = "green"
        self.upward_button["bg"] = "white"
        self.stop_extrusion_button["bg"] = 'white'
        self.command = "d"
        serialPort.serialport.write(self.command.encode())

    #******************************************************************************************************************************* 
    #speed control
    def stop_extrusion_command(self):
        self.stop_extrusion_button["bg"] = '#FE7777'
        self.display_speed["text"] = "Current speed = 0 rps"
        self.hspeed_button["bg"] = "white"
        self.aspeed_button["bg"] = "white"
        self.lspeed_button["bg"] = 'white'
        self.command = "s"
        serialPort.serialport.write(self.command.encode())

    def set_high_speed(self): 
        self.display_speed["text"] = "Current speed = 2.5 rps"
        self.hspeed_button["bg"] = "green"
        self.aspeed_button["bg"] = "white"
        self.lspeed_button["bg"] = 'white'
        self.stop_extrusion_button["bg"] = 'white'
        self.command = "h"
        serialPort.serialport.write(self.command.encode())

    def set_average_speed(self): 
        self.display_speed["text"] = "Current speed = 1.25 rps"
        self.hspeed_button["bg"] = "white"
        self.aspeed_button["bg"] = "green"
        self.lspeed_button["bg"] = 'white'
        self.stop_extrusion_button["bg"] = 'white'
        self.command = "a"
        serialPort.serialport.write(self.command.encode())

    def set_low_speed(self): 
        self.display_speed["text"] = "Current speed = 0.5 rps"
        self.hspeed_button["bg"] = "white"
        self.aspeed_button["bg"] = "white"
        self.lspeed_button["bg"] = 'green'
        self.stop_extrusion_button["bg"] = 'white'
        self.command = "l"
        serialPort.serialport.write(self.command.encode())


    #******************************************************************************************************************************* 
    #config panel methods
    @staticmethod
    def show_ports():
        global strPort
        global tab
        global numConnection
        ports = serial.tools.list_ports.comports()
        numConnection = len(ports)
        for i in range(0,numConnection):
            port = ports[i]
            strPort = str(port)
            var = len(strPort)
            var = var - 5
            strPort = strPort[:-var]
            tab.append(strPort)
            print(strPort)

    def open_com(self):
        global ret_box,ret_box_baud,isopen
        if ( (len(self.box_com.get()) == 0) or (len(self.box_baudrate.get()) == 0)):
            print("null parameter")
        else:
            if self.activate_com_button.cget("text") == 'Launch com':
                isopen = True
                ret_box = self.box_com.get()
                ret_box_baud = self.box_baudrate.get()
                arduino_port = ret_box
                baud = ret_box_baud
                serialPort.Open(arduino_port,baud)
                self.activate_com_button.config(text='Close com')
            else:
                isopen = False
                serialPort.Close()
                self.activate_com_button.config(text='Launch com')

    def reset_ports(self):
        tab.clear()
        self.show_ports()
        self.box_com['values']=(tab)

if __name__ == '__main__':

    root = tk.Tk()
    app = Application(master=root)
    #def actualisation():
    #    app.after(250,actualisation)
    #app.after(500, actualisation)
    app.mainloop()

