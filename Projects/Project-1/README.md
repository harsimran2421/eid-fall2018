Author: Harsimransingh Bindra
Date: 09/26/2018
Installation Instructions:
  1. cd Project-1/
  2. python3 project.py
  3. (Need the Adafruit library to run the code)

Project description: An application is created to display the readings from DHT22 temperature sensor. Temperature values in celcius and humidity values in percentage are printed. The application also contains graphical representation of last 10 temperature and humidity values. The average values of temperature and humidity are also displayed in the application. There are two spin boxes used to set the threshold values for temperature and humidity. If the current values exceed the set threshold,then a warning message is displayed on the application. In addition to the warning display message, an email notification is sent to the desired user too.

References:
  1. https://ralsina.me/posts/BB974.html
  2. https://stackoverflow.com/questions/11812000/login-dialog-pyqt
  3. https://gist.github.com/pklaus/3e16982d952969eb8a9a
  4. http://pyqt.sourceforge.net/Docs/PyQt4/qspinbox.html
 
Project addition:
  1. Implemented a login screen to secure the application
  2. Retrieved the temperature and humidity values ona timer of 3 seconds and store values for a graph
  3. Displaying the latest 6 temperature and humidity values on the graph
  4. Display a warning message on the application if temperature or humidity value exceed over the set threshold.
  5. Send an email notification to the user once the threshold value is exceeded
  6. Used a spin lock to take in and set the threshold values for temperature and humidity
