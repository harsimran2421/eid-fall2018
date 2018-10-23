Author: Harsimransingh  Bindra
Date: 10/21/2018

Installation Instructions
  Webserver
    1. cd Project-2/
    2. sudo python3 server.py
    3. need MYSqlDB installed on the platform(to access the database)

  Sensor code
    1. cd Project-2/
    2. sudo python3 project.py
    3. (Need the Adafruit library and MYSqlDB to run the code)

Project description: 
QT Application side
An application is created to display the readings from DHT22 temperature sensor. Temperature values in celcius and humidity values in percentage are printed. The application also contains graphical representation of last 10 temperature and humidity values. The average values of temperature and humidity are also displayed in the application. There are two spin boxes used to set the threshold values for temperature and humidity. If the current values exceed the set threshold,then a warning message is displayed on the application. In addition to the warning display message, an email notification is sent to the desired user too. The valuesa are stored in the SQL database after every 5 seconds. The minimum and maximum values for temperature and humidity is retrieved from the database and displayed in the QT application as well. There is an option on the Qt application to display the temperature vaues in either celcius or farheneit units.

Webserver side
A webpage is created to display 8 values
  Temperature - immediate value, average, minimum, maximum
  Humidity - immediate value, average, minimum, maximum
Webserver consumes data from the database used by the sensor code.

References
  1. https://ralsina.me/posts/BB974.html
  2. https://stackoverflow.com/questions/11812000/login-dialog-pyqt
  3. https://gist.github.com/pklaus/3e16982d952969eb8a9a
  4. http://pyqt.sourceforge.net/Docs/PyQt4/qspinbox.html
  5. https://os.mbed.com/cookbook/Websockets-Server
  6. http://jqueryui.com/
  7. http://api.jquery.com/click/
  


