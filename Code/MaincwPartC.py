import network
import urequests
from machine import Pin, I2C
import bme280
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Wi-Fi connected:', wlan.ifconfig())

def log_to_google_sheets(temperature, humidity, pressure):
    url = "https://script.google.com/macros/s/AKfycbz1bn1lG-lMzdWJgbLmSVCRIr7O2nt6j-yjzFPBD86YdF1D_bsd3_zZ8SAlOQeB0_wG9A/exec"
    payload = {"temperature": temperature, "humidity": humidity, "pressure": pressure}
    response = urequests.post(url, json=payload)
    if response.status_code == 200:
        print("Data logged to Google Sheets successfully")
    else:
        print("Error logging data to Google Sheets")

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
bme = bme280.BME280(i2c=i2c)

wifi_ssid = "The Iqbal's"
wifi_password = "Zeeshan786"
connect_wifi(wifi_ssid, wifi_password)

while True:
    temperature, pressure, humidity = bme.read_compensated_data()
    log_to_google_sheets(temperature / 100, humidity / 1024, pressure / 25600)
    time.sleep(60)  
