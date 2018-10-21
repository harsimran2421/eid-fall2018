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
        print('new connection')

    def on_message(self, message):
        global conversion_status
        db = MySQLdb.connect(host="localhost", # your host
            user="root",
            # username
            passwd="root", # password
            db="pythonspot") # name of the database
        cur = db.cursor()
        print('message received:  %s' % message)
        # Reverse Message and send it back
        if message == 'conversion':
            conversion_status = conversion_status ^ 1
        if message == 'Temperature':
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
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
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
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
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
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
            cur.execute("SELECT * FROM temperature ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
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
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    print(row[0]," ",row[1], row[2], row[3])
                    print('sending back message: %s' % (message+row[2]+row[1]))
                    self.write_message(message+row[2]+row[1])
        elif message == 'Humidity average':
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    cur.execute("SELECT * FROM humidity_average ORDER by id DESC LIMIT 1")
                    for row in cur.fetchall():
                        print(row[0]," ",row[1], row[2])
                        print('sending back message: %s' % (message+row[2]+row[1]))
                        self.write_message(message+row[2]+row[1])
        elif message == 'Humidity minimum':
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    print(row[0]," ",row[1], row[2], row[3])
                    print('sending back message: %s' % (message+row[2]+row[3]))
                    self.write_message(message+row[2]+row[3])
        elif message == 'Humidity maximum':
            cur.execute("SELECT * FROM humidity ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                if row[1] == 'Not Connected':
                    self.write_message(message+'00:00:00   00/00/00'+'Not Connected')
                else:
                    print(row[0]," ",row[1], row[2], row[3])
                    print('sending back message: %s' % (message+row[2]+row[4]))
                    self.write_message(message+row[2]+row[4])

    def on_close(self):
        print('connection closed')
 
    def check_origin(self, origin):
        return True
application = tornado.web.Application([
    (r'/ws', WSHandler),
    ])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
