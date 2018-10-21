#!/usr/bin/python3
'''
#Author: Harsimransingh Bindra
#Date: 09/26/2018
#File: python source file containing QT5 application code and DHT22 sensor code interfacing code.
#Description: A application is created to display the readings from DHT22 temperature sensor. Temperature values in celcius and humidity values in percentage are printed. The application also contains graphical representation of last 10 temperature and humidity values. The application also displays the average values of temperature and humidity. There are two spin boxes used to setup the threshold values for temperature and humidity. If the current values exceed the set threshold warning message is displayed on the application. In addition to the warning display message an email notification is sent to the desired user too.
#references:
    https://ralsina.me/posts/BB974.html
    https://stackoverflow.com/questions/11812000/login-dialog-pyqt
    https://gist.github.com/pklaus/3e16982d952969eb8a9a
'''
import sys
import MySQLdb
#import mysql.connector
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from email.mime.text import MIMEText
from time import gmtime, strftime
import time
import smtplib
import Adafruit_DHT as dht
import datetime
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#to connect to database
db = MySQLdb.connect(host="localhost", # your host
        user="root",
        # username
        passwd="root", # password
        db="pythonspot") # name of the database
# Create a Cursor object to execute queries.
cur = db.cursor()

#global variables
#list a used for saving 6 latest temperature values
global a
a = [0] * 6
#list b used for saving 6 latest humidity values
global b
b = [0] * 6
i = 0
j = 0

#global variable for connection status
connection_status_temp = 0
connection_status_hum = 0

#global for conversion
conversion = 1
#global variables used for email notifications
global fromaddr
fromaddr = 'speedking2421@gmail.com'
global pwd
pwd = 'Hello@world'
global smtp_server
smtp_server = 'smtp.gmail.com:587'
from PyQt5 import QtWidgets
class plot_graph(FigureCanvas):
    '''
    The plot_graph class is defined to intialise and create the general axis graph using the FigureCanvas packa    ge.
    '''
    def __init__(self, parent=None, width=1.5, height=1.5, dpi=100):
        '''
        init function for plot_graph class defining the width and height and pixel value for the graph
        '''
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        #to clear the axes everytime this function is called
        self.axes.clear()
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass

class draw_temp_graph(plot_graph):
    '''
    Class draw_temp_graph used to define all the functions used to draw the temperature graph using the values stored in list a storing the last 6 temperature values
    '''
    def __init__(self, *args, **kwargs):
        plot_graph.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(5000)
    def compute_initial_figure(self):
        # t variable to to print values 0 to 5 on x axis
        t = [0,1,2,3,4,5]
        self.axes.plot(t, b,'r')
    def update_figure(self):
        '''
        update_figure function in draw_temp_graph is called after every 5 seconds to display the last 5 temperature on the graph
        '''
        #t variable to print values 0 to 5 on x axis
        t = [0,1,2,3,4,5]
        self.axes.clear()
        #plot temperature values on graph
        self.axes.plot(t, a, 'r')
        self.draw()

class draw_hum_graph(plot_graph):
    '''
    Class draw_hum_graph used to define all the functions used to draw the humidity graph using the values stored in list b storing the last 6 humidity values
    '''
    def __init__(self, *args, **kwargs):
        plot_graph.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(5000)
    def compute_initial_figure(self):
        t = [0,1,2,3,4,5]
        self.axes.plot(t, b,'r')
    def update_figure(self):
        '''
        update_figure function in draw_hum_graph is called after every 5 seconds to display the last 5 humidity on the graph
        '''
        t = [0,1,2,3,4,5]
        self.axes.clear()
        self.axes.plot(t, b, 'r')
        self.draw()


class Login(QtWidgets.QDialog):
    '''
    Login class is defined to create a login window before the application window is launched for having a secured login
    '''
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.login_Compare)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
    def login_Compare(self):
        '''
        login_Compare class is used to compare the input username and password
        '''
        #conditional statement to check if the login details match with the input
        if (self.textName.text() == 'Harsimransingh' and self.textPass.text() == 'Bindra'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password')
class project(QDialog):
    '''
    project class contains the code to create the main application
    '''
    def __init__(self):
        super(project,self).__init__()
        #load ui created on the designer
        loadUi('project.ui',self)
        self.setWindowTitle('Project 1')
        #configure the push buttons to call the required functions
        self.temperature.clicked.connect(self.on_pushButton_temp_clicked)
        self.conversion1.clicked.connect(self.on_pushButton_conversion_clicked)
        self.humidity.clicked.connect(self.on_pushButton_hum_clicked)
        #create widgets to draw the temperature and humidity graphs
        self.temp_widget = QWidget(self)
        self.temp_widget.setGeometry(QtCore.QRect(420, 0, 200, 150))
        temp_l = QVBoxLayout(self.temp_widget)
        temp_sc= draw_temp_graph(self.temp_widget, width=1, height=1, dpi=50)
        self.hum_widget = QWidget(self)
        self.hum_widget.setGeometry(QtCore.QRect(420, 180, 200, 150))
        hum_l = QVBoxLayout(self.hum_widget)
        hum_sc = draw_hum_graph(self.hum_widget, width=1, height=1, dpi=50)
        temp_l.addWidget(temp_sc)
        hum_l.addWidget(hum_sc)
        self.temperature_threshold.setValue(50)
        self.humidity_threshold.setValue(70)
        self.get_temp()
        self.get_hum()
    @pyqtSlot()

    def get_temp(self):
        '''
        get_temp function in project class is used to get the temperature values from the sensor and store it in a list to compute the average and provide additional functionality. This function also contains code to compare the threshold value to set off an email alert and display warning message when the current value exceeds the threshold
        '''
        try:
            global connection_status_temp
            h,t = dht.read(dht.DHT22, 4)
            temp_counter = 0
            global i
            global cur
            #condition to handle the condition when sensor is disconnected
            if h == None and t == None:
                if connection_status_temp == 0:
                    cur = db.cursor()
                    cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
                    for row in cur.fetchall():
                        min_temp = row[3]
                        max_temp = row[4]
                        time_stamp=strftime('%H:%M:%S   %D')
                    sql = """INSERT INTO temperature(label,timestamp,minimum,maximum) VALUES(%s,%s,%s,%s)"""
                    cur.execute(sql, ('Not Connected',time_stamp,min_temp,max_temp))
                    db.commit()
                    connection_status_temp = 1
                self.label_temp.setText('Not connected')
            else:
                connection_status_temp = 0
                cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
                for row in cur.fetchall():
                    min_temp = float(row[3])
                    print(min_temp)
                    if t <= min_temp:
                        minimum = str(round(t,3))
                    else:
                        minimum = str(min_temp)
                    max_temp = float(row[4])
                    print(max_temp)
                    if max_temp<=t:
                        maximum = str(round(t,3))
                    else:
                        maximum = str(round(max_temp,3))

                time_stamp=strftime('%H:%M:%S   %D')
                self.temp_min_time.setText(time_stamp)
                self.temp_max_time.setText(time_stamp)
                if conversion == 0:
                    min_temp = min_temp*1.8 + 32
                    max_temp = max_temp*1.8 + 32
                    self.temp_minimum.setText(str(round(min_temp,3)) + ' F')
                    self.temp_maximum.setText(str(round(max_temp,3)) + ' F')
                else:
                    self.temp_minimum.setText(minimum + ' C')
                    self.temp_maximum.setText(maximum + ' C')
                cur = db.cursor()
                val = str(round(t,3))
                time_stamp=strftime('%H:%M:%S   %D')
                sql = """INSERT INTO temperature(label,timestamp,minimum,maximum) VALUES(%s,%s,%s,%s)"""
                #temperature_string = str(round(t,3))
                cur.execute(sql, (val,time_stamp,minimum,maximum))
                db.commit()
                # Select data from table using SQL query.
                cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 5")
                #print the first and second columns
                for row in cur.fetchall():
                    print(row[0], " ", row[1], row[2], row[3], row[4])
                a[i] = t
                i = i + 1
                temp_counter=len(a)
                average_temp = sum(a)/len(a)
                if a[5] != 0:
                    if i == 5:
                        sql = """INSERT INTO temperature_average(average,timestamp) VALUES(%s,%s)"""
                        val = str(round(average_temp,3))
                        time_stamp=strftime('%H:%M:%S   %D')
                        cur.execute(sql, (val,time_stamp))
                        db.commit()
                        # Select data from table using SQL query.
                        cur.execute("SELECT * FROM temperature_average ORDER by id DESC LIMIT 2")
                        # print the first and second columns
                 #       for row in cur.fetchall():
                   #         print(row[0], " ", row[1], row[2])
                    if conversion == 0:
                        average_temp = average_temp*1.8 + 32
                        self.average_temperature.setText(str(round(average_temp,3))+' F')
                    else:
                        self.average_temperature.setText(str(round(average_temp,3))+ ' C')
                time_stamp=strftime('%H:%M:%S   %D')
                self.temp_avg_time.setText(time_stamp)
                #to read the value from spin box to set as threshold
                temp_threshold = self.temperature_threshold.value()
                #condition to check whether the current value exceeds the threshold
                if t >= temp_threshold:
                    subject = "High Temperature"
                    body = "Temperature above the set threshold"
                    server = smtplib.SMTP(smtp_server)
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    message = """From: %s \nTo: %s\nSubject: %s\n\n%s """ %(fromaddr, ",".join("harsimran2411@gmail.com"),subject,body)
                    server.login(fromaddr,pwd)
                    server.sendmail(fromaddr, "harsimran2411@gmail.com",message)
                    server.quit()
                    self.temp_alert.setText('Warning')
                else:
                    self.temp_alert.setText('Ok')
            if i == 6:
                i = 0
        finally:
            #Timer to run the code after every 3 seconds
            QTimer.singleShot(5000,self.get_temp)
    def get_hum(self):
        '''
        get_hum function in project class is used to get the humidity values from the sensor and store it in a list to compute the average and provide additional functionality. This function also contains code to compare the threshold value to set off an email alert and display warning message when the current value exceeds the threshold
        '''
        try:
            global connection_status_hum
            #read value from the sensor
            h,t = dht.read(dht.DHT22, 4)
            global j
            #condition to check if the sensor is disconnected
            if h == None and t == None:
                if connection_status_hum == 0:
                    cur = db.cursor()
                    cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
                    for row in cur.fetchall():
                        min_temp = row[3]
                        max_temp = row[4]
                        time_stamp=strftime('%H:%M:%S   %D')
                    sql = """INSERT INTO humidity(label,timestamp,minimum,maximum) VALUES(%s,%s,%s,%s)"""
                    cur.execute(sql, ('Not Connected',time_stamp,min_temp,max_temp))
                    db.commit()
                    connection_status_hum = 1
                self.label_hum.setText('Not connected')
            else:
                connection_status_hum = 0
                cur = db.cursor()
                cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
                for row in cur.fetchall():
                    min_temp = float(row[3])
                    print(min_temp)
                    if h <= min_temp:
                        minimum = str(round(h,3))
                    else:
                        minimum = str(min_temp)
                    max_temp = float(row[4])
                    print(max_temp)
                    if max_temp<=h:
                        maximum = str(round(h,3))
                    else:
                        maximum = str(max_temp)
                time_stamp=strftime('%H:%M:%S   %D')
                self.hum_minimum.setText(minimum)
                self.hum_min_time.setText(time_stamp)
                self.hum_maximum.setText(maximum)
                self.hum_max_time.setText(time_stamp)
                val = str(round(h,3))
                sql = """INSERT INTO humidity(label,timestamp,minimum,maximum) VALUES(%s,%s,%s,%s)"""
                #temperature_string = str(round(t,3))
                cur.execute(sql, (val,time_stamp,minimum,maximum))
                db.commit()
                # Select data from table using SQL query.
                cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 5")
                # print the first and second columns
                #for row in cur.fetchall():
                 # print(row[0], " ", row[1], row[2])
                b[j] = h
                j = j+1
                average_hum = sum(b)/len(b)
                if b[5] != 0: 
                    if j == 5:
                        sql = """INSERT INTO humidity_average(average,timestamp) VALUES(%s,%s)"""
                        val = str(round(average_hum,3))
                        time_stamp=strftime('%H:%M:%S   %D')
                        cur.execute(sql, (val,time_stamp))
                        db.commit()
                        # Select data from table using SQL query.
                        cur.execute("SELECT * FROM humidity_average ORDER by id DESC LIMIT 2")
                        # print the first and second columns
                        for row in cur.fetchall():
                            print(row[0], " ", row[1], row[2])
                    self.average_humidity.setText(str(average_hum))
                    time_stamp=strftime('%H:%M:%S   %D')
                    self.hum_avg_time.setText(time_stamp)
                if j ==6:
                    j = 0
                #read the the humidity threshold value from the spinbox
                hum_threshold = self.humidity_threshold.value()
                #condition to check if the current value exceeds the threshold
                if h >= hum_threshold:
                    subject = "High Humidity"
                    body = "Humidity value above threshold"
                    server = smtplib.SMTP(smtp_server)
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    message = """From: %s \nTo: %s\nSubject: %s\n\n%s """ %(fromaddr, ",".join("harsimran2411@gmail.com"),subject,body)
                    server.login(fromaddr,pwd)
                    server.sendmail(fromaddr, "harsimran2411@gmail.com",message)
                    server.quit()
                    self.hum_alert.setText('Warning')
                else:
                    self.hum_alert.setText('Ok')
        finally:
            #condition to run the code in every 3 seconds
            QTimer.singleShot(5000,self.get_hum)
    
    def on_pushButton_conversion_clicked(self):
        global conversion
        conversion = conversion ^ 1
    
    def on_pushButton_temp_clicked(self):
        '''
        on_pushButton_temp_clicked function is called when the temperature request push button is clicked and it reads the latest temperature value and displays it on the application
        '''
        #read value from DHT22 sensor
        h,t = dht.read(dht.DHT22, 4)
        if h == None and t == None:
            self.label_temp.setText('Not connected')
        else:
            if conversion == 0:
                temp_f = t*1.8 + 32
                self.label_temp.setText(str(round(temp_f,3)) + " F")
            else:
                self.label_temp.setText(str(round(t,3)) + " C")
        #print timestamp for the latest request
        self.temp_time.setText(strftime('%H:%M:%S   %D'))
    def on_pushButton_hum_clicked(self):
        '''
        on_pushButton_hum_clicked function is called when the humidity request push button is clicked and it reads the latest humidity value and displays it on the application
        '''
        h,t = dht.read(dht.DHT22, 4)
        if h == None and t == None:
            self.label_hum.setText('Not connected') 
        else:
            self.label_hum.setText(str(round(h,3))+"%")
        #print timestamp for the latest request
        self.hum_time.setText(strftime('%H:%M:%S   %D'))
app = QApplication(sys.argv)
login = Login()
#open the application is the login comparison is successful
if login.exec_() == QtWidgets.QDialog.Accepted:
    w = project()
    w.show()
    sys.exit(app.exec_())
