Author: Harsimransingh Bindra
Date: 09/26/2018
Installation Instructions:
  1. cd Project-1/
  2. python3 project.py
  3. (Need the Adafruit library to run the code)

Project description: A application is created to display the readings from DHT22 temperature sensor. Temperature values in celcius and humidity values in percentage are printed. The application also contains graphical representation of last 10 temperature and humidity values. The application also displays the average values of temperature and humidity. There are two spin boxes used to setup the threshold values for temperature and humidity. If the current values exceed the set threshold warning message is displayed on the application. In addition to the warning display message an email notification is sent to the desired user too.
references:
  1. https://ralsina.me/posts/BB974.html
  2. https://stackoverflow.com/questions/11812000/login-dialog-pyqt
  3. https://gist.github.com/pklaus/3e16982d952969eb8a9a
  4. http://pyqt.sourceforge.net/Docs/PyQt4/qspinbox.html
  5. 
Project addition:
  1. Implemented a login screen to secure the application
  2. Retrieved the temperature and humidity values ona timer of 3 seconds and store values for a graph
  3. Displaying the latest 6 temperature and humidity values on the graph
  4. Display a warning message on the application if temperature or humidity value exceed over the set threshold.
  5. Send an email notification to the user once the threshold value is exceeded
