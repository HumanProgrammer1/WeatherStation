import time
from smbus2 import SMBus
from bme280 import BME280
from gpiozero import CPUTemperature
from influxdb import InfluxDBClient
import datetime

# Initialize temperature sensor and InfluxDB client
try:
    cpu = CPUTemperature()
    influx_client = InfluxDBClient(host='localhost', port=8086, username='USERNAME', password='PASSWORD', database='DATABASE')
    print("InfluxDB client and CPU temperature sensor initialized.")
except Exception as e:
    print(f"Error initializing InfluxDB or CPU sensor: {e}")

# Initialize I2C bus and BME280 sensor
try:
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)
    print("BME280 sensor initialized successfully.")
    time.sleep(10)  # Allow sensor to stabilize
except Exception as e:
    print(f"Error initializing BME280: {e}")

# Flag to discard the first measurement
first_run = True

def log_cpu_temperature():
    try:
        val = cpu.temperature
        fields_system = {"cpu_temperature": val}
        json_body = [{
            "measurement": "systemstats",
            "tags": {},
            "fields": fields_system,
        }]
        influx_client.write_points(json_body)
        print(f"Logged CPU temperature: {val:.2f}°C")
    except Exception as e:
        print(f"Error logging CPU temperature: {e}")

def log_bme280_data():
    global first_run
    try:
        temperature = bme280.get_temperature()
        humidity = bme280.get_humidity()
        pressure = bme280.get_pressure()

        if first_run:
            first_run = False
            print("Skipping first BME280 measurement (sensor warm-up).")
            return

        json_body = [{
            "measurement": "bme280",
            "tags": {"source": "bme280"},
            "fields": {"temperature": temperature, "humidity": humidity, "pressure": pressure}
        }]
        influx_client.write_points(json_body)

        print(f"Temperature: {temperature:.2f}°C")
        print(f"Humidity: {humidity:.2f}%")
        print(f"Pressure: {pressure:.2f} hPa")

    except Exception as e:
        print(f"Error logging BME280 data: {e}")

# Infinite loop to log data every 30 seconds
try:
    print("Starting data logging loop. Press Ctrl+C to stop.")
    while True:
        log_cpu_temperature()
        log_bme280_data()
        time.sleep(30)
except KeyboardInterrupt:
    print("Data logging stopped by user.")
