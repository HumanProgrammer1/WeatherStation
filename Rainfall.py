import time
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient

# Configuration
RAIN_SENSOR_PIN = 21  # GPIO pin where the rain gauge is connected
INFLUXDB_HOST = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'USERNAME'
INFLUXDB_PASSWORD = 'PASSWORD'
INFLUXDB_DATABASE = 'DATABASE'
BUCKET_VOLUME_MM = 0.2794  # Amount of rain per bucket tip

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Connect to InfluxDB
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, username=INFLUXDB_USER,
                        password=INFLUXDB_PASSWORD, database=INFLUXDB_DATABASE)

def bucket_tipped(channel):
    """Function called when the bucket tips."""
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    rainfall = BUCKET_VOLUME_MM

    data_point = [
        {
            "measurement": "rainfall",
            "tags": {
                "sensor": "rain_gauge"
            },
            "time": timestamp,
            "fields": {
                "rainfall_mm": rainfall
            }
        }
    ]

    client.write_points(data_point)
    print(f"Bucket tipped at {timestamp}, recorded {rainfall} mm.")



def test_event_detection():
    """Test manual event detection."""
    GPIO.add_event_detect(RAIN_SENSOR_PIN, GPIO.FALLING, callback=bucket_tipped, bouncetime=100)  # Adjusted bouncetime
    if GPIO.event_detected(RAIN_SENSOR_PIN):
        print("Event detected!")

# Add event detection
GPIO.add_event_detect(RAIN_SENSOR_PIN, GPIO.FALLING, callback=bucket_tipped, bouncetime=100)

try:
    print("Listening for rainfall events...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping script.")
finally:
    GPIO.cleanup()

