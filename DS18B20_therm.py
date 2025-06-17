from influxdb import InfluxDBClient
import os, glob, time

class DS18B20(object):
    def __init__(self):
        self.device_file = glob.glob("/sys/bus/w1/devices/28*")[0] + "/w1_slave"

    def read_temp_raw(self):
        with open(self.device_file, "r") as f:
            return f.readlines()

    def crc_check(self, lines):
        return lines[0].strip()[-3:] == "YES"

    def read_temp(self):
        temp_c = -255
        attempts = 0

        lines = self.read_temp_raw()
        success = self.crc_check(lines)

        while not success and attempts < 3:
            time.sleep(.2)
            lines = self.read_temp_raw()
            success = self.crc_check(lines)
            attempts += 1

        if success:
            temp_line = lines[1]
            equal_pos = temp_line.find("t=")
            if equal_pos != -1:
                temp_string = temp_line[equal_pos+2:]
                temp_c = float(temp_string)/1000.0

        return temp_c

def write_to_influx(temp_c):
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('DATABASE')

    json_body = [
        {
            "measurement": "ds18b20_temp",
            "tags": {
                "location": "5cm depth"
            },
            "fields": {
                "temperature": temp_c
            }
        }
    ]

    client.write_points(json_body)

if __name__ == "__main__":
    sensor = DS18B20()
    temp = sensor.read_temp()
    print("Temp: %.2f °C" % temp)
    write_to_influx(temp)



