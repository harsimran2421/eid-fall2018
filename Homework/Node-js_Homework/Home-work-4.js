/*Author name: Harsimransingh Bindra
 *Date: 10/07/2018
 *File: Home-work 4 Node.js programming
 *Description: program that reads 10 values (one every 10 seconds) from the DHT22 sensor *on your Pi and prints out to the console log each reading as well as the lowest,
 *highest, and average of the readings
 *References:
 *          1. https://github.com/momenso/node-dht-sensor
 *          2. http://www.airspayce.com/mikem/bcm2835/
 *          3. https://nodejs.org/en/download/
 *          4. https://www.raspberrypi.org/documentation/usage/gpio/
 * */
/*Library to be included for the DHT22 sensor*/
var Library = require("node-dht-sensor");
/*arrays to store the average values*/
var temp_avg = [];
var hum_avg = [];

var i = 0,temp_sum = 0, hum_sum = 0;
/*variables to store the min max values for temperature and humidity*/
var temp_min_value = 50;
var temp_max_value = 0;
var hum_min_value = 50;
var hum_max_value = 0;

/*variable storing the function for temperature and humidity read*/
var sensor = {
  sensors: {
    name: "Current values",
    type: 22,
    pin: 4
  },
  read: function() {
    if(i<10)
    {
      i = i+1;
    }
    else
    {
      i = 1;
    }
    /*read temperature and humidity values*/
    var b = Library.read(this.sensors.type, this.sensors.pin);
    console.log((i)+". "+this.sensors.name + ": " +
      b.temperature.toFixed(1) + "°C, " +
      b.humidity.toFixed(1) + "%");
    /*timeout function used to call the read function after every 10 seconds*/
    setTimeout(function() {
      sensor.read();
    }, 10000);
    temp_avg[i-1] = b.temperature;
    hum_avg[i-1] = b.humidity;
    var j = 0;
    temp_sum = 0;
    hum_sum = 0;
    /*loop to calculate temperature and humidity average values after 10 latest values are stored*/
    if(i == 10)
    {
      for(j = 0; j<10 ; j++)
      {
        temp_sum += temp_avg[j];
        hum_sum += hum_avg[j];
      }
    }
    /*to store the minimum temperature value*/
    if(temp_avg[i-1]<temp_min_value)
    {
      temp_min_value = temp_avg[i-1];
    }
    /*to store the maximum temperature value*/
    if(temp_avg[i-1] > temp_max_value)
    {
      temp_max_value = temp_avg[i-1];
    }
    /*to store minimum humidty value*/
    if(hum_avg[i-1]<hum_min_value)
    {
      hum_min_value = hum_avg[i-1];
    }
    /*to store maximum temperature value*/
    if(hum_avg[i-1] > hum_max_value)
    {
      hum_max_value = hum_avg[i-1];
    }
    /*calculate the temperature average*/
    temp_sum = temp_sum/j;
    /*calculate the humidity average*/
    hum_sum = hum_sum/j;
    if(i == 10)
    {
      console.log("Avg value for temperature is: "+temp_sum.toFixed(2)+"°C");
      console.log("Minimum value for temperature is: "+temp_min_value.toFixed(2)+"°C");
      console.log("Maximum value for temperature is: "+temp_max_value.toFixed(2)+"°C");
      console.log("Avg value for Humidity is: "+hum_sum.toFixed(2)+"%");
      console.log("Minimum value for Humidity is: "+hum_min_value.toFixed(2)+"%");
      console.log("Maximum value for Humidity is: "+hum_max_value.toFixed(2)+"%");
    }
  }
};
/*call the read function to start the loop*/
sensor.read();
