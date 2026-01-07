import RPi.GPIO as GPIO
import adafruit_dht
import time
import pandas as pd
from datetime import datetime

# GPIO Setup
GPIO.setmode(GPIO.BCM)
SOIL_SENSOR_PIN = 4  # A0 pin connected to GPIO 04
DHT_SENSOR_PIN = 27  # DHT11 data pin
dht_device = adafruit_dht.DHT11(DHT_SENSOR_PIN)

# Data storage
data = []
collection_duration = 48
interval = 30
total_readings = (collection_duration * 60) // interval

def read_soil_moisture():
    GPIO.setup(SOIL_SENSOR_PIN, GPIO.IN)
    time.sleep(0.1)
    moisture_value = GPIO.input(SOIL_SENSOR_PIN)
    calibrated_moisture = moisture_value * 1023
    return calibrated_moisture

def read_temperature_humidity():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return temperature, humidity
    except RuntimeError as e:
        print(f"DHT Sensor Error: {e}")
        return None, None


print(f"Starting data collection for {collection_duration} hours (interval: {interval} mins)")
for i in range(total_readings):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    soil_moisture = read_soil_moisture()
    temp, air_humidity = read_temperature_humidity()

    if temp is not None and air_humidity is not None:
        data.append([timestamp, soil_moisture, temp, air_humidity])
        print(f"Reading {i+1}/{total_readings}: {timestamp} - Soil Moisture: {soil_moisture}, Temp: {temp}°C, Air Humidity: {air_humidity}%")
    time.sleep(interval * 60)

df = pd.DataFrame(data, columns=["Timestamp", "Soil_Moisture", "Temperature", "Air_Humidity"])
df.to_csv("sensor_data.csv", index=False)
print("Data collection complete. Saved to sensor_data.csv")

GPIO.cleanup()
dht_device.exit()
