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
        self.master.title("GUI for data acquisition")
        self.master.geometry("800x500")
        self.master.resizable(False, False)
        self.master.config(background = self.main_color)
        self.master.iconbitmap('logo_GMM.ico')        

        #*******************************************************************************************************************************
        #Frame decleration
        #*******************************************************************************************************************************
        self.serial_data_frame = tk.Frame(self.master, width = '599', height = '499', relief = 'ridge', borderwidth = 1, bg = self.main_color) 
        self.com_config_frame = tk.Frame(self.master, width = '199', height = '199', relief = 'ridge', borderwidth = 1, bg = self.main_color)        
        self.acquisition_frame = tk.Frame(self.master, width = '199', height = '299', relief = 'ridge', borderwidth = 1, bg = self.main_color)

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
        self.serial_data_frame.pack(padx = "2", pady = "2")
        self.serial_data_frame.place(x = 201, y = 1)
        self.com_config_frame.pack(padx = "2", pady = "2")
        self.com_config_frame.place(x = 0, y = 1)
        self.acquisition_frame.pack(padx = "2", pady = "2")
        self.acquisition_frame.place(x = 0, y = 201)

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
        label_title_serial_data = tk.Label(self.serial_data_frame, text="Serial Data", font=("Calibri", 15), bg=self.main_color,
                            fg='white')
        label_title_serial_data.pack()
        label_title_serial_data.place(x = 275, y= 0)

        label_title_com_config = tk.Label(self.com_config_frame, text="Config panel", font=("Calibri", 15), bg=self.main_color, fg='white')
        label_title_com_config.pack()
        label_title_com_config.place(x = 40, y = 0)

        label_title_acquisition = tk.Label(self.acquisition_frame, text="Acquisition control", font=("Calibri", 15), bg=self.main_color,
                            fg='white')
        label_title_acquisition.pack()
        label_title_acquisition.place(x = 20, y= 0)

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

        #file entry label
        self.title_of_my_file = tk.Label(self.acquisition_frame, text="Choose a file name :", bg = self.main_color, fg='white')
        self.title_of_my_file.pack()
        self.title_of_my_file.place(x = 0, y = 33)

        #file format label
        self.title_of_my_file_format = tk.Label(self.acquisition_frame, text="Choose a file format :", bg = self.main_color, fg='white')
        self.title_of_my_file_format.pack()
        self.title_of_my_file_format.place(x = 0, y = 80)

    #*******************************************************************************************************************************
    #Creating widgets
    #*******************************************************************************************************************************
    def create_widgets(self) : 
        #*******************************************************************************************************************************
        #Serial monitor data
        #*******************************************************************************************************************************
        self.scroll_input_data = st.ScrolledText(master = self.serial_data_frame, width = 72, height = 28, relief = 'flat', borderwidth="1")
        self.scroll_input_data.pack()
        self.scroll_input_data.place(x = 0, y=30)

        serialPort.startThread(self.ReceivedData)

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

        #Reset data in serial scrolled text
        self.reset_data_button = tk.Button(self.com_config_frame, text="Reset data",command=self.delete_data)
        self.reset_data_button.pack()
        self.reset_data_button.place(x = 115, y = 150)

        #COM update
        self.com_update_button = tk.Button(self.com_config_frame, text="Update", command = self.reset_ports)
        self.com_update_button.pack()
        self.com_update_button.place(x = 140, y = 58)


        #*******************************************************************************************************************************
        #Acquisition control
        #*******************************************************************************************************************************

        #file entry
        self.my_file = tk.Entry(self.acquisition_frame, width = '15')
        self.my_file.pack()
        self.my_file.place(x = 5, y = 55)

        self.my_file_format = ttk.Combobox(self.acquisition_frame, text = 'file formats')
        self.my_file_format["values"] = (tab_file_format)
        self.my_file_format.set(tab_file_format[1])
        self.my_file_format.pack()
        self.my_file_format.place(x = 5, y = 100)

        self.display_acquisition = tk.Label(self.acquisition_frame, text = "No current data acquisition", width = 21, font=("Courrier", 12), bg='#FCB958', fg=self.main_color)
        self.display_acquisition.pack(pady = 25, padx = self.extern_paddingx)
        self.display_acquisition.place(x = 1, y = 140)

        self.start_acquisition_button = tk.Button(self.acquisition_frame, text="START ACQUISITION", command = self.start_acquisition, bg = "green", fg = self.main_color)
        self.start_acquisition_button.pack(pady = 5, padx = self.extern_paddingx)
        self.start_acquisition_button.place(x = 43, y =180)

        self.stop_acquisition_button = tk.Button(self.acquisition_frame, text="STOP ACQUISITION", command = self.stop_acquisition, bg = "red", fg = self.main_color)
        self.stop_acquisition_button.pack(fill = tk.X, pady = 5, padx = self.extern_paddingx)
        self.stop_acquisition_button.place(x = 45, y = 210)

        self.export_data_button = tk.Button(self.acquisition_frame, text = "Export data", command = self.export_file)
        self.export_data_button.pack()
        self.export_data_button.place(x = 70, y = 240)

    #*******************************************************************************************************************************       
    #Command functions
    #******************************************************************************************************************************* 
    # quit GUI      
    def quit(self):
        self.master.destroy()
   
    #******************************************************************************************************************************* 
    #serial data methods
    def ReceivedData(self, message):
        global str_message
        str_message = message.decode("utf-8")
        self.scroll_input_data.insert('1.0',str_message)
        liste.append(str_message)

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
                self.scroll_input_data.configure(state ='normal')
                self.activate_com_button.config(text='Close com')
            else:
                isopen = False
                serialPort.Close()
                self.scroll_input_data.configure(state ='disabled')
                self.activate_com_button.config(text='Launch com')

    def delete_data(self):
        if isopen == True:
            self.scroll_input_data.delete('1.0',tk.END)
            liste.clear()
        else:
            liste.clear()
            self.scroll_input_data.configure(state ='normal')
            self.scroll_input_data.delete('1.0',tk.END) 
            self.scroll_input_data.configure(state ='disabled')

    def reset_ports(self):
        tab.clear()
        self.show_ports()
        self.box_com['values']=(tab)

    def export_file(self):
            global ret_file_name,ret_format_file
            #b_export["state"] = DISABLED
            if ((len(self.my_file.get()) == 0) or (len(self.scroll_input_data.get('1.0',END))== 0)):
                print("null parameter")
            else:
                ret_file_name = self.my_file.get()
                ret_format_file = self.my_file_format.get() 
                FileName = (ret_file_name+""+ret_format_file) 
                file_check = pathlib.Path(FileName)
                print(FileName)
                if file_check.exists():
                    self.scroll_input_data.configure(state ='normal')
                    self.my_file.delete(0,END)
                    self.scroll_input_data.insert('1.0',"File already exists --> choose anthoser name \n")
                    self.scroll_input_data.configure(state ='disabled')
                else:
                    print("Création du fichier")
                    print(liste[::-1])
                    file = open(FileName,"a")
                    for item in liste:
                        item = item.replace('\r\n','')
                        file.write("%s\n" % item)
                    file.close()
                    self.scroll_input_data.configure(state = 'normal')
                    self.scroll_input_data.insert('1.0',"file created \n")
                    self.scroll_input_data.configure(state = 'disabled')

    #******************************************************************************************************************************* 
    #acquisition control
    def start_acquisition(self):
        self.display_acquisition["text"] = "ongoing data acquisition"
        self.command = "on"
        serialPort.serialport.write(self.command.encode())


    def stop_acquisition(self):
        self.display_acquisition["text"] = "No current data acquisition"
        self.command = "off"
        serialPort.serialport.write(self.command.encode())


if __name__ == '__main__':

    root = tk.Tk()
    app = Application(master=root)
    #def actualisation():
    #    app.after(250,actualisation)
    #app.after(500, actualisation)
    app.mainloop()

