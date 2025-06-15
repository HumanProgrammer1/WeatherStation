from influxdb import InfluxDBClient
import RPi.GPIO as GPIO
import time
import math

# Configure GPIO
WIND_SENSOR_PIN = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(WIND_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configure InfluxDB connection
INFLUXDB_ADDRESS = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_USER = "USERNAME"
INFLUXDB_PASSWORD = "PASSWORD"
INFLUXDB_DATABASE = "DATABASE"

client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUXDB_DATABASE)
client.create_database(INFLUXDB_DATABASE)

def upload_to_influxdb(wind_speed, gust_speed):
    json_body = [
        {
            "measurement": "wind",
            "tags": {
                "location": "home"
            },
            "fields": {
                "wind_speed_mph": wind_speed,
                "gust_speed_mph": gust_speed
            }
        }
    ]
    client.write_points(json_body)

# Initialize variables
ANEMOMETER_RADIUS_CM = 9
CIRCUMFERENCE_CM = math.pi * (2 * ANEMOMETER_RADIUS_CM)  # Calculate circumference
CIRCUMFERENCE_MILES = CIRCUMFERENCE_CM * 0.0000062137  # Convert cm to miles
COUNT_PER_REVOLUTION = 2  # Two pulses per revolution
count = 0
start_time = time.time()
wind_speeds = []

# Define wind speed callback function
def wind_speed_callback(channel):
    global count
    count += 1

# Set up event detection for anemometer pulses
GPIO.add_event_detect(WIND_SENSOR_PIN, GPIO.FALLING, callback=wind_speed_callback)

try:
    while True:
        time.sleep(3)  # Sample every 3 seconds
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            revolutions = count / COUNT_PER_REVOLUTION
            ANEMOMETER_FACTOR = 1.8  # Correction factor for anemometer efficiency
            wind_speed_mph = (revolutions / elapsed_time) * 3600 * CIRCUMFERENCE_MILES
            wind_speed_mph *= ANEMOMETER_FACTOR  # Apply the correction

        else:
            wind_speed_mph = 0

        wind_speeds.append(wind_speed_mph)

        # Debugging output
        print(f"Count: {count}, Wind Speed: {wind_speed_mph:.2f} mph")

        # Reset counters
        count = 0
        start_time = time.time()

        if len(wind_speeds) >= 10:
            max_wind_gust = max(wind_speeds)
            avg_wind_speed = sum(wind_speeds) / len(wind_speeds)
            print(f"Wind Gust: {max_wind_gust:.2f} mph")
            print(f"Average Wind Speed: {avg_wind_speed:.2f} mph")

            # Upload data to InfluxDB
            upload_to_influxdb(avg_wind_speed, max_wind_gust)

            # Reset list for the next 30-second period
            wind_speeds = []

except KeyboardInterrupt:
    print("Stopped")
    GPIO.cleanup()
