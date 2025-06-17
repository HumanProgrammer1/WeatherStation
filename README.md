This is my own quick install for setting up my weather station OS + Script - feel free to use it!

Raspberry Pi Weather Station Code. Use this how you like. It assumes that you are using InfluxDB v1 (Important!) and that you want to record data every 30s for Temperature, Pressure, humidity and Wind Speed/Gust. The ground temperature probe (DS18B20) records every 5 minutes. 

Due to my own personal way of wanting to wiring stuff, you may want to use your own so remember to change that in the script!

How to Install: (assuming that git is install on RPI)
```
sudo pip3 install pimoroni-bme280 smbus --break-system-package
sudo pip3 install influxdb --break-system-package
sudo git clone https://github.com/HumanProgrammer1/WeatherStation.git
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
sudo apt-get update && sudo apt-get install influxdb
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
```
Remeber to Enable I2C and SPI in Raspberry Pi Config
```
sudo raspi-config
```
Then Interface>I2C + Interface>SPI,
Remember to reboot!

Enter into the Influx terminal: 
```
influx
```
or to connect with Human Readable timestamp 
```
influx -precision rfc3339
```
then create a database
```
CREATE DATABASE {database name}
```
Edit the scripts to reflect your details, if there is no Username or Password set, you can just leave it. 

Crontab is used to start the scripts on boot. 
```
@reboot sleep 60; sudo /usr/bin/python3 /home/USERNAME/WeatherStation/wind_speed.py
@reboot sleep 60; sudo /usr/bin/python3 /home/USERNAME/WeatherStation/rainfall.py
@reboot sleep 60; sudo /usr/bin/python3 /home/USERNAME/WeatherStation/bme280_data.py
0 */2 * * * sudo reboot
*/5 * * * * sudo /usr/bin/python3 /home/USERNAME/WeatherStation/DS18B20_therm.py
@reboot sleep 60; echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
```

If you are using the DS18B20 temperature sensor, the following needs added to: 
```
sudo nano /boot/firmware/config.txt
```
then to the bottom, add: 
```
dtoverlay=w1-gpio
```
Then open: 
```
sudo nano /etc/modules
```
and add, to the bottom. 
```
w1-gpio
w1-therm
```
then reboot your system. 

From here, just change the scripts and connect your sensors, test the scripts (they need to run with sudo....) and hopefully it works. 

Enjoy your Meteorology Journey. 
