import time
import urequests
from machine import Pin, I2C
import bme280
import network

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Wi-Fi connected:', wlan.ifconfig())

def log_to_google_sheets(temperature):
    url = "https://script.google.com/macros/s/AKfycbwf-rSljnE4a3iNeP44xvckfUcFgIp1FQTLCTXmAsR3ZtQo3gy7bAfsyPqYjbgEeKg-OQ/exec"
    payload = {"temperature": temperature, "location": "Indoor"}
    response = urequests.post(url, json=payload)
    if response.status_code == 200:
        print("Data logged to Google Sheets successfully")
    else:
        print("Error logging data to Google Sheets")

wifi_ssid = "The Iqbal's"
wifi_password = "Zeeshan786"

connect_wifi(wifi_ssid, wifi_password)

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
bme = bme280.BME280(i2c=i2c)

print("Collecting indoor temperature data...")
for _ in range(10):
    temperature, _, _ = bme.read_compensated_data()
    temperature /= 100  
    print("Temperature:", temperature) 
    log_to_google_sheets(temperature)  
    time.sleep(10)
