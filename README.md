This is my own quick install for settubg up my weather station OS + Script - feel free to use it!

Raspberry Pi Weather Station Code. Use this how you like. It assumes that you are using InfluxDB v1 (Important!) and that you want to record data every 30s for Temperature, Pressure, humidity and Wind Speed/Gust. The ground temperature probe (DS18B20) records every 5 minutes. 

Due to my own personal way of wanting to wiring stuff, you may want to use your own so remember to change that in the script!

How to Install: (assuming that git is install on RPI)
```
sudo pip3 install pimoroni-bme280 smbus --break-system-package
sudo pip3 install influxdb --break-system-package
sudo git clone https://github.com/HumanProgrammer1/WeatherStation.git
```
Crontab is used to start the scripts on boot. 
```
@reboot sleep 60; sudo /usr/bin/python3 /home/USERNAME/WeatherStation/wind_speed.py
@reboot sleep 60; sudo /usr/bin/python3 /home/USERNAME/WeatherStation/rainfall.py
@reboot sleep 60; sudo /usr/bin/python3 /home/USERNAME/WeatherStation/bme280_data.py
0 */2 * * * sudo reboot
*/5 * * * * sudo /usr/bin/python3 /home/USERNAME/WeatherStation/DS18B20_therm.py
@reboot sleep 60; echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
```
