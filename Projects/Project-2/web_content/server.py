#!/usr/bin/python3
'''
#Author: Harsimransingh Bindra
#Date: 10/21/2018
#File: python source file containing webserver code
#Description: A webserver is created which consumes temperature and humidity values from a database and sends to a webpage using websockets. 
#references:
    https://os.mbed.com/cookbook/Websockets-Server
    https://websockets.readthedocs.io/en/stable/intro.html
'''
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import MySQLdb

conversion_status = 1
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 
# Create a Cursor object to execute queries.

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        '''
        open is called when a new connection is opened
        '''
        print('new connection')

    def on_message(self, message):
        '''
        on_message function is called when a message is recieved at the websocket connection
        '''
        global conversion_status
        db = MySQLdb.connect(host="localhost", # your host
            user="root",
            # username
            passwd="root", # password
            db="pythonspot") # name of the database
        cur = db.cursor()
        print('message received:  %s' % message)
        #compare what message is recieved from the web page
        if message == 'conversion':
            #check for unit conversion request
            conversion_status = conversion_status ^ 1
        if message == 'Temperature':
            #fetch latest value from the database and send it to a web page
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                # To check if the sensor is disconnected
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    print(row[0]," ",row[1], row[2], row[3])
                    if conversion_status == 0:
                        temp_conversion = float(row[1])
                        temp_conversion = temp_conversion*1.8 + 32
                        temp_string = str(round(temp_conversion,3))
                        print('sending back message: %s' % (message+row[2]+temp_string))
                        self.write_message(message+row[2]+temp_string + ' F')
                    else:
                        self.write_message(message+row[2]+row[1]+' C')
        elif message == 'Temperature average':
            # Provide average temperature value to the webpage 
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    #fetch latest average temperature value from the data base
                    cur.execute("SELECT * FROM temperature_average ORDER by id DESC LIMIT 1")
                    for row in cur.fetchall():                    
                        if conversion_status == 0:
                            temp_conversion = float(row[1])
                            temp_conversion = temp_conversion*1.8 + 32
                            temp_string = str(round(temp_conversion,3))
                            print(row[0]," ",row[1], row[2])
                            print('sending back message: %s' % (message+row[2]+temp_string))
                        
                            self.write_message(message+row[2]+temp_string+' F')
                        else:
                            self.write_message(message+row[2]+row[1]+' C')
        elif message == 'Temperature minimum':
            #provide minimum temperature value fetched from the data base
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                #to check if the sensor is disconnected
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    if conversion_status == 0:
                        temp_conversion = float(row[3])
                        temp_conversion = temp_conversion*1.8 + 32
                        temp_string = str(round(temp_conversion,3))
                        print(row[0]," ",row[1], row[2], row[3])
                        print('sending back message: %s:' %(message+row[2]+temp_string))
                        self.write_message(message+row[2]+temp_string+' F')
                    else:
                        self.write_message(message+row[2]+row[3]+' C')
        elif message == 'Temperature maximum':
            #provide maximum temperature value fetched from the data base
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                #to check if the sensor is disconnected
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    if conversion_status == 0:
                        temp_conversion = float(row[4])
                        temp_conversion = temp_conversion*1.8 + 32
                        temp_string = str(round(temp_conversion,3))
                        print(row[0]," ",row[1], row[2], row[3])
                        print('sending back message: %s' % (message+row[2]+temp_string))
                        self.write_message(message+row[2]+temp_string + ' F')
                    else:
                        self.write_message(message+row[2]+row[4]+' C')
        elif message == 'Humidity':
            #fetch latest value from the database and send it to a web page
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                # To check if the sensor is disconnected
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    print(row[0]," ",row[1], row[2], row[3])
                    print('sending back message: %s' % (message+row[2]+row[1]+' %'))
                    self.write_message(message+row[2]+row[1] + ' %')
        elif message == 'Humidity average':
            # Provide average humidity value to the webpage 
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    cur.execute("SELECT * FROM humidity_average ORDER by id DESC LIMIT 1")
                    for row in cur.fetchall():
                        print(row[0]," ",row[1], row[2])
                        print('sending back message: %s' % (message+row[2]+row[1]))
                        self.write_message(message+row[2]+row[1] + ' %')
        elif message == 'Humidity minimum':
            #provide minimum humidity value fetched from the data base
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                # To check if the sensor is disconnected
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    print(row[0]," ",row[1], row[2], row[3])
                    print('sending back message: %s' % (message+row[2]+row[3]))
                    self.write_message(message+row[2]+row[3])
        elif message == 'Humidity maximum':
            #provide maximum humidity value fetched from the data base
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                # To check if the sensor is disconnected
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    print(row[0]," ",row[1], row[2], row[3])
                    print('sending back message: %s' % (message+row[2]+row[4]))
                    self.write_message(message+row[2]+row[4] + ' %')
    def on_close(self):
        '''
        on_close function is called when the websocket connection is closed either by the client or server itself 
        '''
        print('connection closed')
 
    def check_origin(self, origin):
        return True
#open the webserver application
application = tornado.web.Application([
    (r'/ws', WSHandler),
    ])

#tornado server parameters
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
